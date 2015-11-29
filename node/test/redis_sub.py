
# -*- coding: utf-8 -*-

import redis

import time

from time import strftime, localtime

r = redis.Redis(host='localhost', port=6379, db=9) 

def post(tag):
    
    val = r.hget(tag, "val")
    timestamp = r.hget(tag, "timestamp")
    print("%s, %s-%s" % (tag, timestamp,val) )
    

def main():
    
    
    #print(dir(r))
    
    p = r.pubsub()
    #r.publish('Que',"New")
    #print(dir(p))
    p.subscribe("c2")
    
    
    for message in p.listen():
        
        print message
        
        v = r.hgetall("a:b")
        
        print v
        
        """
        loop = True
            
        while loop:
            
            val = r.lpop("c1")
            x = strftime("%Y-%m-%d %H:%M:%S",localtime())
            if val != None:
                #post(val)
                print x, val
            else:
                loop = False
        """
    """
    
    while True:
        print 1
        message = p.get_message()
        
        if message:
            # do something with the message
            v = 1
            
            while v:
                
                v = r.lpop("Que")
                if v != None:
                    post(v)
                
                #print v
            
            #print message
        time.sleep(0.001) 
    """
    
if __name__ == "__main__":
    
    
    print strftime("%Y-%m-%d %H:%M:%S",localtime())
    
    
    main()     