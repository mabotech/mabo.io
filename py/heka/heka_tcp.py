# -*- coding: utf-8 -*-

"""
heka tcp client(NetworkInput)

python - hekad

- can't connect to hekad/hekad not start:
[Errno 10061] No connection could be made because
    the target machine actively refused it

save data in redis/logfile when no connection?

"""
import logbook

import socket
import gevent

import toml

logbook.set_datetime_format("local")

logger = logbook.Logger('hekac')

#log = logbook.FileHandler('heka_tcp.log')

log = logbook.RotatingFileHandler('heka_tcp.log', max_size=1024, backup_count=5)

log.push_application()


def get_conf(conf_fn):
    
    """ get configuration from .toml"""
    
    
    with open(conf_fn) as conf_fh:
        
        conf = toml.loads(conf_fh.read())
        
        #print(config)
        return conf
        
        
        
class SocketError(Exception):
    """ heka not started or wrong port"""
    pass
    


class HekaTCPClient(object):
    """ tcp input """
    
    def __init__(self):
        """ init """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.conf = get_conf("hekac.toml")
        
        self.host = self.conf["client"]["host"]
        self.port = self.conf["client"]["port"]
        
    def connect(self):
        """ connect """
        
        try:
            

            
            self.sock.connect((self.host, self.port))
            
            print "connected"
            
        except Exception as err:

            print dir(err)
            
            print err.errno
            
            errmsg =  "target: %s:%s, %s" % (self.host, self.port, err.strerror)
            
            logger.error(errmsg*3)
            
            raise SocketError(errmsg)

    def send(self, i):      
        """ send """
        
        message = "%s" % (i) #'go|cc\nd,ds\nd d,vv|od'
        
        messlen = self.sock.send(message*5)#, 0
        
        print messlen

        #print received

        #print sock.recv(1024)
    
    def close(self):
        """ close socket """
        
        self.sock.close()

def main():
    
    """ main """
    #time.sleep(1)
    
    logger.debug("heka tcp")
    
    client = HekaTCPClient()
    
    client.connect()

    for i in xrange(1, 3333):
        
        client.send(i)   
        logger.debug("send")
        logger.debug("=="*20)
        logger.info(i)
        
        gevent.sleep(1)
    
    
    client.close()
    
if __name__ == '__main__':

    main()