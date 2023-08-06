from __future__ import absolute_import

from builtins import object
import logging
import os
import threading

import opentracing
from opentracing.propagation import Format

from . import db

from . import Tracer

from .reporter import (
    Reporter,
    CompositeReporter,
    LoggingReporter,
)

from .sampler import (
    ConstSampler,
    ProbabilisticSampler,
    RateLimitingSampler,
)

from .constants import (
    DEFAULT_SAMPLING_INTERVAL,
    DEFAULT_FLUSH_INTERVAL,
    SAMPLER_TYPE_CONST,
    SAMPLER_TYPE_PROBABILISTIC,
    SAMPLER_TYPE_RATE_LIMITING,
    TRACE_ID_HEADER,
    BAGGAGE_HEADER_PREFIX,
    DEBUG_ID_HEADER_KEY,
    MAX_TAG_VALUE_LENGTH,
    DATABASE_HOST_KEY,
    DATABASE_PORT_KEY,
)
from .utils import get_boolean
from .metrics import LegacyMetricsFactory, MetricsFactory, Metrics

DEFAULT_REPORTING_HOST = 'localhost'
DEFAULT_REPORTING_PORT = 1206
DEFAULT_SAMPLING_PORT = 5778
LOCAL_AGENT_DEFAULT_ENABLED = True

DEFAULT_DATABASE_HOST = 'localhost'
DEFAULT_DATABASE_PORT = 1206

logger = logging.getLogger(__name__)
logging.basicConfig()

class Config(object):

    _initialized = False
    _initialized_lock = threading.Lock()

    def __init__(self, config, service_name=None, metrics=None, metrics_factory=None):
        self.config = config

        if get_boolean(self.config.get('metrics', True), True):
            self._metrics_factory = metrics_factory or LegacyMetricsFactory(metrics or Metrics())
        else:
            self._metrics_factory = MetricsFactory()

        self._service_name = config.get('service_name', service_name)
        if self._service_name is None:
            raise ValueError('service_name required in the config or param')

    @property
    def service_name(self):
        return self._service_name


    def local_agent_group(self):
        return self.config.get('local_agent', None)


    @property
    def local_agent_reporting_port(self):
        # noinspection PyBroadException
        try:
            return int(self.local_agent_group()['reporting_port'])
        except:
            return DEFAULT_REPORTING_PORT

    @property
    def local_agent_reporting_host(self):
        # noinspection PyBroadException
        try:
            return self.local_agent_group()['reporting_host']
        except:
            return DEFAULT_REPORTING_HOST

    @property
    def logging(self):
        return get_boolean(self.config.get('logging', False), False)

    @property
    def trace_id_header(self):
        """
        :return: Returns the name of the HTTP header used to encode trace ID
        """
        return self.config.get('trace_id_header', TRACE_ID_HEADER)

    @property
    def baggage_header_prefix(self):
        """
        :return: Returns the prefix for HTTP headers used to record baggage
        items
        """
        return self.config.get('baggage_header_prefix', BAGGAGE_HEADER_PREFIX)

    @property
    def debug_id_header(self):
        """
        :return: Returns the name of HTTP header or a TextMap carrier key
        which, if found in the carrier, forces the trace to be sampled as
        "debug" trace. The value of the header is recorded as the tag on the
        root span, so that the trace can be found in the UI using this value
        as a correlation ID.
        """
        return self.config.get('debug_id_header', DEBUG_ID_HEADER_KEY)


    @property
    def enabled(self):
        return get_boolean(self.config.get('enabled', True), True)


    @property
    def max_tag_value_length(self):
        """
        :return: Returns max allowed tag value length. Longer values will
        be truncated.
        """
        return self.config.get('max_tag_value_length', MAX_TAG_VALUE_LENGTH)


    @property
    def sampler(self):
        sampler_config = self.config.get('sampler', {})
        sampler_type = sampler_config.get('type', None)
        sampler_param = sampler_config.get('param', None)
        if not sampler_type:
            return None
        elif sampler_type == SAMPLER_TYPE_CONST:
            return ConstSampler(decision=get_boolean(sampler_param, False))
        elif sampler_type == SAMPLER_TYPE_PROBABILISTIC:
            return ProbabilisticSampler(rate=float(sampler_param))
        elif sampler_type in [SAMPLER_TYPE_RATE_LIMITING, 'rate_limiting']:
            return RateLimitingSampler(
                max_traces_per_second=float(sampler_param))
        else:
            return ConstSampler(decision=get_boolean(sampler_param, False))

        raise ValueError('Unknown sampler type %s' % sampler_type)


    @property
    def database_addr(self):
        return self.config.get(DATABASE_HOST_KEY,DEFAULT_DATABASE_HOST)


    @property
    def database_port(self):
        return self.config.get(DATABASE_PORT_KEY,DEFAULT_DATABASE_PORT)


    @property
    def max_operations(self):
        return self.config.get('max_operations', None)

    @property
    def tags(self):
        """
        :return: Returns tags from config and `ALGO_TAGS` environment variable
        to use as process-wide tracer tags
        """
        tags = self.config.get('tags', {})
        env_tags = os.environ.get('APPTRACK_TAGS', '')
        if env_tags:
            for kv in env_tags.split(','):
                key, value = kv.split('=')
                tags[key.strip()] = value.strip()
        return tags


    @staticmethod
    def initialized():
        with Config._initialized_lock:
            return Config._initialized

    def initialize_tracer(self, io_loop=None,default_backend=None,**kwargs):
        """
        Initialize Algo Tracer based on the passed `algo_client.Config`.
        Save it to `opentracing.tracer` global variable.
        Only the first call to this method has any effect.
        """
        if opentracing.is_global_tracer_registered():
            return opentracing.global_tracer()
            
        with Config._initialized_lock:
            if Config._initialized:
                logger.warn('apptrack tracer already initialized, skipping')
                return
            Config._initialized = True

        channel = self._create_agent_channel()
        channel.set_default_backend(default_backend,**kwargs)

        sampler = self.sampler
        logger.info('Using sampler %s', sampler)

        reporter = Reporter(channel=channel, metrics_factory=self._metrics_factory)

        if self.logging:
            reporter = CompositeReporter(reporter, LoggingReporter(logger))

        tracer = self.create_tracer(
            reporter=reporter,
            sampler=sampler,
        )

        self._initialize_global_tracer(tracer=tracer)
        return tracer

    def create_tracer(self, reporter, sampler):
        return Tracer(
            service_name=self.service_name,
            reporter=reporter,
            sampler=sampler,
            trace_id_header=self.trace_id_header,
            baggage_header_prefix=self.baggage_header_prefix,
            debug_id_header=self.debug_id_header,
            tags=self.tags,
            max_tag_value_length=self.max_tag_value_length,
        )

    def _initialize_global_tracer(self, tracer):
        opentracing.set_global_tracer(tracer)
        logger.info('opentracing.tracer initialized to %s[app_name=%s]',
                    tracer, self.service_name)

    def _create_agent_channel(self, io_loop=None):
        return db.TraceDb.get_db()       




