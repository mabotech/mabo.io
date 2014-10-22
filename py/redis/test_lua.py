# -*- coding: utf-8 -*-

import redis

import time

# TODO： connection pool and exception handling
r = redis.Redis(host='localhost', port=6379, db=4)    

# TODO: alert
# send alert to heka( http post? ) or directly to influxdb? (timeline)

#print dir(r)
print (r.info())
def post(sha, tag, val):
    t = time.time() * 1000
    
    # eval lua script
    v = r.evalsha(sha, 1, tag, val, t)
    print(v)

def main(lua_file):
    
    
    with open(lua_file,"r") as fh:
        lua_code = fh.read()
        
    #print lua_code
    t = time.time() * 1000
    
    # eval lua script
    v = r.eval(lua_code, 1, "dev.tag","val", t)
    
    print(v)
    #time.sleep(2)
    
    
    sha =r.script_load(lua_code)
    #print (sha)
    post(sha, "dev.tag","data")
    
    
if __name__ == "__main__":
    
    lua_file = "polling.lua"
    
    main(lua_file)    
    