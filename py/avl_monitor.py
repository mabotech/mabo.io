

from time import time, localtime, strftime

from singleton import Singleton

from opc_client import OPCClient

from flask.config import Config

from config import CENTRAL_CONFIG

from mabolab.core.global_obj import Global

settings = Config("")

settings.from_pyfile(CENTRAL_CONFIG)

settings['APP_NAME'] = "monitor_bli"

g = Global(settings)

db = g.get_db('postgresql')

ora = g.get_db('oracle')

log = g.get_logger()

class Cache(object):
    
    #__metaclass__ = Singleton
    
    def __init__(self):
        
        self.last_update = time()
        self.last_state = -1
        
        #self.worker = worker
        
    def set(self, last_state, last_update):
        
        self.last_update = last_update
        self.last_state = last_state
        
        
        
    def get(self):
        
        return {"last_state" : self.last_state,  "last_update" : self.last_update}
        
    def reset(self):
        pass
        
        
        
    #def update(self):
    #   
    #   pass
   
class Worker(object):

    def __init__(self):
        
        pass
        
    def save(self, data):
        """
        v = data['next_state']

        s = 0
        
        if v == 1:
            s = 1
            
        elif v == 0:
            s = 2
            
        elif v == 8:
            s = 2
            
        else:
            s = 3
        """    
        
        #print "data: %s" % (data)
        log.debug(data)
        sql = "select mt_f_avl_data('%(statiion)s', '%(state_start)s', '%(state_stop)s', %(duration)s, '%(state)s', '%(next_state)s')" % data
        #print sql
        log.debug(sql)
        #sql = "select now() as dt"
        rtn = db.execute(sql)

        sql = """select mt_f_avl_status_count('GCIC', '%s')""" %(data['statiion'])
        rtn = db.execute(sql)
        #print rtn.fetchone()
        #print "saved"
        
        
class AVLMonitor(object):
    
    def __init__(self, group, station):
        
        self.worker = Worker()
        
        self.cache = Cache()
        
        self.opcc = OPCClient()
        
        self.group = group #"BLI.42700M"
        
        self.station = station
        pass

    def bool2int(self, val):
        
        if type(val) == bool:
            if val == True:
                return 1
            else:
                return 0
        else:
            return 0
    
    def getInt(self, a1, a2, a3, a4, a5, a6, a7):
        return a1*1 + a2 * 2 + a3*4 + a4* 8 + a5 * 16 + a6 * 32 + a7 *64        
        
    def getValues(self, OPCValues):
    
        #self.OPCValues = None
        #self.OPCValues = simatic.readByGroup(ws)
        #print self.OPCValues
        
        #v = simatic.readByGroup(ws)
        #log.debug(str(  list(v[simatic.namedict['ESNNumber']]) ))

        #log.debug(OPCValues)
        if OPCValues != None:
          pointlist = []
          for tag in ['ENGINE_RUNNING', 'ERROR', 'ENGINE_WAITING_FOR_START', 'NO_ENGINE_IN_TESTCELL', 'SUMP_LEVEL_MAX', 'TESTRUN_ERROR', 'SERVICE_MODE']:
              val = OPCValues[tag]
              pointlist.append(self.bool2int(val))
          #~ ENGINE_RUNNING = list(self.OPCValues[simatic.namedict['ENGINE_RUNNING']])
          #~ ERROR = list(self.OPCValues[simatic.namedict['ERROR']])
          
          #~ ENGINE_WAITING_FOR_START = list(self.OPCValues[simatic.namedict['ENGINE_WAITING_FOR_START']])
          
          #~ NO_ENGINE_IN_TESTCELL = list(self.OPCValues[simatic.namedict[ 'NO_ENGINE_IN_TESTCELL']])
          #~ SUMP_LEVEL_MAX = list(self.OPCValues[simatic.namedict['SUMP_LEVEL_MAX']])
          #~ TESTRUN_ERROR = list(self.OPCValues[simatic.namedict['TESTRUN_ERROR']])
          #~ SERVICE_MODE = list(self.OPCValues[simatic.namedict['SERVICE_MODE']])
          
          #~ esn = list(self.OPCValues[simatic.namedict['NO_ENGINE_IN_TESTCELL']])

          if pointlist[0] == None \
            or pointlist[1]==None\
            or pointlist[2]==None\
            or pointlist[3]==None\
            or pointlist[4]==None\
            or pointlist[5]==None\
            or pointlist[6]==None:
                    
            return None
          else:
            info = self.getInt(pointlist[0], pointlist[1], pointlist[2], pointlist[3], pointlist[4], pointlist[5], pointlist[6])
            #~ info = self.getInt(ENGINE_RUNNING[1], ERROR[1], ENGINE_WAITING_FOR_START[1], NO_ENGINE_IN_TESTCELL[1], SUMP_LEVEL_MAX[1], TESTRUN_ERROR[1], SERVICE_MODE[1])
            return info
          
        else:
          return None      

    
    def get_time_str(self, sec):
        return strftime('%Y-%m-%d %H:%M:%S', localtime(sec))
        
    def check(self):
        
        
        #raise( Exception("err"))
        
        #print "<<"*20
        
        values = self.opcc.get_data(self.group)
        #print data
        log.debug(values)
        if values != None:
            #print data
            #data["SerialNo"] =data["SerialNo"][3:]

            #log.debug("*****")
            try:
                last_state = self.getValues(values)
            except Exception, e:
                log.debug(e.message)
            log.debug(last_state)
        else:
            log.error("values = None")
            return 0
        
        #log.debug( "last state:%s" % (last_state) )
        
        val = self.cache.get()
        prev_state = val["last_state"]
        log.debug("%s:%s-%s" % (self.station, prev_state,last_state ))
        if prev_state != last_state  :
            
            log.debug("prev_state: %s" % (prev_state))
            state_start = val["last_update"]
            state_stop = time()
            duration = state_stop - state_start
            self.cache.set(last_state, state_stop)       
            try:
                
                # strftime('%Y-%m-%d %H:%M:%S', localtime(sec))  
                
                data = {"statiion":self.station, 
                        "state_start": self.get_time_str(state_start),
                        "state_stop": self.get_time_str(state_stop),
                        "duration": duration,
                        "state": prev_state,
                        "next_state" :last_state}
                
                self.worker.save(data)
                #print data
            except Exception, e:
                log.debug(e.message)
                
            return 1
            
        else:
            log.debug("same value")
            return 0
            pass
