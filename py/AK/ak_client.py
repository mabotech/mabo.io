# -*- coding: utf-8 -*-


""" 
AK Client 
AK Protocol

"""

import socket

import struct

#import aklib
import logbook
import gevent


from utils import get_conf

logbook.set_datetime_format("local")

logger = logbook.Logger('AKC')

#log = logbook.FileHandler('heka_tcp.log')

log = logbook.RotatingFileHandler('ak_cli.log', max_size=10240, backup_count=5)

log.push_application()

import aklib

STX = 0x02
ETX = 0x03
BLANK = 0x20
K = ord('K')
    
funcs = {"ABCD": aklib.a1, "AVFI": aklib.a2}


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
        
        conf = get_conf("ak_client.toml")
        
        self.host = conf["client"]["host"]
        self.port = conf["client"]["port"] 
        
        self.retry = 3
        
        self.retry_interval = 2
        
        self.timeout = 6
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect(self):
        
        """ connect """
        try:
            
            
            self.sock.connect((self.host, self.port))
            
        except Exception as ex:
            print ex
            self.sock = None
            
    @classmethod
    def pack(cls, cmd):
        
        """ pack """
        
        #cmd = "AVFI"
      
        clen = len(cmd)
        fmt = "!2b%ds5b" % (clen)
        
        buf = struct.pack(fmt, STX, BLANK, cmd, BLANK, K, 0, BLANK, ETX)
        print(buf)
        return buf
    
    def send(self, buf):
        
        """ send """
        
        self.sock.sendall(buf)
        
    def recv(self):
        
        """ recv """
        
        data = self.sock.recv(1024)
        
        dlen = len(data) - 10
        
        if dlen < 0:
            raise Exception("struct error")
            
        print ( data )
        
        fmt = "!2b4s3b%ds1b" % (dlen)
        
        val = struct.unpack(fmt, data)
        
        print(val)
        msg = "Cmd:[%s],Error:[%s], Data:[%s]" % (val[2], val[4], val[5])
        logger.debug ( msg )
        
        if val[2] in funcs:
            func = funcs[val[2]]
            func(val[5])
        else:
            raise Exception("no parser")
            
        cmd = val[2]
        
        return cmd
        #print val
        #print repr(val)
        
    
    def close(self):
        
        """ close socket """
        self.sock.close()
 
def main():
    
    """ main """
    
    logger.info("start AK client")
    
    ak_client = AKClient()    
    
    connected = 0
    
    i = 0
    
    retry = 0
    
    while 1:        
   
        if connected == 0:
            
            if retry < 5:
                ak_client.connect()
            else:
                break
           
            
        if ak_client.sock == None:
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
            
            buf = ak_client.pack(cmd)
            
            ak_client.send(buf)
            
            ak_client.recv()
            
        except Exception as ex:
            print (ex)
            try:
                ak_client.close()
            except Exception as ex:
                print (ex)
                print("closed?")

            #ak_client.connect()
            connected = 0
            
        gevent.sleep(1)
    #ak_client.close()        
        
if __name__ == '__main__':
    
    main()
    
    