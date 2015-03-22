# -*- coding: utf-8 -*-

"""
enqueue to redis

"""

import time

import redis

REDIS_MAX_CONNECTIONS = 100

class DataPub(object):
    
    """ class """
    
    def __init__(self):
        """ init """
        
        rpool = redis.ConnectionPool(host='localhost', port=6379, db=8, \
                    max_connections=REDIS_MAX_CONNECTIONS)

        self.rclient = redis.Redis(connection_pool=rpool) 

    def heartbeat(self):
        pass
        
    def enqueue(self):
        """ enqueue """
        t = time.time()

        self.rclient.rpush("point:abc:def",t)

        self.rclient.rpush("point:abc",t)

        d = {"point:abc:timestamp":t}

        self.rclient.mset(d)

        self.rclient.mset({"point:abc:pstate":t})
        
        self.rclient.mset({"point:abc:heartbeat":t})
        
        self.rclient.mset({"point:abc:client":"F123-10065"})

        self.rclient.publish("point:abc","ok")

def main():
    
    publisher = DataPub()
    
    publisher.enqueue()
    

    
if __name__ == '__main__':
    main()