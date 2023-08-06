from __future__ import absolute_import
from builtins import object
import logging
import threading
import socket
from concurrent.futures import Future
from .constants import DEFAULT_FLUSH_INTERVAL
from . import thrift
from .metrics import Metrics, LegacyMetricsFactory
from .utils import ErrorReporter
import json
import six
import slugify

default_logger = logging.getLogger(__name__)


class NullReporter(object):
    """Ignores all spans."""
    def report_span(self, span):
        pass

    def set_process(self, service_name, tags, max_length):
        pass

    def close(self):
        fut = Future()
        fut.set_result(True)
        return fut


class InMemoryReporter(NullReporter):
    """Stores spans in memory and returns them via get_spans()."""
    def __init__(self):
        super(InMemoryReporter, self).__init__()
        self.spans = []
        self.lock = threading.Lock()

    def report_span(self, span):
        with self.lock:
            self.spans.append(span)

    def get_spans(self):
        with self.lock:
            return self.spans[:]


class LoggingReporter(NullReporter):
    """Logs all spans."""
    def __init__(self, logger=None):
        self.logger = logger if logger else default_logger

    def report_span(self, span):
        self.logger.info('Reporting span %s', span)


class Reporter(NullReporter):
    """Receives completed spans from Tracer and submits them out of process."""
    def __init__(self, channel, error_reporter=None, metrics=None, metrics_factory=None, **kwargs):
        from threading import Lock
        self.metrics_factory = metrics_factory or LegacyMetricsFactory(metrics or Metrics())
        self.metrics = ReporterMetrics(self.metrics_factory)
        self.error_reporter = error_reporter or ErrorReporter(Metrics())
        self.logger = kwargs.get('logger', default_logger)
        # self.agent = Agent.Client(self._channel, self)
        self.stopped = False
        self.stop_lock = Lock()
        self._process_lock = Lock()
        self._process = None
        self.channel = channel

    def set_process(self, service_name, tags, max_length):
        with self._process_lock:
            self._process = thrift.make_process(
                service_name=service_name, tags=tags, max_length=max_length,
            )

    def report_span(self, span):
        self._send(span)

    def _send(self, span):
        if not span:
            return
        span_id=span.span_id
        self.channel.set_span_name(span_id,span.operation_name)
        self.channel.start_span(span_id,parent_id=span.parent_id,tags=span.tags,context=six.iteritems(span.context))
        
    def put_log(self,span_id,level,msg,rings=[],**kwargs):
        self.channel.put_log(span_id,level,msg,rings,**kwargs)
        
    def finish_span(self,span):
        self.channel.finish_span(span.span_id)

    def close(self):
        with self.stop_lock:
            self.stopped = True
            
    def put_tag(self,span,key,value):
        self.channel.put_tag(span.span_id,key,value)
        
    def update_context(self,context):
        self.channel.update_context(six.iteritems(context))

class ReporterMetrics(object):
    def __init__(self, metrics_factory):
        self.reporter_success = \
            metrics_factory.create_counter(name='algo.spans', tags={'reported': 'true'})
        self.reporter_failure = \
            metrics_factory.create_counter(name='algo.spans', tags={'reported': 'false'})
        self.reporter_dropped = \
            metrics_factory.create_counter(name='algo.spans', tags={'dropped': 'true'})
        self.reporter_socket = \
            metrics_factory.create_counter(name='algo.spans', tags={'socket_error': 'true'})


class CompositeReporter(NullReporter):
    """Delegates reporting to one or more underlying reporters."""
    def __init__(self, *reporters):
        self.reporters = reporters

    def set_process(self, service_name, tags, max_length):
        for reporter in self.reporters:
            reporter.set_process(service_name, tags, max_length)

    def report_span(self, span):
        for reporter in self.reporters:
            reporter.report_span(span)

    def close(self):
        from threading import Lock
        lock = Lock()
        count = [0]
        future = Future()

        def on_close(_):
            with lock:
                count[0] += 1
                if count[0] == len(self.reporters):
                    future.set_result(True)

        for reporter in self.reporters:
            f = reporter.close()
            f.add_done_callback(on_close)

        return future
