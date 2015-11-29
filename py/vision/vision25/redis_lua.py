# -*- coding: utf-8 -*-

import redis
import time

from mako.template import Template

from conf import Conf

conf = Conf("config/ak_client.toml")


from local_logger import get_logger

logger = get_logger('redis')



class RedisLua(object):
    
    def __init__(self):
        """ init """
        self.db = redis.Redis(host=conf.redis_host, port=conf.redis_port, db=conf.redis_db)

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
        
        logger.debug(self.hsa)        
        
    def get_script(self):
        """ info """
        mytemplate = Template(filename='lua/send.lua')

        
        return mytemplate.render()
        

    def save(self, data):        
        """ save data to db """
        
        key = "y:a:c"
        
        val = "10.21"
        
        key2 = "y:a:c_st"
        
        val2 = "abc"

        val = self.db.evalsha(self.hsa,  2, key, key2,  val, val2, "abc")
        
        logger.debug(val)

  

def main():
    

    rclient = RedisLua()
    
    data = {"key","val"}
    
    rclient.save(data)

    

        
if __name__ == "__main__":
    
    main()
        