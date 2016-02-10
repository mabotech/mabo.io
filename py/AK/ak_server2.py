# -*- coding: utf-8 -*-

"""
simulator for AK Server
"""

import socket
import sys
import traceback

import thread
#from thread import *

import struct

import logbook
#import gevent

from time import strftime, localtime

from utils import get_conf

logbook.set_datetime_format("local")

logger = logbook.Logger('AKSrv')

#log = logbook.FileHandler('heka_tcp.log')

log = logbook.RotatingFileHandler('logs/ak_server.log', max_size=102400, backup_count=5, \
                    bubble=True)

log.push_application()

# static
STX = 0x02
ETX = 0x03
BLANK = 0x20 # 

def pack(cmd):    
    """ pack """
    
    clen = len(cmd)
    
    dt = strftime("%Y-%m-%d %H:%M:%S", localtime())
    
    if cmd == "ASTF":
        
        fmt = "!2b%ds3b" % (clen)    
        # 0x48:'0'
        buf = struct.pack(fmt, STX, BLANK, cmd, BLANK, 0x30, ETX)         
    
    else:
        data = " SMAN STBY SLIR SVOR SBEI N/A "
        dlen = len(data)
        
        fmt = "!2b%ds3b%ds1b" % (clen, dlen)
    
        # 0x48:'0'
        buf = struct.pack(fmt, STX, BLANK, cmd, BLANK, 0x48, BLANK, data, ETX) 
    
    logger.debug(buf)
    
    return buf

def clientthread(conn):    
    """ client thread """
    
    try:
        while True:
             
            #Receiving from client
            
            idata = conn.recv(1024)
            logger.debug("recv")
            
            dlen = len(idata) - 11
            
            print dlen
            
            if dlen > 0:   
                fmt = "!2b4s4b%ds1d" % (dlen)
                
            else:
                fmt = "!2b4s5b"
                
            val = struct.unpack(fmt, idata)
            print(val)
            logger.debug(val)
            
            if not idata: 
                break
                
    
            buf = pack(val[2])
            
            conn.sendall(buf)
            #break
         
        #came out of loop
        conn.close()
    except Exception as ex:
        logger.debug(ex)
        #print("client closed")
        #raise



def server(): 
    
    """ server """
    conf = get_conf("config/ak_server.toml")
    
    logger.info("start AK simulator server")
    host = conf["server"]["host"]
    
    port = conf["server"]["port"]
     
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    logger.debug('Socket created %s:%s' % (host, port) )
     
    #Bind socket to local host and port
    try:
        sock.bind((host, port))
        
    except socket.error as msg:
        
        logger.debug('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1] )
        sys.exit()
         
    logger.debug('Socket bind complete')
     
    #Start listening on socket
    sock.listen(10)
    logger.debug('Socket now listening')
     
    #Function for handling connections. This will be used to create threads

    #now keep talking with the client
    while 1:
        #wait to accept a connection - blocking call
        conn, addr = sock.accept()
        logger.debug( 'Connected with ' + addr[0] + ':' + str(addr[1]) )
         
        # start new thread takes 1st argument as a function name to be run, 
        # second is the tuple of arguments to the function.
        thread.start_new_thread(clientthread ,(conn,))
     
    sock.close()
    
def main():
    """ main """
    server()
    
if __name__ == "__main__":
    
    main()