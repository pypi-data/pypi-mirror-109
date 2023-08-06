# -*- coding: utf-8 -*-
import json
import os
import datetime
import time
from mongoengine import *
import copy
import slugify
        
def init(**kwargs):
    for k, v in kwargs.items():
        conn_params = copy.deepcopy(v)
        name = conn_params.pop('name')
        register_connection(k, name, **conn_params)
        
#默认30天过期
EXPIRED_SECONDS = 3600*24*30

COMMON_EXPIRED_INDEX = {
    'fields': ['created_at'],
    'expireAfterSeconds': EXPIRED_SECONDS
}

class Span(Document):
    start_time = DateTimeField()
    end_time = DateTimeField()
    name = StringField(max_length=200)
    parent_id = ObjectIdField()
    created_at = DateTimeField(required=True,default=datetime.datetime.utcnow)
    
    meta = {
        'db_alias':'default',
        'indexes':[
            COMMON_EXPIRED_INDEX
            ]
    }
    
    @staticmethod  
    def get_span(span_id):
        span = Span.objects(id=span_id).first()
        if span is None:
            raise RuntimeError("span id %s is not exist"%span_id)
        return span
        
    @staticmethod
    def make_mongo_dict(kwargs):
        d = {}
        for k,v in kwargs.items():
            d[slugify.slugify(k, separator='_')] = v
        return d
    

def create_new_id():
    '''
    '''
    span = Span()
    span.save()
    return str(span.id)
    
def put_tag(span_id,key,value):
    '''
    '''
    span = Span.get_span(span_id)
    names = [key]
    values = [value]
    for tag in Tag.objects(span_id=span_id):
        tag_names = tag.name
        tag_values = tag.value
        if key == tag_names[0] and value == tag_values[0]:
            return
        elif key == tag_names[0]:
            i = 2
            while True:
                loop_key = "%s.%d"%(key,i)
                if loop_key not in tag_names:
                    tag_names.append(loop_key)
                    tag_values.insert(0,value)
                    tag.name = tag_names
                    tag.value = tag_values
                    tag.save()
                    is_new_tag = False
                    return
                i+=1
    tag = Tag(span_id=span_id,name=names,value=values)
    tag.save()
    
def put_log(span_id,level,msg,rings = [],**kwargs):
    '''
    '''
    log = Log()
    Span.get_span(span_id)
    log.span_id = span_id
    log.event = level
    log.message = msg
    log.payload = Span.make_mongo_dict(kwargs)
    log.save()
    for ring in rings:
        Ring(log_id=log.id,name=ring).save()

def finish_span(span_id):
    '''
    '''
    span = Span.get_span(span_id)
    span.end_time = datetime.datetime.utcnow()
    span.save()
    
def start_span(span_id,parent_id=None,tags=[],context=None):
    '''
    '''
    span = Span.get_span(span_id)
    span.start_time = datetime.datetime.utcnow()
    if parent_id is not None:
        Span.get_span(parent_id)
        span.parent_id = parent_id
    span.save()
    for k,v in tags:
        put_tag(span_id,k,v)
        
    if context is not None:
        context['baggage'] = Span.make_mongo_dict(context['baggage'])
        Context(**context).save()
    

def set_span_name(span_id,name):
    '''
    '''
    span = Span.get_span(span_id)
    span.name = name
    span.save()

class Log(Document):
    span_id = ObjectIdField(required=True)
    event = StringField(max_length=20)
    timestamp = DateTimeField(default=datetime.datetime.utcnow)
    message = StringField()
    #这个字段要求必须定义'default'数据库别名
    payload = DictField()
    
    meta = {
        'db_alias':'default',
        'indexes':[
            {
            'fields': ['timestamp'],
            'expireAfterSeconds': EXPIRED_SECONDS
        }]
    }

class Tag(Document):
    span_id = ObjectIdField(required=True)
    name = ListField()
    value = ListField()
    created_at = DateTimeField(required=True,default=datetime.datetime.utcnow)
    
    meta = {
        'db_alias':'default',
        'indexes':[
            COMMON_EXPIRED_INDEX,
        ]
    }

class Context(Document):
    span_id = ObjectIdField(required=True)
    parent_id = ObjectIdField()
    baggage = DictField()
    flags = IntField()
    trace_id = StringField(max_length=100)
    created_at = DateTimeField(required=True,default=datetime.datetime.utcnow)
    
    meta = {
        'db_alias':'default',
        'indexes':[
            COMMON_EXPIRED_INDEX,
        ]
    }
    

class Ring(Document):
    log_id = ObjectIdField(required=True)
    name = StringField(max_length=20)
    created_at = DateTimeField(required=True,default=datetime.datetime.utcnow)
    meta = {
        'db_alias':'default',
        'indexes':[
            COMMON_EXPIRED_INDEX,
        ]
    }
    
def obj_to_dict(obj):
    return dict(obj.to_mongo())
    
def to_list_dict(objs):
    lst = []
    for obj in objs:
        lst.append(obj_to_dict(obj))
    return lst

def full_span_id(span_id):
    parent_id_list = [str(span_id)]
    parent_id = span_id
    while parent_id:
        span = Span.objects(id=parent_id).first()
        parent_id = span.parent_id
        if parent_id:
            parent_id_list.append(str(parent_id))
    parent_id_list.reverse()
    return ".".join(parent_id_list)

def get_span_info(span_id,contain_child=False,to_dict=True):
    span = Span.get_span(span_id)
    tags = Tag.objects(span_id=span_id)
    if to_dict:
        span_data = obj_to_dict(span)
        span_data['id'] = full_span_id(span_id)
        tag_list = to_list_dict(tags)
        span_data['tags'] = tag_list
        span_data['childs'] = []
        if contain_child:
            child_spans = Span.objects(parent_id=span_id)
            childs = []
            for child_span in child_spans:
                childs.append(get_span_info(child_span.id,contain_child,to_dict))
            span_data['childs'] = childs
            
        context = Context.objects(span_id=span_id).first()
        if not context:
            span_data['context'] = None
        else:
            span_data['context'] = obj_to_dict(context)
        return span_data
    return span

def get_span_logs(span_id,timestamp=None,log_ring=None):
    logs = Log.objects(span_id=span_id)
    if not logs.first():
        return []
    if log_ring is not None:
        ring_logs = []
        for log in logs:
            if Ring.objects(name=log_ring,log_id=log.id).first():
                ring_logs.append(log)
        return ring_logs
    return to_list_dict(logs)

def form_span_id(span_id):
    obj_span_id = hex(span_id).replace("0x","").replace("L","")
    return obj_span_id
    
def update_context(context):
    obj = Context.objects(span_id=context['span_id']).first()
    obj.baggage = Span.make_mongo_dict(context['baggage'])
    obj.flags = context['flags']
    obj.save()
    
def get_span_context(span_id):
    context = Context.objects(span_id=span_id).first()
    if not context:
        return None
    return obj_to_dict(context)