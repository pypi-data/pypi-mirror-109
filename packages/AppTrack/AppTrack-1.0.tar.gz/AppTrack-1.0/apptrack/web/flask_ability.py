# -*- coding: utf-8 -*-
import json
from flask import request, jsonify, Flask, g
from collections import OrderedDict
import opentracing

def lect_request(request, args=None):
    """
    解析请求参数
    request传入参数的header中带有token的字段
    :param request:
    :param args:
    :return:
    """
    if request.form:
        lect = request.form.to_dict()
    elif request.json:
        lect = copy.deepcopy(request.json)
    else:
        try:
            lect = json.loads(request.data)
        except:
            lect = {}
    if request.args:
        tmp = request.args.to_dict()
        lect.update(tmp)

    if isinstance(args, str):
        v = lect.get(args, '')
        return v.encode('utf-8', 'ignore')
    elif isinstance(args, list):
        r = []
        for k in args:
            v = lect.get(k, '')
            r.append(v)
        return r
    elif isinstance(args, dict) or isinstance(args, OrderedDict):
        r = OrderedDict()
        for k in args:
            v = lect.get(k, args.get(k, ''))
            r[k] = v

        if isinstance(args, OrderedDict):
            return r.values()
        else:
            return dict(r)
    return lect

def create_span():
    path = request.path
    lect = lect_request(request)
    context = opentracing.global_tracer().extract(opentracing.Format.HTTP_HEADERS,request.headers)
    if context is not None:
        g.span = opentracing.global_tracer().start_span(path, opentracing.child_of(context))
    else:
        g.span = opentracing.global_tracer().start_span(path)
    g.span.set_baggage(lect)
    g.span.set_tag('path',request.path).set_tag('method',request.method).set_tag('remote_addr',request.remote_addr)
    g.span.set_tag('url',request.url).set_tag('protocol',request.scheme)

def finish_span(response):
    g.span.set_tag('status_code',response.status_code)
    #为每个请求注入span id
    data = response.get_json()
    data['span_id'] = g.span.span_id
    error = False
    if response.status_code == 500:
        error = True
    g.span.finish(error=error)
    response.set_data(json.dumps(data))
    return response
    
def init_interceptor(app):
    app.before_request(create_span)
    app.after_request(finish_span)
    