


import socket
import gevent

def main():

    #time.sleep(1)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    sock.connect(('127.0.0.1', 5565))
    print "connected"
        
    for i in xrange(41,43):
        
        
        
        print "send"
        
        message = "%s" %(i) #'go|cc\nd,ds\nd d,vv|od'
        
        messlen = sock.send(message*5)#, 0  
        
        print messlen
        
        gevent.sleep(0.01)
        #print received
        
        #print sock.recv(1024)
    
    sock.close()

if __name__ == '__main__':
    main()