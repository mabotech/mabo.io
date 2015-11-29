
import redis

import socket

import gevent

import time


r = redis.Redis(host='localhost', port=6379, db=9) 



while True:
    
    print time.time()
    
    p = r.pubsub()
    r.publish('act',"New")
    r.publish('message',"New")
    
    gevent.sleep(0.1)