

import socket
import sys
from thread import *

import struct

import logbook
import gevent

from time import time, strftime, localtime

from utils import get_conf

logbook.set_datetime_format("local")

logger = logbook.Logger('AKS')

#log = logbook.FileHandler('heka_tcp.log')

log = logbook.RotatingFileHandler('ak_srv.log', max_size=10240, backup_count=5)

log.push_application()

def clientthread(conn):
    #Sending message to connected client
    #conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
     
    #infinite loop so that function do not terminate and thread do not end.
    
    try:
        while True:
             
            #Receiving from client
            
            idata = conn.recv(1024)
            logger.debug("recv")
            
            fmt = "%db" % (len(idata))
            
            val = struct.unpack(fmt, idata)
            
            print(val)
            
            reply = idata
            if not idata: 
                break
                
            cmd = "ABCD"
            cmd =  cmd
            clen = len(cmd)
            
            dt = strftime("%Y-%m-%d %H:%M:%S", localtime())
            
            data = "MABO 001,002,003" + dt
            dlen = len(data)
            fmt = "!2b%ds2b%ds1b" % (clen, dlen)
            buf = struct.pack(fmt, 0x02, 0x20, cmd, 0x20, 0x01, data, 3)   
            print buf
            conn.sendall(buf)
         
        #came out of loop
        conn.close()
    except Exception as ex:
        print ex
        #print("client closed")
        #raise



def main(): 
    
    conf = get_conf("ak_server.toml")
    
    logger.info("start AK simulator server")
    HOST = conf["server"]["host"]#'127.0.0.1'   # Symbolic name meaning all available interfaces
    
    PORT = conf["server"]["port"]#6010 # Arbitrary non-privileged port
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'Socket created'
     
    #Bind socket to local host and port
    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
         
    print 'Socket bind complete'
     
    #Start listening on socket
    s.listen(10)
    print 'Socket now listening'
     
    #Function for handling connections. This will be used to create threads

    #now keep talking with the client
    while 1:
        #wait to accept a connection - blocking call
        conn, addr = s.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
         
        #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
        start_new_thread(clientthread ,(conn,))
     
    s.close()
    
if __name__ == "__main__":
    main()