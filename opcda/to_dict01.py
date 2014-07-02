



x = ["ABC","ZXV","DD"]

y = [1,2,3]

def f(x1,y1):
    return x1, y1

print map(f, x, y)

if len(x) != len(y):
    raise Exception("array must align")
    
z = {}

for i in range(0, len(x)):
    z [ x[i] ] = y[i]
    

cols = """referenceid        int4 NULL,
lastupdateon       timestamp NULL,
lastupdatedby      varchar(40)  NULL,
createdon          timestamp NULL,
createdby          varchar(40)  NULL,
active             int2 default 1 NOT NULL,
rowversionstamp    int4 default 1 NOT NULL,"""

import datetime

for i in cols.split("\n"):
   # print i
    v = i.split(" ")
    print v[0]
    if i.count('timestamp') == 1:
        print v[0]
        z[ v[0] ] = " now() "
    else:
        z[ v[0]] = 'emp1'
    
print z
    
print "value='%(ZXV)s, %(createdon)s, '%(ABC)s', '%(createdby)s'  " % z







