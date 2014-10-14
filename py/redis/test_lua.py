# -*- coding: utf-8 -*-

import redis

import time

def main(filename):
    # connection pool
    r = redis.Redis(host='localhost', port=6379, db=4)     
    
    with open(filename,"r") as fh:
        lua_code = fh.read()
        
    #print lua_code
    t = time.time() * 1000
    
    v = r.eval(lua_code, 1, "tag.x","abc", t)
    print(v)
    #time.sleep(2)
    v = r.eval(lua_code, 1, "tag.x","ok", t)
    print(v)
    
if __name__ == "__main__":
    
    filename = "polling.lua"
    
    main(filename)    
    