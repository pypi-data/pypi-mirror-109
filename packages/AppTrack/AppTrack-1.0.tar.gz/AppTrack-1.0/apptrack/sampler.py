from __future__ import absolute_import
from __future__ import division
from builtins import object
import json
import logging
import random
import six

from threading import Lock
from .constants import (
    MAX_ID_BITS,
    DEFAULT_SAMPLING_INTERVAL,
    SAMPLER_TYPE_CONST,
    SAMPLER_TYPE_PROBABILISTIC,
    SAMPLER_TYPE_RATE_LIMITING,
    SAMPLER_TYPE_LOWER_BOUND,
)
from .metrics import Metrics, LegacyMetricsFactory

default_logger = logging.getLogger(__name__)

SAMPLER_TYPE_TAG_KEY = 'sampler.type'
SAMPLER_PARAM_TAG_KEY = 'sampler.param'
DEFAULT_SAMPLING_PROBABILITY = 0.001
DEFAULT_LOWER_BOUND = 1.0 / (10.0 * 60.0)  # sample once every 10 minutes
DEFAULT_MAX_OPERATIONS = 2000

STRATEGIES_STR = 'perOperationStrategies'
OPERATION_STR = 'operation'
DEFAULT_LOWER_BOUND_STR = 'defaultLowerBoundTracesPerSecond'
PROBABILISTIC_SAMPLING_STR = 'probabilisticSampling'
SAMPLING_RATE_STR = 'samplingRate'
DEFAULT_SAMPLING_PROBABILITY_STR = 'defaultSamplingProbability'
OPERATION_SAMPLING_STR = 'operationSampling'
MAX_TRACES_PER_SECOND_STR = 'maxTracesPerSecond'
RATE_LIMITING_SAMPLING_STR = 'rateLimitingSampling'
STRATEGY_TYPE_STR = 'strategyType'


class Sampler(object):
    """
    Sampler is responsible for deciding if a particular span should be
    "sampled", i.e. recorded in permanent storage.
    """

    def __init__(self, tags=None):
        self._tags = tags

    def is_sampled(self, trace_id, operation=''):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)


class ConstSampler(Sampler):
    """ConstSampler always returns the same decision."""

    def __init__(self, decision):
        super(ConstSampler, self).__init__(
            tags={
                SAMPLER_TYPE_TAG_KEY: SAMPLER_TYPE_CONST,
                SAMPLER_PARAM_TAG_KEY: decision,
            }
        )
        self.decision = decision

    def is_sampled(self, trace_id, operation=''):
        return self.decision, self._tags

    def close(self):
        pass

    def __str__(self):
        return 'ConstSampler(%s)' % self.decision


class ProbabilisticSampler(Sampler):
    """
    A sampler that randomly samples a certain percentage of traces specified
    by the samplingRate, in the range between 0.0 and 1.0.

    It relies on the fact that new trace IDs are 64bit random numbers
    themselves, thus making the sampling decision without generating a new
    random number, but simply calculating if traceID < (samplingRate * 2^64).
    Note that we actually ignore (zero out) the most significant bit.
    """

    def __init__(self, rate):
        super(ProbabilisticSampler, self).__init__(
            tags={
                SAMPLER_TYPE_TAG_KEY: SAMPLER_TYPE_PROBABILISTIC,
                SAMPLER_PARAM_TAG_KEY: rate,
            }
        )
        assert 0.0 <= rate <= 1.0, 'Sampling rate must be between 0.0 and 1.0'
        self.rate = rate
        self.max_number = 1 << MAX_ID_BITS
        self.boundary = rate * self.max_number

    def is_sampled(self, trace_id, operation=''):
        return trace_id < self.boundary, self._tags

    def close(self):
        pass

    def __str__(self):
        return 'ProbabilisticSampler(%s)' % self.rate


