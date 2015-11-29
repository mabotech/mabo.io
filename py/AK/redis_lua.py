# -*- coding: utf-8 -*-
import os, sys

import redis
import time

import toml

import logging

from mako.template import Template

#from conf import Conf

#conf = Conf("config/ak_client.toml")

conf_fn = "config/ak_client.toml"

with open(conf_fn, "r") as conf_fh:

    cfg = toml.loads(conf_fh.read())

    conf = cfg["redis"]

#from local_logger import get_logger

#logger = get_logger('redis')

logger = logging.getLogger("redis")

class RedisLua(object):
    
    def __init__(self):
        """ init """

        
        logger.info("RedisLua init...")
        
        #self.key = 
        
        self.ttl = conf["heartbeat_ttl"]
        
        self.connect()
        
        """
        
        # 1s, so slow?
        self.hsa = self.db.script_load(lua_code)
        
        logger.debug(self.hsa)
        
        """
        
    def connect(self):
    
        try:
            
            pool = redis.ConnectionPool(host=conf["host"], port=conf["port"], db=conf["db"])
            self.db = redis.Redis(connection_pool=pool)

            self.script_load()
            
        except Exception as ex:
            logger.error(ex)
    
    def script_load(self):
        """ script load """
        
        self.lua_code = self.get_script()
        
        #print lua_code
        
        self.hsa = self.db.script_load(self.lua_code)
        
        #logger.debug(self.hsa)        
        
    def get_script(self):
        """ info """
        
        mytemplate = Template(filename=conf["lua_script"])#filename='lua/update.lua')

        return mytemplate.render()
    
    
    def check_conn(self):
        
        if self.hsa == None:
           
            logger.debug("reload script")
            
            self.hsa = self.db.script_load(self.lua_code)

    def process(self, key, value, message):
        
        try:
            
            timestamp = 1000 * time.time()
            
            rtn = self.db.evalsha(self.hsa,  1, key, value, timestamp, message, self.ttl)
            
            if rtn != "same":                
                logger.debug("%s, data: %s, rtn: %s" %(key, value, rtn))        
        
        except Exception as ex:
           logger.error(ex)

    def save(self, key, value, message):
        """ 
        save data to db 
        key: equipment_id
        """        
        
        try:
            
            #self.script_load()            
            
            self.check_conn()
            
            self.process(key, value, message)
        
        except Exception as ex:
            
            self.hsa = None
            
            #logger.warn("|%s,%s" %(key, data)) 
            
            logger.error(ex)
            
            #self.connect()
            #logger.debug(val) 

def main():
    
    import time
    
    rclient = RedisLua()
    
    
    key = "eqm011"
    
    i = 0
    
    while 1:
        
        result = "info:%s" %(i)
        rclient.save(key, i%4, result)
        i = i +1
        print i
        time.sleep(5)
        
if __name__ == "__main__":
    
    main()
        