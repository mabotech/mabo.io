
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
    
    __metaclass__ = Singleton
    
    def __init__(self):
        
        self.serial_no = None
        self.flag = 0
        
        #self.worker = worker
        
    def set(self, data):
        
        self.serial_no = data["SerialNo"]
        self.flag = data["Flag"]
        
        
        
    def get(self):
        
        return {"esn" : self.serial_no,  "flag" : self.flag}
        
    def reset(self):
        pass
        
        
        
    #def update(self):
    #   
    #   pass
   
class Worker(object):

    def __init__(self):
        
        pass
        
    def save(self, data):
        
        text = ""
        #db.call_sp(text)
        
        try:
            
            obj = data #get_obj(data)
            
        except:
            return
        
        #print "=="*20
        #raise(Exception("save exception"))
        #print "save"
        
        if obj['TestTypeRun1'] == '01':
            obj['TestType'] = '9M'
        elif obj['TestTypeRun2'] == '01':
            obj['TestType'] = '30M'
        elif obj['TestTypeRun3'] == '01':
            obj['TestType'] = '3'
        else:
            raise(Exception("test type is wrong"))
        
        obj['TestCount'] = int(obj['TestCount'] )
            
        if obj['TestStatus'] not in ['N','P','F','I']:
             raise(Exception("status is wrong"))   
        
        #mt_f_serialno_test_data
        #(i_serialno character varying, i_container character varying, i_testcell character varying, i_testtype character varying, i_testcount integer, i_teststatus character varying, i_resource character varying, i_workcenter character varying)

        #print "data: %s" % (data)
        sql = "select mt_f_serialno_test_data('%(SerialNo)s', '%(PalletNo)s', '%(TestCell)s', '%(TestType)s','%(TestCount)s', '%(TestStatus)s', 'bli','42700' )" % obj
        #print sql
        #sql = "select now() as dt"
        rtn = db.execute(sql)
        #print rtn.fetchone()
        #print "saved"
        
        
class BLIMonitor(object):
    
    def __init__(self):
        
        self.worker = Worker()
        
        self.cache = Cache()
        
        self.opcc = OPCClient()
        
        self.group = "BLI.42700M"
        pass
        
    def check(self):
        
        
        #raise( Exception("err"))
        
        #print "<<"*20
        
        data = self.opcc.get_data(self.group)
        #print data
        log.debug(data)
        if data != None:
            #print data
            #data["SerialNo"] =data["SerialNo"][3:]
            esn = data["SerialNo"]
            flag = data["Flag"]
        else:
            return 0
        
        log.debug( "flag:%s, esn:%s" % (flag, esn) )
        
        prev_esn = self.cache.get()["esn"]
        
        if  flag == '1' and esn != prev_esn  :
            
            log.debug("pervious esn: %s" % (prev_esn) )
        
            self.cache.set(data)
            
            try:
                self.worker.save(data)
                #print data
            except Exception, e:
                log.debug(e.message)
                
            return 1
            
        else:
            return 0
            pass
