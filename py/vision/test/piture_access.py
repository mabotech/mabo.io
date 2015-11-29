
import requests
import shutil

from requests.auth import HTTPBasicAuth

import time

import numpy

url = "http://192.168.1.58/tmpfs/auto.jpg"

# Authorization:Basic YWRtaW46YWRtaW4=

import cv2

for i in xrange(0,1):

    r = requests.get(url, stream=True, auth=HTTPBasicAuth('admin', 'admin'))

    #print r

    t  = int(1000*time.time())

    if r.status_code == 200:
        with open("a%s.jpg" % (t), 'wb') as f:
            r.raw.decode_content = True
            #shutil.copyfileobj(r.raw, f)
            print("done")
            v =r.raw.read()
            print (v)
            """
            x = numpy.array(v).reshape(v.size[1], v.size[0], 3)
            print type(x)
            #print dir(x)
            #print x.tolist()
            
            t = cv2.imread(v)
            print t
            """
            f.write(v)
    else:
        print r.status_code