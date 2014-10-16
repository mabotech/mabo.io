# -*- encoding: utf-8 -*-

#import pyodbc

#pyodbc.pooling=False

from pool import init_pool

#from pool import DBPool

from singleton import Singleton

class Database:
    
    """
    
    """
    
    __metaclass__ = Singleton
    
    def __init__(self, ds_string=""):
        
        
        
        DBPool = init_pool(ds_string)
        
        conn = DBPool.connect()  
        
        self.cursor = conn.cursor()
        
        """
        
        try:
            
            db_string = 'DSN=flexnet;Database=flexnet;UID=flxuser;PWD=flxuser'
            
            self.cnxn = pyodbc.connect(db_string)
            self.cursor = self.cnxn.cursor()
        except Exception, e:
            print e[1]
            raise Exception('error')
        """

    def execute(self, sql):
        #print sql
        return self.cursor.execute(sql)
        
    def fetchall(self):
        rows = self.cursor.fetchall()
        return rows

    def fetchone(self):
        row = self.cursor.fetchone()
        return row
        
if __name__ == '__main__':
    
    ds_string = 'DSN=fn183;Database=gf6flexnet_prod;UID=cimuser;PWD=cimplus'
    
    db = Database(ds_string)
    
    sql = """
        select mi2.name, mi.name as miname, tt.short, mi.operationid from menu_item mi 
inner join menu_item mi2 on mi.parentid = mi2.id
inner join text_translation tt on tt.textid = mi.textid and tt.languageid = 1033
--left join text_translation tt2 on tt2.textid = mi2.textid and tt2.languageid = 1033
where
mi.showmobile = 1  and mi.operationid > 1000
    """
    
    db.execute(sql)
    
    rtn = db.fetchall()
    
    for item in rtn:
        print item
    
