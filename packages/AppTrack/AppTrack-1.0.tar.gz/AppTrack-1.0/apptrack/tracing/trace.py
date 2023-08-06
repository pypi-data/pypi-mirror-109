# -*- coding: utf-8 -*-
#from base import BaseRequest
import os
import logging
import apptrack
from apptrack.constants import SAMPLER_TYPE_CONST
import opentracing

TRACE_DB_NAME = 'traces'

MONGO_BACKEND = "backend.mongo"
DEFAULT_BACKEND = "default"

def init_tracer(service_name,backend=DEFAULT_BACKEND):
    trace_config = apptrack.Config({
        'sampler':{'type':SAMPLER_TYPE_CONST,'param':True}},
        service_name,
    )
    if backend == MONGO_BACKEND:
        tracer = trace_config.initialize_tracer(default_backend=MONGO_BACKEND,**{
            'default': {
                'name': TRACE_DB_NAME,
                'host': '127.0.0.1',
                'port': 27017,
            },
        })
    elif backend == DEFAULT_BACKEND:
        assert(False)
    else:
        raise RuntimeError("error backend %s"%backend)
    opentracing.set_global_tracer(tracer)


