# -*- coding: utf-8 -*-


"""
simulator for AK Server
"""

import socket
import sys

import thread
#from thread import *

import struct

import logbook
#import gevent

from time import strftime, localtime

from utils import get_conf

logbook.set_datetime_format("local")

logger = logbook.Logger('AKS')

#log = logbook.FileHandler('heka_tcp.log')

log = logbook.RotatingFileHandler('ak_srv.log', max_size=10240, backup_count=5)

log.push_application()

STX = 0x02
ETX = 0x03
BLANK = 0x20

def pack(cmd):
    
    clen = len(cmd)
    
    dt = strftime("%Y-%m-%d %H:%M:%S", localtime())
    
    data = "MABO TEST " + dt
    dlen = len(data)
    
    fmt = "!2b%ds3b%ds1b" % (clen, dlen)
    
    buf = struct.pack(fmt, STX, BLANK, cmd, BLANK, 0x01, BLANK, data, ETX) 
    
    print buf
    
    return buf

def clientthread(conn):
    
    """ client thread """
    try:
        while True:
             
            #Receiving from client
            
            idata = conn.recv(1024)
            logger.debug("recv")
            
            fmt = "%db" % (len(idata))
            
            val = struct.unpack(fmt, idata)
            
            print(val)
            
            if not idata: 
                break
                
    
            buf = pack("ABCD")
            
            conn.sendall(buf)
         
        #came out of loop
        conn.close()
    except Exception as ex:
        print ex
        #print("client closed")
        #raise



def main(): 
    """ main """
    
    conf = get_conf("ak_server.toml")
    
    logger.info("start AK simulator server")
    host = conf["server"]["host"]
    
    port = conf["server"]["port"]
     
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'Socket created'
     
    #Bind socket to local host and port
    try:
        sock.bind((host, port))
        
    except socket.error as msg:
        
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
         
    print 'Socket bind complete'
     
    #Start listening on socket
    sock.listen(10)
    print 'Socket now listening'
     
    #Function for handling connections. This will be used to create threads

    #now keep talking with the client
    while 1:
        #wait to accept a connection - blocking call
        conn, addr = sock.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
         
        # start new thread takes 1st argument as a function name to be run, 
        # second is the tuple of arguments to the function.
        thread.start_new_thread(clientthread ,(conn,))
     
    sock.close()
    
if __name__ == "__main__":
    main()