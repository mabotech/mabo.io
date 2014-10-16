

from twisted.internet import threads, reactor


from time import sleep,  time, strftime, localtime, mktime

import redis

import serial

from redis import Redis

import logging
import logging.handlers
import logging.config

logging.config.fileConfig('logging.ini')

log = logging.getLogger("welding")

from singleton import Singleton

class WeldingData(object):
    
    __metaclass__ = Singleton
    
    def __init__(self):
        
        self.line1 = ""
        self.data = []
        
    
    def set_data(self, val):
        
        val = val.strip();
        
        if val == "":
            pass
        elif val.count("M:")>0:
            self.line1 = val
        else:
            self.line1 = self.line1 + val
            
        if len(self.line1)>69:
            self.data.append(self.line1)
            self.line1 = ""
            if len(self.data)>0:
                return self.data.pop(0)
            else:
                return 0
        else:
            return 0




class Ser(object):
    
    def __init__(self):
        pass
        
    def readline(self):
        return "%s" % time()


def worker(ser, rc):
    
    wd = WeldingData()
  
    start = time()
    print start
    v = 0
    
    
    try:         
        v = ser.readline()   
        log.debug("[%s]" %v)    
    except Exception, e:
        log.debug( e.message )   
    
    if v!= 0:
        line = wd.set_data(v)
        log.debug("line:[%s]" %line)    
        if line == 0:
            pass
        else:
            rc.lpush('welding2', line) #'welding', 'M:W1,01,0.81,0.79,1.38,1.29,01.0,1.63,W2,2.02,2.00,2. %s' %(start))
            log.debug( "lpush: "+ line )


        
  
    delay = time() - start
  
  #print delay

    loop(delay, ser, rc)
  
def loop(delay, ser, rc ):
  
    d = 1
    reactor.callLater(d, worker, ser, rc)


def run():
    
    try:
        """
        ser = serial.Serial('COM8',baudrate=9600,
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS, #SEVENBITS,
            timeout=0)  # open first serial port

        """
        pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
        
        rc = redis.Redis(connection_pool=pool)
        
        ser = Ser()
        
        
        reactor.callLater(1, worker, ser, rc)

        reactor.run()
    except Exception, e:
        print e.message
        raise(Exception("Exception"))
    
def stop():
  reactor.stop()
  pass
  
    
if __name__ == "__main__":
    run()
