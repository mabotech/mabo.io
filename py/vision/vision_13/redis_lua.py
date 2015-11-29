# -*- coding: utf-8 -*-
import os, sys

import redis
import time

import toml

import logging

from mako.template import Template

#from conf import Conf

#conf = Conf("config/ak_client.toml")

conf_fn = "config/vision.toml"

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

        logger.debug(conf)
        
        self.connect()
        
        """
        
        # 1s, so slow?
        self.hsa = self.db.script_load(lua_code)
        
        logger.debug(self.hsa)
        
        """
        
    def connect(self):
    
        try:
            self.db = redis.Redis(host=conf["host"], port=conf["port"], db=conf["db"])

            self.script_load()
            
        except Exception as ex:
            logger.error(ex)
            pass
    
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
        

    def save(self, key, result, data):        
        """ 
        save data to db 
        key: equipment_id
        """
        info = "%s, %s, %s" %(key, result, data)
        logger.debug(info)
        val = None
        try:

            timestamp = 1000 * time.time()
            
            val = self.db.evalsha(self.hsa, 1, key, data, timestamp, result)

            logger.debug(val)
            
            if val != "same":
                logger.debug("%s, data: %s, rtn: %s" %(key, data, val)) 
        
        except Exception as ex:
            logger.warn("|%s,%s,%s" %(key, data, val)) 
            logger.error(ex)
            self.connect()
            #logger.debug(val)

  

def main():
    

    rclient = RedisLua()
    
    data = {"key","val"}
    
    key = ""

    result = ""
    
    rclient.save(key, result, data)
    
        
if __name__ == "__main__":
    
    main()
        
