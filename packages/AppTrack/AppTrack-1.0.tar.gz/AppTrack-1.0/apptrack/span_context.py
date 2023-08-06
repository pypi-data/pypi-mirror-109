from __future__ import absolute_import

import opentracing
from opentracing.ext import tags
from .constants import NOOP_SPAN_ID

class SpanContext(opentracing.SpanContext):
    __slots__ = ['span_id','span_id', 'parent_id', 'flags', '_baggage']

    def __init__(self, trace_id, span_id, parent_id, flags=None, baggage=None):
        self.trace_id = trace_id
        self.span_id = span_id
        self.parent_id = parent_id or None
        self.flags = flags or 0
        self._baggage = baggage or opentracing.SpanContext.EMPTY_BAGGAGE
        self._debug_id = 999

    @property
    def baggage(self):
        return self._baggage or opentracing.SpanContext.EMPTY_BAGGAGE

    def with_baggage_item(self, key, value):
        baggage = dict(self._baggage)
        baggage[key] = value
        return SpanContext(
            trace_id=self.trace_id,
            span_id=self.span_id,
            parent_id=self.parent_id,
            flags=self.flags,
            baggage=baggage,
        )

    # @property
    # def span_id(self):
    #     return self.span_id

    # @span_id.setter
    # def span_id(self, spanid):
    #     self.span_id = spanid


    @property
    def is_debug_id_container_only(self):
        return not self.trace_id and self._debug_id is not None

    @property
    def debug_id(self):
        return self._debug_id

    @staticmethod
    def with_debug_id(debug_id):
        ctx = SpanContext(
            trace_id=None, span_id=None, parent_id=None, flags=None
        )
        ctx._debug_id = debug_id
        return ctx

    def __str__(self):
        return str(self.span_id) + "<" + str(self._baggage) + ">"

    def __repr__(self):
        return self.__str__()
        
    def iteritems(self):
        return {'trace_id':str(self.trace_id),'span_id':self.span_id,'parent_id':self.parent_id,'flags':self.flags,'baggage':self._baggage}
