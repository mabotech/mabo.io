

data = [(u'BLI.42700M.Flag', True, 'Good', '10/30/13 01:26:46'), (u'BLI.42700M.PalletNo', u'P001', 'Good', '10/30/13 01:26:46'), (u'BLI.42700M.SerialNo', u'90000861', 'Good', '10/30/13 01:26:46'), (u'BLI.42700M.TestCell', u'TC01', 'Good', '10/30/13 01:26:46'), (u'BLI.42700M.TestCount', 0, 'Good', '10/30/13 01:26:46'), (u'BLI.42700M.TestStatus', 0, 'Good', '10/30/13 01:26:46'), (u'BLI.42700M.TestTypeRun1', 0, 'Good', '10/30/13 01:26:46'), (u'BLI.42700M.TestTypeRun2', 0, 'Good', '10/30/13 01:26:46'), (u'BLI.42700M.TestTypeRun3', 0, 'Good', '10/30/13 01:26:46')]



def get_obj(data):
    obj = {}

    for val in data:
        
        #print val
        
        if val[2] != "Good":
            
            raise(Exception("Not good"))
            
        print val[0], val[1], val[2]
        
        key =  val[0].split(".")[-1]
            
        obj[key] = val[1]
        
    return obj
    

print get_obj(data)