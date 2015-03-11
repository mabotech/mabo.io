# -*- coding: utf-8 -*-

""" 
AK Client 
AK Protocol

"""

import socket
import struct

import traceback

#import aklib

import gevent

from conf import Conf

conf = Conf("ak_client.toml")

from local_logger import get_logger

logger = get_logger('AKCli')

#log = logbook.FileHandler('heka_tcp.log')

import aklib

# static
STX = 0x02
ETX = 0x03
BLANK = 0x20
K = ord('K')   

# socket status

UNKNOWN = 0
SOCKET_OPENED = 1
SOCKET_CONNECTED = 2
SOCKET_CLOSED = 3


class AKClient(object):
    
    """ 
    AK Protocol Test, 
    
    * BEP/Burke E. Porter
    * MAHA
    * Horiba
    * AVL    
    """

    def __init__(self):        
        """ init """
        
        
        
        self.connected = 0
        self.closed = 0
        
        self.socket_status = UNKNOWN
        
        self.i = 0
        
        self.retry = 0   

        self.last_errno = 0
        
        self.open()
        
    
    def open(self):
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_status = SOCKET_OPENED
        
    def connect(self):        
        """ connect """
        try:
            
            logger.debug("connecting...")
            
            if self.closed == 0:
                
                self.sock.connect((conf.host, conf.port))

            else:
                # open a socket
                #self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
                self.open()
                self.sock.connect((conf.host, conf.port))
                
                self.closed = 0
            
            self.connected = 1
            self.socket_status = SOCKET_CONNECTED
            
        except Exception as ex:
            
            #logger.debug(traceback.format_exc())
            
            if self.last_errno == ex.errno:
                logger.debug("[Errno %s]" %(ex.errno))
            else:
                self.last_errno = ex.errno
                logger.debug(ex)               
                
            self.connected = 0
            #self.sock = None

    def close(self):        
        """ close socket """
        
        try:
            
            self.sock.close()
            self.closed = 1
            self.socket_status = SOCKET_CLOSED
            
        except Exception as ex:
            
            logger.debug(ex)
            logger.debug("closed?")
            
    def pack(self, cmd):        
        """ pack """        
        #cmd = "AVFI"      
        clen = len(cmd)
        
        # AK Command telegram
        fmt = "!2b%ds5b" % (clen)
        #print fmt
        buf = struct.pack(fmt, STX, BLANK, cmd, BLANK, K, conf.channel_number, BLANK, ETX)
        logger.debug(buf)
        return buf
    
    def send(self, buf):        
        """ send """
        try:
            self.sock.sendall(buf)
        except Exception as ex:
            logger.debug(ex)
            raise(Exception(ex))
            
    def parse(self, val):
        """ process received data """
        logger.debug(val)
        try:
            
            func =  getattr(aklib, val[2].lower())
            data = val[6]
            info = func(data)
            
        except Exception as ex:
            logger.debug(ex)
            #'module' object has no attribute 'abcd'
            raise Exception("no parser")         
        
        
    def recv(self):        
        """ recv """
        
        try:
            data = self.sock.recv(1024)
        except Exception as ex:
            logger.debug(ex)
            raise(Exception(ex))
        
        logger.debug( data )   
        #print "data:%s:" %(data)
        
        #return 0
        
        dlen = len(data) - conf.non_data_len#10
        
        if dlen < 0:
            #raise Exception("struct error")
            fmt = "!2b4s3b"
            
             
        else:
            # AK Response telegram
            fmt = "!2b4s3b%ds1b" % (dlen)
        
        try:
            val = struct.unpack(fmt, data)
            logger.debug(val)
            self.parse(val)
            
        except Exception as ex:
            #logger.debug(ex)
            logger.error(ex)
        
        #print(val)
        
        #msg = "Cmd:[%s],Error:[%s], Data:[%s]" % (val[2], val[4], val[6])
        
        #logger.debug ( msg )          
            
        #cmd = val[2]
        
        #return cmd
        #print val
        #print repr(val)       
    

            
            
    def get_data(self, cmd):
        
        try:               
            
            buf = self.pack(cmd)            
            # send 
            self.send(buf)
            # receive [block]
            self.recv()
            
        except Exception as ex:
            logger.debug("182")
            logger.debug(ex)            
            self.close()            
            #ak_client.connect()
            self.connected = 0        
        
    
    def check_conn(self):
        
        logger.debug(self.connected)
        
        if self.connected == 0:
            self.connect()
            
        if self.connected == 0:
            
            return 0
        else:
            self.connected = 1
            return 1
    
    def cb(self):
        
        if self.connected == 0:
            
            if self.retry < conf.max_retry:
                self.connect()
            else:
                raise (Exception("break"))           
            
        if self.sock == None:
            self.retry = self.retry + 1
            raise (Exception("continue"))
            
        else:
            self.connected = 1
            self.retry = 0
            
        self.i = self.i+1
        
        if self.i > 20:
            self.i = 1  
        
    def run(self):        
        """ run """
        
        i = 0
        
        while 1:
       
            self.check_conn()
            
           
            if self.connected == 0:
                
                # sleep
                gevent.sleep(conf.reconnection_interval)
            
            else:
                
                cmd = "AVFI"
                cmd = "AWEG"
                cmd = "AWRT"
                
                cmds = ["ASTF", "ASTZ", "AWRT"]
                
                try:
                    if i<len(cmds):
                        
                        cmd = cmds[i]
                        
                        i = i +1
                        
                        self.get_data(cmd)
                        
                        # sleep
                        gevent.sleep(conf.ticker_interval)
                        
                    else:
                        i = 0
                        #cmd = cmds[i]
                    
                except Exception as ex:
                    logger.debug(ex)
                    raise(Exception("loop broken"))
                
            
        #ak_client.close()        

def main():
    """ main """
    
    logger.info("start AK client")
    
    ak_client = AKClient() 
    
    ak_client.run()
    
    cfg = Conf()
    
    
if __name__ == '__main__':
    
    main()
    
    