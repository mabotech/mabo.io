# -*- coding: utf-8 -*-


"""
dequeue from redis
"""

import redis


REDIS_MAX_CONNECTIONS = 100

class DataSub(object):
    """ class """
    
    def __init__(self):        
        """ init """
        
        rpool = redis.ConnectionPool(host='localhost', port=6379, db=6, \
                max_connections=REDIS_MAX_CONNECTIONS)

        self.rclient = redis.Redis(connection_pool=rpool) 
        

    def start(self):
        """ listen """

        """
        rclient.rpush("point:abc:def",'{"abd":"def"}')
        rclient.rpush("point:xyz","8")
        """

        #print(dir(rclient))
        #rclient.subscribe("point:abc")

        sub = self.rclient.pubsub()
         
        sub.subscribe('point:abc')

        for msg in sub.listen():
            
            
            
            self.process(msg)            
          
    def process(self, msg):        
        """ process """
        
        print msg
        
        list_len = self.rclient.llen("point:abc:def")
        
        print "len:%s" % (list_len)
        
        for seq in xrange(0, list_len):
        
            val = self.rclient.lpop("point:abc:def")
            
            print val  
        
        #print rclient.lrange("point:abc:def", 0, -1)
        
        print self.rclient.mget("point:abc:timestamp")[0]
        print self.rclient.mget("point:abc:pstate")[0]
        

def main():

    """ main """
    subscriber = DataSub()
    subscriber.start()
    
    
    
if __name__ == '__main__':
    main()        