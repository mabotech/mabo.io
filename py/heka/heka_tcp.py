# -*- coding: utf-8 -*-

"""
tcp client(NetworkInput) for heka

[Errno 10061] No connection could be made because
    the target machine actively refused it

"""

import socket
import gevent

class SocketError(Exception):
    """ heka not started or wrong port"""
    pass

class TCPClient(object):
    """ tcp input """
    
    def __init__(self):
        """ init """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect(self):
        """ connect """
        
        try:
            self.sock.connect(('127.0.0.1', 5565))
            
            print "connected"
            
        except Exception as err:

            print dir(err)
            print err.errno
            errmsg =  err.strerror
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
    
    client = TCPClient()
    
    client.connect()

    for i in xrange(1, 33):
        
        client.send(i)   
        print "send"
        gevent.sleep(1)
    
    
    client.close()
    
if __name__ == '__main__':

    main()