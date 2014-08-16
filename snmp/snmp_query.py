
from time import strftime, localtime
import gevent

from pysnmp.entity.rfc3413.oneliner import cmdgen

def exception(Exception):
    
    def __init__(self):
        pass
    

def query():
    
    # gevent timeout not work here
    
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
        print result
    else:
        print "timeout"
    #finally:
    #    timeout.cancel()
    
def main():
    
    for i in xrange(0, 3):
        query()
        gevent.sleep(1)
        
    
if __name__ == "__main__":
    main()