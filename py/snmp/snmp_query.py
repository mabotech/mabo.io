# -*- coding: utf-8 -*-

import time
from time import strftime, localtime

import socket
import gevent

from pysnmp.entity.rfc3413.oneliner import cmdgen

def exception(Exception):
    
    def __init__(self):
        pass
    
# def getValue():

# def getData():

# thread pool, gevent





def query(node):
    """
    return value, elapsed time
    """
    # gevent timeout not work here
    
    start = time.time()
    
    result = None
    
    print strftime("%Y-%m-%d %H:%M:%S", localtime())
    
    with gevent.Timeout(1, False) as timeout: 
        
        
        #gevent.sleep(5)
        cmdGen = cmdgen.CommandGenerator()

        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
            cmdgen.CommunityData('public'),
            cmdgen.UdpTransportTarget(('demo.snmplabs.com', 161)),
            #cmdgen.UdpTransportTarget(('localhost', 161)),
            '1.3.6.1.2.1.1.5.0'
        )
        print 
        print("===="*4)
        result ='\n'.join([ '%s = %s' % varBind for varBind in varBinds])
    
    if result != None:
        print("seq:%s, result:[%s]" % (node,result ))
    else:
        print "timeout"
    #finally:
    #    timeout.cancel()
    
    return time.time() - start
    
def mainloop():
    
    
    while True:
    
        for i in xrange(0, 3):
            duration = query(i)
            print "%s" %(duration)
        
        gevent.sleep(1)
        
    
if __name__ == "__main__":
    mainloop()