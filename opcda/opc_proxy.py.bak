import logging
import logging.handlers, logging.config


from threading import Lock

_lock = Lock()

import Pyro.core

import OpenOPC
import time

import sys
import traceback

#import simplejson as json



class OPCProxy:
    
    
  
    def __init__(self, host, port, provider, timeout):
    
        self.provider = provider #'SWToolbox.TOPServer.V5'
        
        self.reconnecting = 0
        
        self.count = 0
        
        self.lock = 0

        self.host = host    
        self.port = port
                
        self.timeout = timeout #20000
        

        
        self.failedTimes = 0
        
        self.groups = {}
        
        self.initialize()
        
        st = time.time()

        #self.workstations = [u'35200M', u'35300A', u'35350A', u'35450M', u'35500M', u'35600A', u'35700M', u'35800A', u'35850A', u'35900T', u'35913R', u'36000M', u'36050A', u'36100M', u'36250M', u'36255M', u'36350A', u'36400A'] 
        
        #self.tagnames = ['point1', 'point2', 'point3', 'point4', 'point5', 'point6', 'point7']
        #self.tagnames = ['ENGINE_RUNNING', 'ERROR', 'ENGINE_WAITING_FOR_START', 'NO_ENGINE_IN_TESTCELL', 'SUMP_LEVEL_MAX', 'TESTRUN_ERROR', 'SERVICE_MODE']
            
        self.namedict = {}


        """
        i = 0
        
        for item in self.tagnames:
          self.namedict[item] = i
          i = i + 1
        """
    
    def connect(self):
        
        _lock.acquire()
        
        _lock.release()        
      
        try:
            self.opc  = OpenOPC.open_client(self.host, self.port)
            
            self.opc.connect(self.provider,self.host)      

        except Exception, e:
            
            raise Exception(e.message)

    def reconnect(self):
        pass
        
    
    def initialize(self):
        pass
    
    
    def recreateGroup(self):
        
        _lock.acquire()
        
        _lock.release()
        
        
        info = ""
        if self.reconnecting == 0:
          self.reconnecting = 1
          try:
            self.opc  = OpenOPC.open_client(self.host, self.port)
            self.opc.connect(self.provider, self.host)
            info =  self.opc.servers()
            info = info + self.opc.info()
            for group in self.groups:       
              self.createGroupByWS2(group)
            self.reconnecting = 0
          except Exception, e:
            # release the lock
            info = "excetp: %s"%(e)
            log.error(info)
            log.error(traceback.format_exc())
            self.reconnecting = 0
        else:
          info = "working..."
        return info

    def createGroupByTag(self, tag):
        tags = []
        for item in self.workstations:
          itag =  "%s.%s"%(item, tag)
          tags.append(itag)
        #print tags
        return self.opc.read(tags, group=tag, timeout = self.timeout)
    
    def createGroupByWS2(self, group):
        tags = []

        for item in self.tagnames:
          tag = "%s.%s"%(group, item)
          tags.append(tag)
        log.debug(tags)
        return self.opc.read(tags, group=group, update=500, timeout = self.timeout)    
    
    def create_group(self, igroup, itags):
      
        tags = []
        self.groups[igroup] = itags
        #create group for each tag in tag list
        for item in itags:
          tag = "%s.%s"%(igroup, item)
          tags.append(tag)
          
        return self.opc.read(tags, group=igroup, update=500, timeout = self.timeout)
    
    def removeGroup(self, group):
        self.opc.remove(group)
    
    def removeAllGroups(self):
        #print self.printGroup()
        self.opc.remove(self.opc.groups())
  
    def getGroups(self):
        return self.opc.groups()
    
    def getproperties(self, tag):
        return self.opc.properties(tag)

    def getRootList(self):
        return self.opc.list()
    
    def getNodeList(self, node):
        return self.opc.list(node)
    
    def read(self, igroup):

        try:
          return self.opc.read(group=igroup, timeout = self.timeout)
        except Exception, e:
          info = 'recreate group: %s...'%(igroup)
          log.error(info)
          info = "excetp: %s"%(e)
          log.error(info)
          log.error(traceback.format_exc())      
          #self.recreateGroup()
          return None
    
    def mwrite(self, lst):
        #raise Exception("""Can't Write""")
        t1 = time.time()
        #print "in multiple write:[%s]"%str(lst)
        v = self.opc.write( lst, include_error=True)
        dur = "%.4fs"%(time.time() - t1)
        now = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        info = "%s,write:[%s]/%s"%(now, str(lst), dur)
        log.debug(info) 
        return (v, dur)
    
    def write(self, tag, value):
        #raise Exception("""Can't Write""")  
        
        t1 = time.time()
        v = self.opc.write( [(tag,value)], include_error=True)
        dur = "%.4fs"%(time.time() - t1)
        now = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        print "%s,write:[%s][%s]/%s"%(now, tag, value, dur)    
        return (v, dur, value)  
        #return "in write:[%s][%s] BUT NO ACTION"%(tag, value)
        
    def printGroup(self):
    
        print self.opc.groups()
        
    def close(self):
        self.opc.close()
    
    def __del__(self):
        pass

if __name__ == "__main__":
    
    
    provider = "SWToolbox.TOPServer.V5"
    host = '127.0.0.1'
    port = 7766
    
    opc = OPCProxy(host, port, provider, 20000)
    opc.connect()
