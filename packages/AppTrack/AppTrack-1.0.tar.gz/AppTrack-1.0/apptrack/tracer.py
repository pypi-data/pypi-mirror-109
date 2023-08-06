#!/usr/bin/python
# coding:utf-8

from __future__ import absolute_import
import six
from collections import namedtuple
import json
import struct
import time
import os
import random

import opentracing
from opentracing import Reference, ReferenceType, Format, UnsupportedFormatException, SpanContextCorruptedException
from opentracing.ext import tags as ext_tags

from . import db
from . import constants
from .codecs import TextCodec,  BinaryCodec
from .span import Span, SAMPLED_FLAG, DEBUG_FLAG
from .span_context import SpanContext
from .constants import START_TIME, SPAN_ID, MAX_ID_BITS, GEN_ID_RANGE
from .metrics import Metrics, LegacyMetricsFactory
import md5

def msg_id(msg=''):
    if not isinstance(msg, str) or msg=='':
        return None
    d=md5.new(msg).hexdigest()
    return int(d[:6],16)

class Tracer(opentracing.Tracer):
    def __init__(self, service_name, reporter, sampler, metrics=None,
        metrics_factory=None,
        trace_id_header=constants.TRACE_ID_HEADER,
        baggage_header_prefix=constants.BAGGAGE_HEADER_PREFIX,
        debug_id_header=constants.DEBUG_ID_HEADER_KEY,
        tags=None, 
        max_tag_value_length=constants.MAX_TAG_VALUE_LENGTH,
        ):
        self.service_name = service_name
        self.reporter = reporter
        self.sampler = sampler
        self.metrics_factory = metrics_factory or LegacyMetricsFactory(metrics or Metrics())
        self.metrics = TracerMetrics(self.metrics_factory)
        self.debug_id_header = debug_id_header
        self.max_tag_value_length = max_tag_value_length
        self.random = random.Random(time.time() * (os.getpid() or 1))
        self.codecs = {
            Format.TEXT_MAP: TextCodec(
                url_encoding=False,
                trace_id_header=trace_id_header,
                baggage_header_prefix=baggage_header_prefix,
                debug_id_header=debug_id_header,
            ),
            Format.HTTP_HEADERS: TextCodec(
                url_encoding=True,
                trace_id_header=trace_id_header,
                baggage_header_prefix=baggage_header_prefix,
                debug_id_header=debug_id_header,
            ),
            Format.BINARY: BinaryCodec(),
        }
        self.tags = {
            constants.APPTRACK_VERSION_TAG_KEY: constants.APPTRACK_CLIENT_VERSION,
        }
        if tags:
            self.tags.update(tags)

        self.trace_id=msg_id(self.service_name)

    def start_span(self, operation_name, child_of=None, references=None, tags=None,start_time=None,log_rings=[]):
        
        parent = child_of
        if references:
            if isinstance(references, list):
                # TODO only the first reference is currently used
                references = references[0]
            parent = references.referenced_context

        # allow Span to be passed as reference, not just SpanContext
        if isinstance(parent, Span):
            parent = parent.context

        tags = tags or {}
        if parent is None or parent.referenced_context.is_debug_id_container_only:
            trace_id = self.trace_id if self.trace_id else self.random_id()
            span_id = trace_id
            parent_id = None
            flags = 0
            baggage = None
            if parent is None:
                sampled, sampler_tags = \
                    self.sampler.is_sampled(trace_id, operation_name)
                if sampled:
                    flags = SAMPLED_FLAG
                    for k, v in six.iteritems(sampler_tags):
                        tags[k] = v
            else:  # have debug id
                flags = SAMPLED_FLAG | DEBUG_FLAG
                tags[self.debug_id_header] = parent.debug_id
        else:
            trace_id = parent.referenced_context.trace_id
            #必须要求父span和子span的trace_id一致
            assert(str(self.trace_id) == str(trace_id))
            parent_id = parent.referenced_context.span_id
            flags = parent.referenced_context.flags
            baggage = dict(parent.referenced_context.baggage)
            if isinstance(references, Reference):
                if references.type == ReferenceType.FOLLOWS_FROM:
                    parent_id = parent.parent_id
        
        span_id=self.gen_id()
        span_ctx = SpanContext(trace_id=trace_id, span_id=span_id,
                               parent_id=parent_id, flags=flags,
                               baggage=baggage)
        tags.update(self.tags)
        span = Span(context=span_ctx, tracer=self, operation_name=operation_name,log_rings=log_rings,tags=tags)
        if operation_name is not None:
            span.set_operation_name(operation_name)
        span.start()
        return span

    def inject(self, span_context, format, carrier):
        codec = self.codecs.get(format, None)
        if codec is None:
            raise UnsupportedFormatException(format)
        if isinstance(span_context, Span):
            # be flexible and allow Span as argument, not only SpanContext
            span_context = span_context.context
        if not isinstance(span_context, SpanContext):
            raise ValueError(
                'Expecting Apptack SpanContext, not %s', type(span_context))
        codec.inject(span_context=span_context, carrier=carrier)

    def extract(self, format, carrier):
        codec = self.codecs.get(format, None)
        if codec is None:
            raise UnsupportedFormatException(format)
        context = codec.extract(carrier)
        if context is not None:
            #解包后的span_id是一个整数,需要和数据库里面存放的span_id进行转换
            context.span_id = self.form_span_id(context.span_id)
            assert(context.trace_id == context.trace_id)
        return context

    def report_span(self, span):
        self.reporter.report_span(span)
        
    def finish_span(self,span):
        self.reporter.finish_span(span)

    def random_id(self):
        return self.random.getrandbits(MAX_ID_BITS)

    def gen_id(self):
        span_id = db.TraceDb.get_db().create_span_id()
        return span_id
        
    def form_span_id(self,span_id):
        return db.TraceDb.get_db().form_span_id(span_id)

    def whole_system_root_span(self):
        REG_WHOLE_SYSTEM_SCRIPT = """
        key = db.work_on_key()
        (s, v) = db.get(key)
        if s.not_found():
            s = db.put(key, span_id)
            if s.ok():
                return '{"status":"ok", "ret": "%s" }' % span_id
            else:
                return '{"status":"error", "ret": "put whole system root span id %s failed" % str(span_id) }'
        else:
            if s.ok():
                return '{"status":"ok", "ret": "%s" }' % str(v)
            else:
                return '{"status":"error", "ret": "get whole system root span id %s failed, because %s" % (str(span_id), str(s)) }'"""
                
        print ggggggggggg
        root_span_info = self.taskdb().get(define.WHILE_SYSTEM_ROOT_SPAN_PATH)

        if root_span_info['reason'] == 'ok':
            try:
                span_id = root_span_info['ret']

                assert name_to_standard(span_id) == span_id
                span_ctx = self.extract(Format.TEXT_MAP, {"span_context": {SPAN_ID: span_id}})
                return Span(self, span_ctx)
            except Exception, ex:
                pass
        else:
            s = Span(self, None)
            root_span_info = self.taskdb().exec_script(define.WHILE_SYSTEM_ROOT_SPAN_PATH,
                                                       "span_id='" + s.context.span_id + "'\n" + REG_WHOLE_SYSTEM_SCRIPT)

            if root_span_info['reason'] == 'ok':
                try:
                    span_id_info = json.loads(root_span_info['ret'])
                    if span_id_info['status'] == 'ok':
                        span_id = span_id_info['ret']

                        assert name_to_standard(span_id) == span_id
                        span_ctx = self.extract(Format.TEXT_MAP, {"span_context": {SPAN_ID: span_id}})
                        root_span = Span(self, span_ctx)
                        root_span.set_operation_name("gtx_cloud_root")
                        return root_span
                    else:
                        raise SpanContextCorruptedException()
                except Exception, ex:
                    # print exception_report(str(ex))
                    raise SpanContextCorruptedException()
            else:
                raise SpanContextCorruptedException()
                
    def get_span(self,span_id,contain_child=False):
        return db.TraceDb.get_db().get_span_info(span_id,contain_child)

    def get_logs(self,span_id,timestamp=None,log_ring=None):
        return db.TraceDb.get_db().get_span_logs(span_id,timestamp,log_ring)
        
    def get_context(self,span_id):
        return db.TraceDb.get_db().get_span_context(span_id)
        
    def set_span_name(self,span_id,name):
        db.TraceDb.get_db().set_span_name(span_id,name)

class TracerMetrics(object):
    """Tracer specific metrics."""

    def __init__(self, metrics_factory):
        self.traces_started_sampled = \
            metrics_factory.create_counter(name='algo.traces-started', tags={'sampled': 'true'})
        self.traces_started_not_sampled = \
            metrics_factory.create_counter(name='algo.traces-started', tags={'sampled': 'false'})
        self.traces_joined_sampled = \
            metrics_factory.create_counter(name='algo.traces-joined', tags={'sampled': 'true'})
        self.traces_joined_not_sampled = \
            metrics_factory.create_counter(name='algo.traces-joined', tags={'sampled': 'false'})
        self.spans_sampled = \
            metrics_factory.create_counter(name='algo.spans', tags={'sampled': 'true'})
        self.spans_not_sampled = \
            metrics_factory.create_counter(name='algo.spans', tags={'sampled': 'false'})