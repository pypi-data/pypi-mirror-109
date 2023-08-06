from __future__ import absolute_import
from __future__ import division

from builtins import str
from builtins import object

import six


class MetricsFactory(object):
    """Generates new metrics."""

    def _noop(self, *args):
        pass

    def create_counter(self, name, tags=None):
        return self._noop

    def create_timer(self, name, tags=None):
        return self._noop

    def create_gauge(self, name, tags=None):
        return self._noop


class LegacyMetricsFactory(MetricsFactory):
    """A MetricsFactory adapter for legacy Metrics class."""

    def __init__(self, metrics):
        self._metrics = metrics

    def create_counter(self, name, tags=None):
        key = self._get_key(name, tags)

        def increment(value):
            return self._metrics.count(key, value)
        return increment

    def create_timer(self, name, tags=None):
        key = self._get_key(name, tags)

        def record(value):
            # Convert microseconds to milliseconds for legacy
            return self._metrics.timing(key, value / 1000.0)
        return record

    def create_gauge(self, name, tags=None):
        key = self._get_key(name, tags)

        def update(value):
            return self._metrics.gauge(key, value)
        return update

    def _get_key(self, name, tags=None):
        if not tags:
            return name
        key = name
        for k in sorted(six.iterkeys(tags)):
            key = key + '.' + str(k) + '_' + str(tags[k])
        return key


class Metrics(object):
    """
    Provides an abstraction of metrics reporting framework.
    This Class has been deprecated, please use MetricsFactory
    instead.
    """

    def __init__(self, count=None, gauge=None, timing=None):

        self._count = count
        self._gauge = gauge
        self._timing = timing
        if not callable(self._count):
            self._count = None
        if not callable(self._gauge):
            self._gauge = None
        if not callable(self._timing):
            self._timing = None

    def count(self, key, value):
        if self._count:
            self._count(key, value)

    def timing(self, key, value):
        if self._timing:
            self._timing(key, value)

    def gauge(self, key, value):
        if self._gauge:
            self._gauge(key, value)
