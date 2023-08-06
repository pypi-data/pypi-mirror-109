#!/usr/bin/python
# coding:utf-8
from libcloud.base import singleton
from ConfigParser import ConfigParser
import os
import time

def GetDynamicImportModule(full_module_path):
    '''
        从给定字符串中动态获取模块的类
    '''
    #必须先导入模块,再获取模块里面的方法,不要直接导入类
    #如果类名是类似xx.yy.zz这样的,必须设置fromlist不为空
    module_obj = __import__(full_module_path,globals(), globals(), fromlist=['__name__'])
    return module_obj

class TraceDb:
    '''
    '''
    MONGODB_ENGINE = "backend.mongo"
    #表示该类是单例类
    #数据库引擎列表
    DRIVERS = [
       MONGODB_ENGINE,
    ]
    __metaclass__ = singleton.Singleton
    default_database_engine = None
    def __init__(self):
        self.database_engines = {}
        for db_engine_name in TraceDb.DRIVERS:
            database_engine_module = GetDynamicImportModule(db_engine_name)
            self.database_engines[db_engine_name] = database_engine_module
  
    def set_default_backend(self,default_backend,**kwargs):
        if not default_backend in self.database_engines:
            raise RuntimeError("error backend name %s"%default_backend)
        TraceDb.default_database_engine = default_backend
        self.database_engines[default_backend].init(**kwargs)

    def put_tag(self,span_id,key,value):
        self.database_engines[self.default_database_engine].put_tag(span_id,key,value)
            
    def put_log(self,span_id,level,msg,rings=[],**kwargs):
        self.database_engines[self.default_database_engine].put_log(span_id,level,msg,rings,**kwargs)

    def finish_span(self,span_id):
        self.database_engines[self.default_database_engine].finish_span(span_id)
            
    def start_span(self,span_id,parent_id=None,tags=[],context=None):
        self.database_engines[self.default_database_engine].start_span(span_id,parent_id,tags,context)

    def set_span_name(self,span_id,name):
        self.database_engines[self.default_database_engine].set_span_name(span_id,name)

    @classmethod
    def get_db(cls):
        return cls()
        
    def create_span_id(self):
        if not self.default_database_engine:
            raise RuntimeError("error!could not find default trace backend")
        return self.database_engines[self.default_database_engine].create_new_id()
        
    def form_span_id(self,span_id):
        return self.database_engines[self.default_database_engine].form_span_id(span_id)
        
    def get_span_info(self,span_id,contain_child=False):
        return self.database_engines[self.default_database_engine].get_span_info(span_id,contain_child)

    def get_span_logs(self,span_id,timestamp=None,log_ring=None):
        return self.database_engines[self.default_database_engine].get_span_logs(span_id,timestamp,log_ring)

    def get_span_context(self,span_id):
        return self.database_engines[self.default_database_engine].get_span_context(span_id)
    
    def update_context(self,context):
        self.database_engines[self.default_database_engine].update_context(context)
