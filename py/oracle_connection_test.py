

from flask.config import Config

from mabolab.core.global_obj import Global

CENTRAL_CONFIG = 'C:/MTP/mabotech/maboss1.3.0/maboss/conf/maboss_config.py'

settings = Config("")

settings.from_pyfile(CENTRAL_CONFIG)

settings['APP_NAME'] = "monitor_bli"

g = Global(settings)

db = g.get_db('postgresql')

ora = g.get_db('oracle')

log = g.get_logger()



def dbtest(serialno):
    
    sql = """select status, lastupdateon from cob_t_serial_no_workstation 
where serialno = '%s'  and workstation = '42700' 
order by id desc""" % (serialno)

    rtn = ora.execute(sql)
    
    print rtn.fetchone()
    
if __name__ == '__main__':
    
    esn = '90000641'
    dbtest(esn)