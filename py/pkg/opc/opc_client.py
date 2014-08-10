
import logging
#import logging.handlers
#import logging.config


logging.config.fileConfig('logging.ini')


log = logging.getLogger(__file__)

import simplejson

from opc_proxy import OPCProxy 

from singleton import Singleton

class OPCClient(object):

    __metaclass__ = Singleton
    
    def __init__(self):       

        fh = open("opc_config.json", "r")

        data = fh.read()

        self.json = simplejson.loads(data)
        
        group_names = self.json["groups"]  #["Channel1.Device1"]# ["BLI.42700M","BLI.42701S"]
        host = self.json["host"]# 'mabo01'        
        port = self.json["port"]        
        opc_server =  self.json["opc_server"]# "SWToolbox.TOPServer.V5"
        opc_host = self.json["opc_host"]#server = '192.168.100.107'#
        timeout =  self.json["timeout"]#20000
        mode =  self.json["mode"]
        
        self.opc_proxy = OPCProxy(mode, host, port, opc_server, opc_host, timeout)

        try:
            self.opc_proxy.connect()
        except Exception, e:
            log.error(e.message)
            raise(Exception("Connection OPC Error"))
        for group_name in group_names:
        
            points =  self.json[group_name]["points"]
            
            #print points
            #print group_name
            
            #print 
            path = self.json[group_name]["path"]

            itags = []
            for tag in points:
                itags.append(".".join([path, tag]) )
            log.debug(itags)
            log.debug(group_name)
            v = self.opc_proxy.read2(itags, group_name)
            log.debug(v)
            
    def get_data(self, group_name):
        
        vals = self.read(group_name)
        #log.debug(group_name)
        #log.debug(vals)
        objs = {}
        
        for i in range(0, len(vals) ):
            
            if vals[i][2] != 'Good':
                log.error(str(vals))
                log.error("Quality Not Good")
                raise(Exception("Quality Not Good"))
            else:
                objs[self.json[group_name]["alias"][i]] = vals[i][1]
                
        return objs

    def read(self, group_name):
        
        #print group_name
        
        #path = self.json[group_name]["path"]
        
        v = self.opc_proxy.read3(group_name)

        return v
