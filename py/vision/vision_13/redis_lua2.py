# -*- coding: utf-8 -*-

import os, sys

import redis
import time

from mako.template import Template

"""
from conf import Conf

conf = Conf("config/ak_client.toml")


from local_logger import get_logger

logger = get_logger('redis')
"""

from config import get_config

conf_fn = os.sep.join(
    [os.path.split(os.path.realpath(__file__))[0], "config.toml"])

conf = get_config(conf_fn)["redis"]

class RedisLua(object):
    
    def __init__(self):
        """ init """
        self.db = redis.Redis(host=conf["HOST"], port=conf["PORT"], db=conf["DB"])

        self.script_load()
        
        """
        
        # 1s, so slow?
        self.hsa = self.db.script_load(lua_code)
        
        logger.debug(self.hsa)
        
        """
        
    def script_load(self):
        """ script load """
        lua_code = self.get_script()
        
        self.hsa = self.db.script_load(lua_code)
        
        #logger.debug(self.hsa)        
        
    def get_script(self):
        """ info """
        mytemplate = Template(filename=conf["LUA_SCRIPT"])

        
        return mytemplate.render()
        

    def save(self, x,y,r):        
        """ save data to db """      
        
        key = "7"
        timestamp = 1000 * time.time()
        val = self.db.evalsha(self.hsa,  1, key, r, timestamp, x, y)
        print val
        #logger.debug(val)

  

def main():
    

    rclient = RedisLua()
    
    data = {"key","val"}
    
    rclient.save(60,70,1)

    

        
if __name__ == "__main__":
    
    main()
        