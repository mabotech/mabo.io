

import socket

import gevent

import time
from time import strftime, localtime

def main():
    
    
    while True:

        fn = "f%s.dat" % (strftime("%Y_%m_%d_%H_%M_%S", localtime()))
        fh = open(fn, "w")
        for i in xrange(1,10):
            fh.write("OK[%s]" % (i))
            fh.flush()
            gevent.sleep(0.1)
            
        fh.close()
        
        gevent.sleep(5)
        
        
if __name__ == "__main__":
    main()