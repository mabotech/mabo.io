# -*- coding: utf-8 -*-

import redis

import time


r = redis.Redis(host='localhost', port=6379, db=4)     

def post(sha, tag, val):
    t = time.time() * 1000
    v = r.evalsha(sha, 1, tag, val, t)
    print(v)

def main(filename):
    # connection pool    
    
    with open(filename,"r") as fh:
        lua_code = fh.read()
        
    #print lua_code
    t = time.time() * 1000
    
    v = r.eval(lua_code, 1, "dev.tag","val", t)
    print(v)
    #time.sleep(2)
    
    
    sha =r.script_load(lua_code)
    #print (sha)
    post(sha, "dev.tag","data")
    
    
if __name__ == "__main__":
    
    filename = "polling.lua"
    
    main(filename)    
    