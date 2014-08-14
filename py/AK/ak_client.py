# -*- coding: utf-8 -*-

""" 
AK Client 
AK Protocol

"""

import socket
import struct

#import aklib

import gevent

from conf import Conf

conf = Conf("ak_client.toml")

from local_logger import get_logger

logger = get_logger('AKC')

#log = logbook.FileHandler('heka_tcp.log')

import aklib


STX = 0x02
ETX = 0x03
BLANK = 0x20
K = ord('K')   


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
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect(self):        
        """ connect """
        try:         
            
            self.sock.connect((conf.host, conf.port))
            
        except Exception as ex:
            print ex
            self.sock = None
            
    def pack(self, cmd):        
        """ pack """        
        #cmd = "AVFI"      
        clen = len(cmd)
        fmt = "!2b%ds5b" % (clen)
        #print fmt
        buf = struct.pack(fmt, STX, BLANK, cmd, BLANK, K, conf.channel_number, BLANK, ETX)
        print(buf)
        return buf
    
    def send(self, buf):        
        """ send """
        
        self.sock.sendall(buf)
        
    def process(self, val):
        """ process received data """
        
        try:
            func =  getattr(aklib, val[2].lower())
            func(val[6])
        except Exception as ex:
            logger.debug(ex)
            #'module' object has no attribute 'abcd'
            raise Exception("no parser")         
        
        
    def recv(self):        
        """ recv """
        
        data = self.sock.recv(1024)
        
        dlen = len(data) - conf.non_data_len#10
        
        if dlen < 0:
            raise Exception("struct error")
            
        logger.debug( data )
        
        fmt = "!2b4s3b%ds1b" % (dlen)
        
        try:
            val = struct.unpack(fmt, data)
            
            self.process(val)
        except Exception as ex:
            
            logger.error(ex)
        
        #print(val)
        
        #msg = "Cmd:[%s],Error:[%s], Data:[%s]" % (val[2], val[4], val[6])
        
        #logger.debug ( msg )
        
          
            
        #cmd = val[2]
        
        #return cmd
        #print val
        #print repr(val)       
    
    def close(self):        
        """ close socket """
        
        self.sock.close()
 
    def run(self):        
        """ run """  
        
        connected = 0
        
        i = 0
        
        retry = 0
        
        while 1:        
       
            if connected == 0:
                
                if retry < conf.max_retry:
                    self.connect()
                else:
                    break
               
                
            if self.sock == None:
                retry = retry + 1
                continue
            else:
                connected = 1
                retry = 0
                
            i = i+1
            
            if i > 20:
                i = 1
                
            try:
                
                cmd = "AVFI"
                
                buf = self.pack(cmd)
                
                self.send(buf)
                
                self.recv()
                
            except Exception as ex:
                print (ex)
                try:
                    self.close()
                except Exception as ex:
                    print (ex)
                    print("closed?")

                #ak_client.connect()
                connected = 0
                
            gevent.sleep(conf.ticker_interval)
        #ak_client.close()        

def main():
    """ main """
    
    logger.info("start AK client")
    
    ak_client = AKClient() 
    
    ak_client.run()
    
    cfg = Conf()
    
    
if __name__ == '__main__':
    
    main()
    
    