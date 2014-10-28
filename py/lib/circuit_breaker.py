# -*- coding: utf-8 -*-

"""

circuit status:

- connected : C
- broken : B
- reconnecting : R
- fitial : F

connection pool

"""

import threading

import redis


# Circuit Breaker State in redis
    
class CircuitBreaker(object):
    
    """  Circuit Breaker Pattern """
    
    def __init__(self):
        
        self._fail_max = 0
        
        self._lock = threading.RLock()   
        #acquire()
        #release()

        pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
        self.redisc = redis.Redis(connection_pool=pool)


    def restart_req(self):
        """ send restart request to job queue"""
        
        with self._lock:
        
            pass
        
    
    def check_redis(self):
        """
        check if redis is available
        """
        
        
        pass

    def register(self, status):
        """ register connection"""
        pass

    def check_status(self):
        """ check connection(circuit) status"""       
        
        pass
            
           
    def connect(self):
        """ connect """
        self.register('C')

    def reconnect(self):
        """ reconnect """
        self.register('R')
        
        self.register('C')
        
        self.register('F')
        

    def read(self):
        
        """ read """
        
        status = self.check_status()
        
        if status == 'C':
            pass


    def write(self):
        """ write """
        pass
    
    
    
def main():
    """ main """
    pass