# -*- coding: utf-8 -*-

import sys

#
sys.setrecursionlimit(40)

import time
from time import strftime, localtime

import gevent

from gevent.pool import Pool

from gevent import socket

from msgpack import packb, unpackb

#server = SimpleServer(('127.0.0.1', 0))
#server.start()

def query(j, i):
    
    print "in query:%s" %(j)

    t = time.time()

    try:
        client = socket.create_connection(('127.0.0.1', 5001))
        
    except Exception, e:
        
        print ">>"*20
        print e.message
        
        return ""
    
    v = {'dd_%s'%(i):'abc12333:'+ str(t)} 
    
    print v
    
    
    client.send( packb(v))
    #raise(Exception("query error"))
    y = None
    with gevent.Timeout(2, False):
        y = client.recv(10240)
    
    if y != None:
        print "unpackb:"+unpackb(y)
    else:
        print "timeout"
    #raise(Exception("query error"))
    print "%s : %s" % (i, time.time() - t)


    #print dir(client)

    #client.send('0')

    #y = client.recv(10240)

    #print "[%s]"%(y)
    
    gevent.sleep(0)
    
    client.close()



    #response = client.makefile().read()
    #print response
    #server.stop()

pool = Pool(10)

j = 0

def loop():
    
    global j
    
    print dir(pool)
    
    while True:
        j = j + 1
        
        print "=="*20
        print strftime("%Y-%m-%d %H:%M:%S", localtime())
        print "=="*20
        print "in loop\n"
        
        try:
            
            with gevent.Timeout(2, False):
                
                for i in xrange(3):
                    
                    #test cb
                    #if circuit_breaker.broken == True: 
                    pool.spawn(query, j, i) 
                    
                #pool.join()
                
                print "free_count: %s" % ( pool.free_count() )
                
        except Exception, e:

            print e.message

        gevent.sleep(1) #joinall(v)
    
    #gevent.spawn(loop).join() #waiting the loop finish


def run():
    
    print "run"

    loop()
    
    
def main():
    
    
    run()
    
if __name__ == '__main__':
    
    #run()
    #gevent.sleep(100)
    main()
    