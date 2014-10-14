
# -*- coding: utf-8 -*-

import redis

import time

r = redis.Redis(host='localhost', port=6379, db=4) 

def post(tag):
    
    val = r.hget(tag, "val")
    
    print(val)
    

def main():
    
    
    #print(dir(r))
    
    p = r.pubsub()
    #r.publish('Que',"New")
    #print(dir(p))
    p.subscribe("Que")
    
    
    for message in p.listen():
        
        #print message
        
        loop = True
            
        while loop:
            
            val = r.lpop("Que")
            
            if val != None:
                post(val)
            else:
                loop = False
        
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
    
    
    
    main()     