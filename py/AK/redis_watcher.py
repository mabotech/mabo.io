# -*- coding: utf-8 -*-


"""
dequeue from redis
"""

import socket
import gevent

import redis


REDIS_MAX_CONNECTIONS = 100

class RedisWatcher(object):
    """ class """
    
    def __init__(self):        
        """ init """
        
        rpool = redis.ConnectionPool(host='localhost', port=6379, db=5, \
                max_connections=REDIS_MAX_CONNECTIONS)

        self.db = redis.Redis(connection_pool=rpool) 
        
        
    def send(self):
        
        """ 
        
        send to heka
        or send to influxdb
        
        if send failed push data to redis again?
        
        """
        

    def start(self):
        
        while 1:
            
            """
            v = self.db.lpop("c1")
            
            if v != None:
                print(v)
            else:
                print("no data")
            
            """
            
            gevent.sleep(1)
          

        

def main():

    """ main """
    watcher = RedisWatcher()
    watcher.start()
    
    
    
if __name__ == '__main__':
    main()        