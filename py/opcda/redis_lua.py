# -*- coding: utf-8 -*-
import os, sys

import redis
import time

import toml

import logging

from mako.template import Template

import traceback

#from conf import Conf

#conf = Conf("config/ak_client.toml")

conf_fn = "config/opc_monitor.toml"

with open(conf_fn, "r") as conf_fh:

    cfg = toml.loads(conf_fh.read())

    conf = cfg["redis"]

#from local_logger import get_logger

#logger = get_logger('redis')

logger = logging.getLogger("redis")

logger.debug(conf)

class RedisLua(object):
    
    def __init__(self):
        """ init """

        
        logger.info("RedisLua init...")
        
        self.connect()
        
        """
        
        # 1s, so slow?
        self.hsa = self.db.script_load(lua_code)
        
        logger.debug(self.hsa)
        
        """
        
    def connect(self):
        
        logger.debug("connect...............")
        
        try:           
            
            self.db = redis.Redis(host=conf["host"], port=conf["port"], db=conf["db"])

            self.script_load()
            
        except Exception as ex:
            logger.error(ex)
            logger.debug(traceback.format_exc())
    
    def script_load(self):
        """ script load """
        
        lua_code = self.get_script()
        
        #print lua_code
        
        self.hsa = self.db.script_load(lua_code)
        
        #logger.debug(self.hsa)        
        
    def get_script(self):
        """ info """
        
        mytemplate = Template(filename=conf["lua_script"])#filename='lua/update.lua')

        return mytemplate.render()
        

    def save(self, key, result, data, ttl = 60):        
        """ 
        save data to db 
        key: equipment_id
        """
        print "====="
        logger.debug("key:%s, data:%s, ttl:%s" %(key, data, ttl))
        
        rtn = ""
        try:

            timestamp = 1000 * time.time()
            
            rtn = self.db.evalsha(self.hsa,  1, key, data, timestamp, result, ttl)
            if rtn != "same":
                logger.debug("%s, data: %s, rtn: %s" %(key, data, rtn)) 
        
        except Exception as ex:
            logger.warn("|%s,%s,%s" %(key, data, rtn)) 
            logger.error(ex)
            self.connect()
            #logger.debug(val)

  

def main():
    

    rclient = RedisLua()
    
    data = {"key","val"}
    
    key = "eqm002"
    data = 1
    
    rclient.save(key, "", data)
    
        
if __name__ == "__main__":
    
    main()
        