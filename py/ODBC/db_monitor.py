
import socket
import gevent

import sqlalchemy.pool as pool

import pyodbc
pyodbc.pooling=False

from central_config import Config

conf = Config("config.toml").config


def getconn():
    """ get db connection """
    ds_string = conf["app"]["ds_string"] #"""DSN=MSSQL1;UID=sa;PWD=Py03thon"""

    conn = pyodbc.connect(ds_string)
    
    return conn

class DBMonitor(object):
    
    def __init__(self):
        
        mypool = pool.QueuePool(getconn, \
            max_overflow=conf["app"]["max_overflow"], \
            pool_size=conf["app"]["pool_size"])

        # get a connection
        self.conn = mypool.connect()

        # use it
        self.cursor = self.conn.cursor()

    
    def check(self):
        """
        check db
        """
        sql = conf["app"]["sql"]# """select * FROM [msdb].[dbo].[backupfile]"""

        x = self.cursor.execute(sql)

        for i in x:
            print i[0],i[1],i[2]
            
    
    def post(self):
        """ post query value to redis (lus script)"""
        
        pass            
    
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
            monitor.check()
        
            gevent.sleep(3)
            
            if reconn <3:
                raise(Exception("test ex"))
            
        except Exception as ex:
            
            """ reconnect """
            print(ex)
            print ("reconnecting... ")
            del monitor
            
            monitor = DBMonitor()   
            
            reconn = reconn + 1
            
            gevent.sleep(1)
    
if __name__ == "__main__":
    
    main()