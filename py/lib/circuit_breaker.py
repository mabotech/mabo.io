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
        """   """
        
        self.broken = False
        self.instance_name = "name"
        self._fail_max = 0
        
        self._lock = threading.RLock()   
        #acquire()
        #release()

        pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
        self.redisc = redis.Redis(connection_pool=pool)

    def reconnect_redis():
        """ reconnect redis"""
        pass
        
    def restart_req(self):
        """ send restart request to job queue"""
        
        with self._lock:        
            pass
        
    
    def test_redis(self):
        """ test if redis is available """        
        
        return True

    def register(self, status):
        """ register connection """
        
        pass

    def check_status(self):
        """ check connection(circuit) status """
        
        if self.test_redis() = True:
            pass
        else:
            reconnect_redis()
            pass
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
            self.broken = False
            pass
            
    def write(self):
        """ write """
        
        pass
        
    
def main():
    """ main """
    pass