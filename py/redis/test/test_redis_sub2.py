
# -*- coding: utf-8 -*-

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

    while True:
        
        r.publish(CHANNEL,msg)
        
        
        x = {"abc":"def","g": 1000 * time.time()}
        
        val = msgpack.packb(x)
        
        r.lpush("q2",val)
        
        print("msg:%s" % (msg))
        time.sleep(1)


    
if __name__ == "__main__":
    
    
    
    main()     