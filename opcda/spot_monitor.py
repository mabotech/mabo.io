

import gevent


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

    
class SpotCache(object):
    
    __metaclass__ = Singleton
    
    def __init__(self):
        
        self.serial_no = None
        self.spot = 0


        
        #self.worker = worker
        
    def set(self, data):
        
        self.serial_no = data["SerialNo"]
        self.spot = data["Spot"]
        
        
        
    def get(self):
        
        return {"esn" : self.serial_no, "spot":self.spot}
        
    def reset(self):
        pass    
    

def update_audit_status(esn):

        """sql = "select status, lastupdateon from cob_t_serial_no_workstation 
    where serialno = '%s'  and workstation = '42700' 
    order by id desc""" % (esn)
        sql="""select cwbvr.result AS result ,cwbvr.lastupdateon FROM cob_t_build_verification cbv inner join cob_t_wo_build_verifi_req cwbvr on cbv.id=cwbvr.buildverificationid
                and upper(cbv.type)='AUDIT' and cwbvr.esn='%s' and cbv.workstation='42700'"""%(esn)
        
        #print ">>"*20
        #print sql

        rtn = ora.execute(sql)
        
        row = rtn.fetchone()
        
        if row != None:
            #if row[0] ==1:
            if row[0]=='PASS':
                auditstatus = 'P'
            else:
                auditstatus = 'F'
            
            sql = "select mt_f_serialno_test_audit('%s','%s','audit','42701')" %(esn, auditstatus)
            
            #print ">>"*30
            log.debug( sql )
            
            rtn = db.execute(sql)
        else:
            log.debug("can't find esn:%s in ng db" %(esn))
            
            sql = "select mt_f_serialno_test_audit('%s','%s','audit','42701')" %(esn, 'na')
            
            #print ">>"*30
            log.debug( sql )
            
            rtn = db.execute(sql)   
    

class SpotWorker(object):

    def __init__(self):
        
        pass
        
    def save(self, data):    
        
        #print ">>"*25
        
        esn = data["SerialNo"]
        
        spotflat = data["Spot"]
        
        if spotflat == 1:
            spottest = 2  #spot
        else:
            spottest = 1  #1: not spot; 0: default no decision
        
        sql = "select mt_f_serialno_test_spot('%s','%s','spot','42701')" % (esn, spottest)
        
        #print sql
        
        rtn = db.execute(sql)

        log.debug("before save")
        gevent.sleep(10)  #10
        gevent.spawn(update_audit_status, esn)
        #update_audit_status(esn)
        log.debug("after save")

class SpotMonitor(object):
    
    def __init__(self):
        
        self.worker = SpotWorker()
        
        self.cache = SpotCache()
        
        self.opcc = OPCClient()
        
        self.group = "BLI.42701S"

        log.debug("init SpotMonitor")
        
        pass
        
    def check(self):
        
        
        #raise( Exception("err"))
        #print ">>"*20
        log.debug("spot monitor check")
        data = self.opcc.get_data(self.group)
        #print data
        log.debug(data)
        
        if data != None:
            #data["SerialNo"] = data["SerialNo"][3:]
            esn = data["SerialNo"]
            spot = data["Spot"]
        else:
            return 0
        
        log.debug( "spot:%s, esn:%s" % (spot, esn ) )
        
        prev_esn = self.cache.get()["esn"]
        
        if (spot == 1 or spot == 20 or spot == 251) and esn != prev_esn:
            
            log.debug("pervious esn: %s" % (prev_esn) )
        
            self.cache.set(data)
            
            try:
                self.worker.save(data)
            except Exception, e:
                log.debug(e.message)
                
            return 1
            
        else:
            return 0
            pass

