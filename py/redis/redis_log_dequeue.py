# -*- coding: utf-8 -*-


"""
dequeue log from redis
"""
import socket
import gevent

import redis


REDIS_MAX_CONNECTIONS = 100

class DataSub(object):
    """ class """
    
    def __init__(self):        
        """ init """
        
        rpool = redis.ConnectionPool(host='localhost', port=6379, db=0, \
                max_connections=REDIS_MAX_CONNECTIONS)

        self.rclient = redis.Redis(connection_pool=rpool) 
        

    def start(self):
        while True:
            self.process(1)
            gevent.sleep(1)           
          
    def process(self, msg):        
        """ process """
        
        list_len = self.rclient.llen("logQ")
        
        #print "len:%s" % (list_len)
        
        for seq in xrange(0, list_len):
        
            val = self.rclient.lpop("logQ")
            
            print (val)  
        

        

def main():

    """ main """
    subscriber = DataSub()
    subscriber.start()
    
    
    
if __name__ == '__main__':
    main()        