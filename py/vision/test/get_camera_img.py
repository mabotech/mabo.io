
import time

import socket

import gevent


import urllib2


def main():
    # create a password manager
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()

    # Add the username and password.
    # If we knew the realm, we could use it instead of None.
    top_level_url = "http://192.168.1.58"

    password_mgr.add_password(None, top_level_url, "admin", "")

    handler = urllib2.HTTPBasicAuthHandler(password_mgr)

    # create "opener" (OpenerDirector instance)
    opener = urllib2.build_opener(handler)

    # use the opener to fetch a URL
    a_url = "http://192.168.1.58/auto.jpg"


    for i in range(0, 3):
        
        fn = "a%s.jpg" %(i)    
        

        with open(fn, "wb") as fh:
            start = time.time()
            img = opener.open(a_url).read()
            print "%.3f" %(time.time() - start)
            fh.write(img)
            
            
        gevent.sleep(1)



