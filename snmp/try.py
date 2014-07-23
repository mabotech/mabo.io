

import gevent

from pysnmp.entity.rfc3413.oneliner import cmdgen

def exception(Exception):
    
    def __init__(self):
        pass
    

def main():
    
    # gevent timeout not work here
    with gevent.Timeout(1, False) as timeout: 
        cmdGen = cmdgen.CommandGenerator()

        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
            cmdgen.CommunityData('public'),
            cmdgen.UdpTransportTarget(('demo.snmplabs.com', 161)),
            #cmdgen.UdpTransportTarget(('localhost', 161)),
            '1.3.6.1.2.1.1.2.0'
        )
        print 
        print("===="*4)
        print('\n'.join([ '%s = %s' % varBind for varBind in varBinds]))
    
    #finally:
    #    timeout.cancel()
if __name__ == "__main__":
    main()