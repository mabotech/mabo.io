# -*- coding: utf-8 -*-

"""
opc da proxy
"""
__version__ = '0.2'

import time
import sys
import traceback
from threading import Lock
import logging
import logging.handlers

#import logging.config

import Pyro.core
import OpenOPC
import pythoncom
from OpenOPC import OPCError

log = logging.getLogger(__file__)

#import simplejson as json
from mabopy.patterns.singleton import Singleton

from exceptions import GatewayException, OPCServerException

class OPCProxy(object):
    
    """ OPC Proxy
    
    disconnection:
    - openopc gateway
    - opc server    
    """
    
    __metaclass__ = Singleton    
  
    def __init__(self, mode, host, port, opc_server,  opc_host, timeout):
        """ init """
        
        #pythoncom.CoInitialize ()
    
        #self.provider = provider #'SWToolbox.TOPServer.V5'
        
        self.mode = mode        
        self.opc_server = opc_server
        self.opc_host = opc_host        
        self.readonly = False        
        self.reconnecting = 0        
        self.count = 0        
        self.lock = 0
        self.host = host    
        self.port = port
                
        self.timeout = timeout #20000
        
        self.failedTimes = 0        
        self.groups = {}        
        #self.initialize()        
        st = time.time()
        self.namedict = {}        
        self.connection_attempts = 0        
        self._lock = Lock()
    
    def connect(self):
        """ connect """
        self._lock.acquire()
        
        self._lock.release()        
      
        try:
            #print self.host
            #print self.opc_host
            #print self.opc_server
            
            #self.opc  = OpenOPC.open_client(self.host, self.port)
            if self.mode == 'dcom':
                self.opc = OpenOPC.client("Graybox.OPC.DAWrapper", self.host)
            else:
                self.opc  = OpenOPC.open_client(self.host, self.port)
                
            self.opc.connect(self.opc_server, self.opc_host) 
            info =  self.opc.servers()
            
            print info
            
        except OPCError, oe:
            log.debug( str(oe) )
            raise Exception(oe.message)
        except Exception, e:
            log.debug(traceback.print_exc() )
            raise Exception(e.message)

    def reconnect(self):
        """ reconnect """
        log.info("reconnect...")
  
        info = ""
        
        if self._lock.locked() == False:
            #self.reconnecting = 1
            self._lock.acquire()
            try:
              
                #self.opc  = OpenOPC.open_client(self.host, self.port)
                #self.opc.connect(self.provider, self.host)
                if self.mode == 'dcom':
                    self.opc = OpenOPC.client("Graybox.OPC.DAWrapper", self.host)
                else:
                    self.opc  = OpenOPC.open_client(self.host, self.port)
            
                info =  self.opc.servers()
                info = info + self.opc.info()
                for group in self.groups:
                
                    self.create_group(group, self.groups[group])
              
                #self.reconnecting = 0
            except Exception, e:
                # release the lock
                info = "excetp: %s"%(e.message)
                log.error(info)
                log.error(traceback.format_exc())
                #self.reconnecting = 0
                
            finally:
                log.debug("lock release")
                self._lock.release()
        else:
            
            info = "reconnecting..."
            log.debug(info)
            return info

    def createGroupByTag(self, tag):
        """ create group """
        tags = []
        for item in self.workstations:
            itag =  "%s.%s"%(item, tag)
            tags.append(itag)
        #print tags
        return self.opc.read(tags, group=tag, timeout = self.timeout)
    
    def createGroupByWS2(self, group):
        """ create group """
        tags = []

        for item in self.tagnames:
            tag = "%s.%s"%(group, item)
            tags.append(tag)
        #log.debug(tags)
        return self.opc.read(tags, group=group, update=500, timeout = self.timeout)    
    
    def create_group(self, igroup, itags):
        """ create group """
        tags = []
        self.groups[igroup] = itags
        #create group for each tag in tag list
        for item in itags:
          tag = "%s.%s"%(igroup, item)
          tags.append(tag)
          
        return self.opc.read(tags, group=igroup, update=500, timeout = self.timeout)
    
    def removeGroup(self, group):
        """ remove group """
        self.opc.remove(group)
    
    def removeAllGroups(self):
        """ remove all groups """
        #print self.printGroup()
        self.opc.remove(self.opc.groups())
  
    def getGroups(self):
        """ get groups"""
        return self.opc.groups()
    
    def getproperties(self, tag):
        """ get properties """
        return self.opc.properties(tag)

    def getRootList(self):
        """ get root list """
        return self.opc.list()
    
    def getNodeList(self, node):
        """ get node list """
        return self.opc.list(node)
        
    def read2(self, tags, group):
        """ read """
        #print dir(self.opc)
        #print tags
        #print group
        log.debug("read2:%s" % group )           
        
        return self.opc.read(tags = tags, group=group, update=200)
    
    def read3(self, group):
        """ read """
        log.debug("read3:%s" % group )
        return self.opc.read(group=group, update=200)
    
    
    def read(self, igroup):
        """ read """
        #if self._lock.locked() == False:
        
        #check circuit breaker

        try:
            
            return self.opc.read(group=igroup, timeout = self.timeout)
        
        except Exception, e:
            info = 'recreate group: %s...'%(igroup)
            #log.error(info)
            info = "excetp: %s"%(e.message)  #
            log.error(info)
            log.error(traceback.format_exc())      
            #self.recreateGroup()              
            self.reconnect()

            return None
          
        #else:            
        #    log.debug("locked")            
        #    return None
    
    def mwrite(self, lst):
        """ write """
        #raise Exception("""Can't Write""")
        t1 = time.time()
        #print "in multiple write:[%s]"%str(lst)
        v = self.opc.write( lst, include_error=True)
        dur = "%.4fs"%(time.time() - t1)
        now = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        info = "%s,write:[%s]/%s"%(now, str(lst), dur)
        #log.debug(info) 
        return (v, dur)
    
    def write(self, tag, value):
        """ write """
        #raise Exception("""Can't Write""")  
        
        t1 = time.time()
        v = self.opc.write( [(tag,value)], include_error=True)
        dur = "%.4fs"%(time.time() - t1)
        now = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        #log.debug("%s,write:[%s][%s]/%s"%(now, tag, value, dur) )    
        return (v, dur, value)  
        #return "in write:[%s][%s] BUT NO ACTION"%(tag, value)
        
    def printGroup(self):
        """ print group """
        pass
        #log.debug( self.opc.groups() )
        
    def close(self):
        """ close """
        self.opc.close()
    
    def __del__(self):
        """ delete """
        pass

if __name__ == "__main__":    
    
    opc_server = "SWToolbox.TOPServer.V5"
    host = 'mabo01'
    port = 7766
    opc_host = 'mabo01'
    
    mode = 'dcom'
    
    opc = OPCProxy(mode, host, port, opc_server, opc_host , 20000)
    opc.connect()
    #print opc.read2(["MT", "Tag1", "Tag2"], "Channel1.Device1")
    print opc.read2(["Channel1.Device1.MT", "Channel1.Device1.Tag1", "Channel1.Device1.Tag2"], "Channel1.Device1")
    #print opc.read3("Channel1.Device1")

    #print opc.read2(["Flag", "PalletNo", "SerialNo", "TestCell", "TestCount", "TestStatus", "TestTypeRun1", "TestTypeRun2", "TestTypeRun3"], "BLI.42700M")
    #print opc.read3("BLI.42700M")
