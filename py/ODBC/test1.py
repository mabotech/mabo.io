




import pyodbc

pyodbc.pooling=False

def test():

    ds_string = """DSN=Opera5;UID=sa;PWD=Py03thon"""

    conn = pyodbc.connect(ds_string)

    cursor = conn.cursor()

    sql = """select * FROM [Opera5323N].[dbo].[Allarmi]"""
    
    x = cursor.execute(sql)    
    
    for i in x:
        print i[0],i[1],i[2]
        
    cursor.close()
    del cursor
    conn.close()

def main():
    test()
    
    
if __name__ == "__main__":
    main()