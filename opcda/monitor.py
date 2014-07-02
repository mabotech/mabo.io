
"""
import logging
import logging.handlers
import logging.config


logging.config.fileConfig('logging.ini')


log = logging.getLogger(__file__)
"""

import os, sys
import subprocess
import traceback


from singleton import Singleton

import simplejson


from apscheduler import events

from apscheduler.scheduler import Scheduler

import time

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


from mabolab.equipment.opc.opc_proxy import OPCProxy 





"""

bil_tags = ['Flag', 'PalletNo', 'SerialNo', 'TestCell', 'TestCount', 
			'TestStatus', 'TestTypeRun1', 'TestTypeRun2', 'TestTypeRun3']



"""

class Cache(object):
    
    __metaclass__ = Singleton
    
    def __init__(self):
        
        self.serial_no = None
        self.flag = 0
        
        #self.worker = worker
        
    def set(self, data):
        
        self.serial_no = data[2][1]
        self.flag = data[0][1]
        
        
        
    def get(self):
        
        return {"esn" : self.serial_no,  "flag" : self.flag}
        
    def reset(self):
        pass
        
        
        
    #def update(self):
    #   
    #   pass
    
class SpotCache(object):
    
    __metaclass__ = Singleton
    
    def __init__(self):
        
        self.serial_no = None
        self.spot = 0
        
        #self.worker = worker
        
    def set(self, data):
        
        self.serial_no = data[0][1]
        self.spot = data[1][1]
        
        
        
    def get(self):
        
        return {"esn" : self.serial_no, "spot":self.spot}
        
    def reset(self):
        pass    
    
    
def get_obj(data):
    obj = {}

    for val in data:
        
        #print val
        
        if val[2] != "Good":
            
            raise(Exception("Not good"))
            
        #print val[0], val[1], val[2]
        
        key =  val[0].split(".")[-1]
            
        obj[key] = val[1]
        
    return obj
    
class SpotWorker(object):

    def __init__(self):
        
        pass
        
    def save(self, data):    
        
        #print ">>"*25
        
        esn = data[0][1]
        
        spotflat = data[1][1]
        
        if spotflat == True:
            spottest = 2
        else:
            spottest = 0
        
        sql = "select mt_f_serialno_test_spot('%s','%s','spot','42701')" % (esn, spottest)
        
        #print sql
        
        rtn = db.execute(sql)
        sql="""select cwbvr.status AS status ,cwbvr.lastupdateon FROM cob_t_build_verification cbv inner join cob_t_wo_build_verifi_req cwbvr on cbv.id=cwbvr.buildverificationid
                and upper(cbv.type)='AUDIT' and cwbvr.esn='%s' and cbv.workstation='42700'"""%(esn)
        

        
        """sql = "select status, lastupdateon from cob_t_serial_no_workstation 
    where serialno = '%s'  and workstation = '42700' 
    order by id desc" % (esn)"""
        #print ">>"*20
        #print sql

        rtn = ora.execute(sql)
        
        row = rtn.fetchone()
        
        if row != None:
            if row[0] ==1:
                auditstatus = 'P'
            else:
                auditstatus = 'F'
            
            sql = "select mt_f_serialno_test_audit('%s','%s','audit','42701')" %(esn, auditstatus)
            
            #print ">>"*30
            log.debug( sql )
            
            rtn = db.execute(sql)
        else:
            log.debug("can't find esn:%s in ng db" %(esn))
            
        
        
        
    
class Worker(object):

    def __init__(self):
        
        pass
        
    def save(self, data):
        
        text = ""
        #db.call_sp(text)
        
        try:
            
            obj = get_obj(data)
            
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
            raise(Exception("type wrong"))
        
        obj['TestCount'] = int(obj['TestCount'] )
            
        if obj['TestStatus'] not in ['N','P','F','I']:
             raise(Exception("status wrong"))   
        
        #mt_f_serialno_test_data
        #(i_serialno character varying, i_container character varying, i_testcell character varying, i_testtype character varying, i_testcount integer, i_teststatus character varying, i_resource character varying, i_workcenter character varying)

        #print "data: %s" % (data)
        sql = "select mt_f_serialno_test_data('%(SerialNo)s', '%(PalletNo)s', '%(TestCell)s', '%(TestType)s','%(TestCount)s', '%(TestStatus)s', 'rs','42700' )" % obj
        #print sql
        #sql = "select now() as dt"
        rtn = db.execute(sql)
        #print rtn.fetchone()
        #print "saved"

