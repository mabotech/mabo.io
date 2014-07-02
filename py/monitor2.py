
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

import gevent

from gevent.pool import Pool


#import simplejson


#from apscheduler import events

#from apscheduler.scheduler import Scheduler

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

from spot_monitor import SpotMonitor
from bli_monitor import BLIMonitor
from avl_monitor import AVLMonitor

"""

bil_tags = ['Flag', 'PalletNo', 'SerialNo', 'TestCell', 'TestCount', 
			'TestStatus', 'TestTypeRun1', 'TestTypeRun2', 'TestTypeRun3']



"""



"""    
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
"""
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


def update_audit_status(esn):

        """sql = "select status, lastupdateon from cob_t_serial_no_workstation 
    where serialno = '%s'  and workstation = '42700' 
    order by id desc" % (esn)"""
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

def recheck():

    sql = """select serialno from mt_t_serialno_test where auditstatus = 'na' and rowversionstamp<20 """

    rtn = db.execute(sql)

    row = rtn.fetchone()

    if row != None:
        esn = row[0]

        update_audit_status(esn)

        log.debug("recheck [%s]" % (esn))

    
    
    pass
    
def run():
    
    log.info( "BLI Monitor starting..." )
    
    #check_pid()
    
    avl_group = {"TC01":"GCIC_TC01",
    "TC02":"GCIC_TC02",
    "TC03":"GCIC_TC03",
    "TC04":"GCIC_TC04"}
    
    avl_list = []
    
    for group in avl_group:
        station = avl_group[group]
        obj = AVLMonitor(group, station)
        avl_list.append(obj)
    
    bli = BLIMonitor()    
   
    spot = SpotMonitor()
    
    pool = Pool(20)
    
    while True:
        
        for obj in avl_list:
            pool.spawn(obj.check)
            gevent.sleep(0)
        
        pool.spawn(bli.check) 
        gevent.sleep(0)
        pool.spawn(spot.check) 
        #bli.check()
        #time.sleep(3)
        pool.spawn(recheck)
        gevent.sleep(2)
    
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

def test():
    sql="""select cwbvr.status AS status ,cwbvr.lastupdateon FROM cob_t_build_verification cbv inner join cob_t_wo_build_verifi_req cwbvr on cbv.id=cwbvr.buildverificationid
                and upper(cbv.type)='AUDIT' and cwbvr.esn='90003971' and cbv.workstation='42700'"""
    rtn = ora.execute(sql)
        
    row = rtn.fetchone()
        
    if row != None:
        if row[0] =='COMPLETE':
            auditstatus = 'P'
        else:
            auditstatus = 'F'
        print row[0]
            
        sql = "select mt_f_serialno_test_audit('90004241','%s','audit','42701')" %(auditstatus)
        rtn = db.execute(sql)
        print "*****************"
        print rtn.rowcount
        print "****************************************"

test()
    
    
    
if __name__ == "__main__":
    
    run()
    #esn = '90000641'
    
    #dbtest(esn)
    
    
    