class RateLimitingSampler(Sampler):
    """
    Samples at most max_traces_per_second. The distribution of sampled
    traces follows burstiness of the service, i.e. a service with uniformly
    distributed requests will have those requests sampled uniformly as well,
    but if requests are bursty, especially sub-second, then a number of
    sequential requests can be sampled each second.
    """

    def __init__(self, max_traces_per_second=10):
        super(RateLimitingSampler, self).__init__(
            tags={
                SAMPLER_TYPE_TAG_KEY: SAMPLER_TYPE_RATE_LIMITING,
                SAMPLER_PARAM_TAG_KEY: max_traces_per_second,
            }
        )
        assert max_traces_per_second >= 0, \
            'max_traces_per_second must not be negative'
        self.traces_per_second = max_traces_per_second
        self.rate_limiter = RateLimiter(
            credits_per_second=self.traces_per_second,
            max_balance=self.traces_per_second if self.traces_per_second > 1.0 else 1.0
        )

    def is_sampled(self, trace_id, operation=''):
        return self.rate_limiter.check_credit(1.0), self._tags

    def close(self):
        pass

    def __eq__(self, other):
        """The last_tick and balance fields can be different"""
        if not isinstance(other, self.__class__):
            return False
        d1 = dict(self.rate_limiter.__dict__)
        d2 = dict(other.rate_limiter.__dict__)
        d1['balance'] = d2['balance']
        d1['last_tick'] = d2['last_tick']
        return d1 == d2

    def __str__(self):
        return 'RateLimitingSampler(%s)' % self.traces_per_second


class GuaranteedThroughputProbabilisticSampler(Sampler):
    def __init__(self, operation, lower_bound, rate):
        super(GuaranteedThroughputProbabilisticSampler, self).__init__(
            tags={
                SAMPLER_TYPE_TAG_KEY: SAMPLER_TYPE_LOWER_BOUND,
                SAMPLER_PARAM_TAG_KEY: rate,
            }
        )
        self.probabilistic_sampler = ProbabilisticSampler(rate)
        self.lower_bound_sampler = RateLimitingSampler(lower_bound)
        self.operation = operation
        self.rate = rate
        self.lower_bound = lower_bound

    def is_sampled(self, trace_id, operation=''):
        sampled, tags = \
            self.probabilistic_sampler.is_sampled(trace_id, operation)
        if sampled:
            self.lower_bound_sampler.is_sampled(trace_id, operation)
            return True, tags
        sampled, _ = self.lower_bound_sampler.is_sampled(trace_id, operation)
        return sampled, self._tags

    def close(self):
        self.probabilistic_sampler.close()
        self.lower_bound_sampler.close()

    def update(self, lower_bound, rate):
        # (NB) This function should only be called while holding a Write lock.
        if self.rate != rate:
            self.probabilistic_sampler = ProbabilisticSampler(rate)
            self.rate = rate
            self._tags = {
                SAMPLER_TYPE_TAG_KEY: SAMPLER_TYPE_LOWER_BOUND,
                SAMPLER_PARAM_TAG_KEY: rate,
            }
        if self.lower_bound != lower_bound:
            self.lower_bound_sampler = RateLimitingSampler(lower_bound)
            self.lower_bound = lower_bound

    def __str__(self):
        return 'GuaranteedThroughputProbabilisticSampler(%s, %f, %f)' \
               % (self.operation, self.rate, self.lower_bound)


def get_sampling_probability(strategy=None):
    if not strategy:
        return DEFAULT_SAMPLING_PROBABILITY
    probability_strategy = strategy.get(PROBABILISTIC_SAMPLING_STR)
    if not probability_strategy:
        return DEFAULT_SAMPLING_PROBABILITY
    return probability_strategy.get(SAMPLING_RATE_STR, DEFAULT_SAMPLING_PROBABILITY)


def get_rate_limit(strategy=None):
    if not strategy:
        return DEFAULT_LOWER_BOUND
    rate_limit_strategy = strategy.get(RATE_LIMITING_SAMPLING_STR)
    if not rate_limit_strategy:
        return DEFAULT_LOWER_BOUND
    return rate_limit_strategy.get(MAX_TRACES_PER_SECOND_STR, DEFAULT_LOWER_BOUND)
