

import toml
import json


import socket
import gevent

import sqlalchemy.pool as pool

import pyodbc
pyodbc.pooling=False

from multi_logging import get_logger
from redis_lua import RedisLua



#from central_config import Config

#conf = Config("config.toml").config


conf_fn = "config/db_monitor.toml"

with open(conf_fn, "r") as conf_fh:

    cfg = toml.loads(conf_fh.read())

    conf = cfg["app"]

with open(conf["logging_config"], "r") as fh:
    
    json_str = fh.read() 

conf_json = json.loads(json_str)

logger = get_logger(conf["log_base"], conf["app_name"], conf_json)

logger.debug(conf)
logger.debug("debug")

#import sys

#sys.exit(1)


def getconn():
    """ get db connection """
    ds_string = conf["db"]["ds_string"] #"""DSN=MSSQL1;UID=sa;PWD=Py03thon"""

    conn = pyodbc.connect(ds_string)
    
    return conn

class DBMonitor(object):
    
    def __init__(self): 

        self.connected = 0
        self.closed = 0
        self.db = RedisLua()

    def connect(self):   
        
        logging.debug("connect db...")
        
        try:
            
            self.mypool = pool.QueuePool(getconn, \
                max_overflow=conf["db"]["max_overflow"], \
                pool_size=conf["db"]["pool_size"])

            # get a connection
            self.conn = self.mypool.connect()

            # use it
            self.cursor = self.conn.cursor()  
            
            self.connected = 1
            
        except Exception as ex:
            self.connected = 0
        
        
    def check_conn(self):
        
        if self.connected == 0:
            
            self.connect()
            
        if self.connected == 0:
            
            return 0
            
        else:
            
            self.connected = 1
            return 1
    
    
    def query(self):
        """
        check db
        """
        sql = conf["db"]["sql"]# """select * FROM [msdb].[dbo].[backupfile]"""

        rows = self.cursor.execute(sql)

        row = rows.fetchone()
        logging.debug(row[0])
        self.process(row)
        
        #print(row)
        """
        for i in x:
            print i[0],i[1],i[2]
        """
    
    def process(self, row):
        """ save query value to redis (lus script)
        if EInit < now and ETest == None and status = 'start':
            data = 1
        elif  EInit < now and ETest < Now and status in ['finished', 'cancel']
            data = 2
        """
        #print (row)
        
        key = conf["equipment_id"]
        
        result = "test start" 
        result = "test end" 
        
        data = 1  ## 1
        
        self.db.save(key, result, data)
    
    def __del__(self):
        """
        release db connection to pool
        """
        self.cursor.close()
        del self.cursor
        self.conn.close()

        
        
def main():
    """ run """
    
    monitor = DBMonitor()
    
    reconn = 0
    
    while True:
        
        try:
            
            
            monitor.check_conn()
            
            #print monitor.connected
            
            if monitor.connected == 0:
                
                # sleep
                gevent.sleep(conf["reconnection_interval"])
                
            else:
                monitor.query()
            
                gevent.sleep(conf["ticker_interval"])
            
            #if reconn <3:
            #    raise(Exception("test ex"))
            
        except Exception as ex:
            
            """ reconnect """
            print(ex)
            #print ("reconnecting... ")
            
            #del monitor
            
            #monitor = DBMonitor()   
            
            #reconn = reconn + 1
            
            #gevent.sleep( conf["ticker_interval"])
    
if __name__ == "__main__":
    
    main()