class SpotMonitor(object):
    
    def __init__(self):
        
        self.worker = SpotWorker()
        
        self.cache = SpotCache()
        
        self.opcc = OPCClient()
        
        self.group = "BLI.42701S"
        pass
        
    def check(self):
        
        
        #raise( Exception("err"))
        
        data = self.opcc.read(self.group)
        #print data
        
        if data != None:
        
            esn = data[0][1]
            spot = data[1][1]
        else:
            return 0
        
        log.debug( "esn:%s" % (esn ) )
        
        prev_esn = self.cache.get()["esn"]
        
        if esn != prev_esn  :
            
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

class BLIMonitor(object):
    
    def __init__(self):
        
        self.worker = Worker()
        
        self.cache = Cache()
        
        self.opcc = OPCClient()
        
        self.group = "Channel1.Device1"
        pass
        
    def check(self):
        
        
        #raise( Exception("err"))
        
        data = self.opcc.read(self.group)
        #print data
        
        if data != None:
            print data
            esn = data[2][1]
            flag = data[0][1]
        else:
            return 0
        
        log.debug( "esn:%s" % (esn ) )
        
        prev_esn = self.cache.get()["esn"]
        
        if  flag == 1 and esn != prev_esn  :
            
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


class OPCClient(object):
    
    def __init__(self):        
    
        group_names =["Channel1.Device1"]# ["BLI.42700M","BLI.42701S"]

        fh = open("config.json", "r")

        data = fh.read()

        json = simplejson.loads(data)

        

        host =  'mabo01'
        
        port = 7766
        
        provider = "SWToolbox.TOPServer.V5"
        opc_server = '192.168.100.107'#
        timeout = 20000

        self.opc_proxy = OPCProxy(host, port, provider, opc_server, timeout)

        self.opc_proxy.connect()
        
        for group_name in group_names:
        
            points =  json[group_name]["points"]
            
            print points
            print group_name
            
            print self.opc_proxy.read2(points, group_name)


    def read(self, group_name):
        
        print group_name
        
        v = self.opc_proxy.read3(group_name)

        return v

def err_listener(ev):  
    
    #print dir(ev)   
    
    if ev.exception:        
        
        log.debug ( traceback.format_exc() )

        if ( type( ev.exception .message) == unicode ):
            log.debug( ev.exception .message.encode('utf8')) #.encode("gb2312")
        else:
            log.debug("exception:"+ev.exception .message)

        log.debug ( sys.exc_info() )    

        log.debug ('%s error.' % str(ev.job))  
    else:  
        
        log.debug( "%s:[%s]" % ( ev.code, ev.retval ) )
        pass
  
#
def kill(fn):

    pidf = open(fn, 'r')
    
    pid = pidf.read()
    
    cmd ="tskill %s"%(pid)
    
    log.debug("kill process")
    
    try:
        subprocess.Popen(cmd, shell=True) 
    except:
        log.error("kill failed")
        
    pidf.close()
    
def update_pid(fn):
    pidf = open(fn, 'w')
    pid = str(os.getpid())
    pidf.write(pid)
    pidf.close()

def check_pid():
    
    fn = "monitor_pli.pid"
    
    if os.path.exists(fn):
        kill(fn)

    update_pid(fn) 
    
def run():
    
    log.info( "BLI Monitor starting..." )
    
    #check_pid()
    
    bli = BLIMonitor()    
   
    spot = SpotMonitor()
    
    while True:
        bli.check()
        time.sleep(3)
        
    
    #sched = Scheduler(daemonic = False)
    
    
    #sched.add_listener(err_listener, events.EVENT_ALL) 
    
    #sched.add_interval_job(lambda:bli.check(), seconds=3)
    
    #sched.add_interval_job(lambda:spot.check(), seconds=3)
    
    #sched.add_listener(err_listener,  events.EVENT_JOB_ERROR | events.EVENT_JOB_EXECUTED| events.EVENT_JOB_MISSED)  
   
    #sched.start()
    
    log.info( "started" )
    
    
    
    """
    while 1:
        time.sleep(2)
        
        monitor.check()
    """
    pass

def stop():
    pass

def dbtest(serialno):
    
    sql = """select status, lastupdateon from cob_t_serial_no_workstation 
where serialno = '%s'  and workstation = '42700' 
order by id desc""" % (serialno)

    rtn = ora.execute(sql)
    
    row = rtn.fetchone()
    
    #print row
    
    sql = "select now()"
    
    rtn = db.execute(sql)
    
    row = rtn.fetchone()
    
    #print row
    
    
    
if __name__ == "__main__":
    
    run()
    #esn = '90000641'
    
    #dbtest(esn)
    
    
    
