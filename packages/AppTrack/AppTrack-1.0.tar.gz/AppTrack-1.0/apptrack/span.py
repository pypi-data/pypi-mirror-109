#!/usr/bin/python
# coding:utf-8

from __future__ import absolute_import

import time
import sys
import os
import json
import inspect
import threading
import traceback
import logging

import opentracing
from opentracing.ext import tags as opentracing_tags
from opentracing.propagation import SpanContextCorruptedException
import datetime

from .utils import gethostname,local_ip
from .span_context import SpanContext
from .constants import SAMPLED_FLAG, DEBUG_FLAG, APPTRACK_HOSTNAME_TAG_KEY, APPTRACK_IPV4_TAG_KEY
from . import codecs
from .thrift import make_string_tag, make_tags, make_log
import slugify
import traceback
import StringIO
import six


LOG_RING_DEFAULT = 'system_manager'

LOG_LEVEL_DBG = logging.getLevelName(logging.DEBUG)
LOG_LEVEL_INFO = logging.getLevelName(logging.INFO)
LOG_LEVEL_WARN = logging.getLevelName(logging.WARNING)
LOG_LEVEL_ERROR = logging.getLevelName(logging.ERROR)
LOG_LEVEL_FAULT = logging.getLevelName(logging.FATAL)
LOG_LEVEL_EXCEPTION = 'EXCEPTION'

