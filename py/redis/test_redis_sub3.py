# -*- coding: utf-8 -*-

"""
test:
send data with msgpack to redis

"""

import redis

import time

import msgpack


HOST = "localhost"
PORT = 6379
DB = 5

CHANNEL = "c1"

r = redis.Redis(host='localhost', port=6379, db=4) 

def post(tag):
    
    val = r.hget(tag, "val")
    timestamp = r.hget(tag, "timestamp")
    print("%s, %s-%s" % (tag, timestamp,val) )
    

def main():
    
    
    #print(dir(r))
    
    msg = "abc"
    
    lua_code2 = """    
    local msgpack = cmsgpack.pack({time = ARGV[2],  state = KEYS[1]})
    redis.call("LPUSH", "q2", msgpack) 
    return 1
    """
    
    with open("msgpack.lua", "r") as fileh:
        lua_code = fileh.read()
        
    sha = r.script_load(lua_code)
    
    print sha

    while True:
        
        r.publish(CHANNEL,msg)
        
        """
        x = {"abc":"def","g": 1000 * time.time()}
        
        val = msgpack.packb(x)
        
        r.lpush("q2",val)
        
        print("msg:%s" % (msg))
        """
        
        h = r.evalsha(sha, 1, "dev.tag",  "abc", 1000 * time.time())

        print(h)
        time.sleep(1)


    
if __name__ == "__main__":
    
    
    
    main()     