class Span(opentracing.Span):
    __slots__ = ['_tracer', '_context',
                 'operation_name', 'start_time', 'end_time',
                 'logs', 'tags', 'update_lock']

    def __init__(self, context, tracer, operation_name=None,
                 tags=None, start_time=None,log_rings = []):
        super(Span, self).__init__(context=context, tracer=tracer)
        self.operation_name = operation_name
        self.start_time = start_time or datetime.datetime.utcnow()
        self.end_time = None
        self.update_lock = threading.Lock()
        self.tags = [(opentracing_tags.ERROR,False),(APPTRACK_HOSTNAME_TAG_KEY,gethostname()),(APPTRACK_IPV4_TAG_KEY,local_ip())]
        self.log_rings = log_rings
        if tags:
            for k, v in six.iteritems(tags):
                self.tags.append([k,v])
        if not self.log_rings:
            self.log_rings = [LOG_RING_DEFAULT]
                
    def start(self):
        self.tracer.report_span(self)

    def finish(self, finish_time=None,error=False,**kwargs):
        if not self.is_sampled():
            return

        self.end_time = finish_time or datetime.datetime.utcnow()
        if error:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            Span._on_error(self, exc_type, exc_value, exc_traceback)
            self.set_tags(kwargs)
        self.tracer.finish_span(self)
        
    def set_operation_name(self, operation_name):
        self.operation_name = operation_name
        self.tracer.set_span_name(self.span_id,self.operation_name)
        return opentracing.Span.set_operation_name(self,operation_name)

    @property
    def context(self):
        """Provides access to the SpanContext associated with this Span.

        The SpanContext contains state that propagates from Span to Span in a
        larger trace.

        :return: returns the SpanContext associated with this Span.
        """
        return self._context

    @property
    def tracer(self):
        """Provides access to the Tracer that created this Span.

        :return: returns the Tracer that created this Span.
        """
        return self._tracer

    @property
    def trace_id(self):
        return self.context.trace_id

    @property
    def span_id(self):
        return self.context.span_id

    @property
    def parent_id(self):
        return self.context.parent_id

    @property
    def flags(self):
        return self.context.flags

    def is_sampled(self):
        return self.context.flags & SAMPLED_FLAG == SAMPLED_FLAG

    def is_debug(self):
        return self.context.flags & DEBUG_FLAG == DEBUG_FLAG

    def __repr__(self):
        print self.context.trace_id,self.context.span_id,self.context.parent_id,self.context.flags
        c = codecs.span_context_to_string(trace_id=self.context.trace_id,span_id=self.context.span_id,
            parent_id=self.context.parent_id, flags=self.context.flags)
        return '%s %s.%s' % (c, self.tracer.service_name, self.operation_name)


    def set_tag(self, key, value):
        with self.update_lock:
            if key == opentracing_tags.SAMPLING_PRIORITY:
                if value > 0:
                    self.context.flags |= SAMPLED_FLAG | DEBUG_FLAG
                else:
                    self.context.flags &= ~SAMPLED_FLAG
            else:
                tag = make_string_tag(
                    key=key,
                    value=str(value),
                    max_length=self.tracer.max_tag_value_length,
                )
                #self.tags.append(tag)
        self.tracer.reporter.put_tag(self,key,value)
        return self
        
    def set_tags(self,tags):
        for k,v in tags.items():
            self.tracer.reporter.put_tag(self,k,v)
        return self

    def list_tags(self):
        return [t for t, v in self.tracer.taskdb().sdb.keys("/" + self.spanid, with_value=False)]


    def _logger(self, log_ring, log_level, content):
        assert(type(log_ring) == list)
        if self.is_debug():
            print "{ring}:{level} {content}" \
            .format(ring=log_ring,level=log_level,content=content)

        self.log_kv({
            opentracing.span.logs.EVENT:log_level,
            opentracing.span.logs.MESSAGE:content,
            'ring':log_ring
            })


    def logger(self,log_ring=[]):

        class span_logger:
            def __init__(self, ring, log_handle):
                self.log_ring = ring
                self.log = log_handle

            def debug(self, msg):
                self.log(self.log_ring, LOG_LEVEL_DBG,msg)

            def info(self, msg):
                self.log(self.log_ring, LOG_LEVEL_INFO,msg)

            def warn(self, msg):
                self.log(self.log_ring, LOG_LEVEL_WARN,msg)

            def error(self, msg):
                self.log(self.log_ring, LOG_LEVEL_ERROR,msg)
                
            def exception(self, msg=''):
                self.log(self.log_ring, LOG_LEVEL_EXCEPTION,msg)

            def fault(self, msg):
                self.log(self.log_ring, LOG_LEVEL_FAULT,msg)

        return span_logger(log_ring if log_ring else self.log_rings[0:1], self._logger)


    def log_kv(self, key_values, timestamp=None):
        timestamp = timestamp if timestamp else time.time()
        log = make_log(
            timestamp=timestamp if timestamp else time.time(),
            fields=key_values,
            max_length=self._tracer.max_tag_value_length,
        )
        # 下面的代码将获取对log_kv函数的调用者信息，已追加进日志记录中
        stacks = inspect.stack()
        if len(stacks) < 2:
            caller_fn = "Unkown"
            line_no = 0
            file_name = "Unkown"
        else:
            try:
                caller_class_self = stacks[1][0].f_locals.get("self", None)
                if caller_class_self == None:
                    caller_fn = stacks[1][3] + '(...)'
                else:
                    caller_fn = caller_class_self.__class__.__name__ + '.' + stacks[1][3] + '(...)'
            except:
                caller_fn = "Unkown"

            line_no = stacks[1][2]
            file_name = stacks[1][1]

      #  key_values.update({'caller_fn': caller_fn, 'line_no': line_no, 'file_name': file_name, "timestamp": timestamp})
        # 为每个log条目分配一个全局id号，注意如果多个进场都在向同一个span进行日志输出，那么，有可能这些id号是不连续的，因此为了让
        # log日志能按照时间顺序排列，我们还要在日志id号前面加上时间戳数据，此外， 通过spanid作为前缀的id号，我们将裁掉前面的spanid前缀，只保留后面的id
        # sorting logs
        default_event= self.operation_name if self.operation_name else 'other'
        event=key_values.pop(opentracing.span.logs.EVENT, default_event)
        message = key_values.pop(opentracing.span.logs.MESSAGE)
        self._tracer.reporter.put_log(self.span_id,event,message,rings=key_values.pop('ring'),**key_values)
        return self

    def set_baggage_item(self, key, value):
        prev_value = self.get_baggage_item(key=key)
        new_context = self.context.with_baggage_item(key=key, value=value)
        self._context = new_context
        logs = {
            'event': 'baggage',
            'key': key,
            'value': value,
            'message':'set span %s baggage item'%self.span_id,
            'ring':self.log_rings[0:1]
        }
        if prev_value:
            logs['override'] = True
        self.log_kv(key_values=logs)
        self._tracer.reporter.update_context(self._context)
        return self
        
    def set_baggage(self, baggage):
        for k,v in baggage.items():
            self.set_baggage_item(k,v)

    def get_baggage_item(self, key):
        return self.context.baggage.get(key)

    def __enter__(self):
        """Invoked when span is used as a context manager.

        :return: returns the Span itself
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ends context manager and calls finish() on the span.

        If exception has occurred during execution, it is automatically added
        as a tag to the span.
        """
        Span._on_error(self, exc_type, exc_val, exc_tb)
        self.finish()
        
    @staticmethod
    def _on_error(span, exc_type, exc_val, exc_tb):
        if not span or not exc_type:
            return

        io_err = StringIO.StringIO() 
        io_err.write('--- Logging exception ---\n')
        traceback.print_exception(exc_type, exc_val, exc_tb, None, io_err)
        io_err.write('Call stack:\n')
        span.set_tag(opentracing_tags.ERROR, True)
        span.log_kv({
            opentracing.span.logs.EVENT: LOG_LEVEL_EXCEPTION,
            opentracing.span.logs.MESSAGE: str(exc_val),
            opentracing.span.logs.ERROR_OBJECT: str(exc_val),
            opentracing.span.logs.ERROR_KIND: str(exc_type),
            opentracing.span.logs.STACK: io_err.getvalue(),
            'ring':span.log_rings
        })
        io_err.close()


def spanid_to_span(tracer, span_id, need_record_where_it_is=False, need_wait_events_collector=None):
    if need_record_where_it_is:
        timestamp = time.time()        
        key_values = {}
        self.log_kv({'event':[LOG_RING_0,LOG_LEVEL_INFO],
            'layload':json.dumps(key_values),
            'timestamp':timestamp,
            })
    trace_id=tracer.trace_id
    ctx = tracer.get_context(span_id)
    if ctx is None:
        ctx = SpanContext(trace_id=trace_id, span_id=span_id, parent_id=0)
    else:
        assert(str(ctx['trace_id']) == str(trace_id))
        ctx = SpanContext(trace_id=trace_id, span_id=span_id, parent_id=ctx.get('parent_id',None),flags=ctx['flags'],baggage=ctx['baggage'])
    return Span(ctx,tracer)