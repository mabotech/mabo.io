
import os, sys
import time

import socket
import gevent

import collections

from clib import report

Result = collections.namedtuple("Result", "device count time")


def detector(device, results):
    """ worker """
    
    while True:
        
        try:
            try:
                result = detect_one(device)
                results.put(result)
            except Exception as err:
                report(err)  
            
            #raise Exception("Exception in worker")
            
        except Exception as exc:
            report(exc)
        
        finally:
            # sleep
            gevent.sleep(3)
        
def detect_one(device):
    """ work here """
    
    t1 = time.time()
    gevent.sleep(0.2)
    
    t2 = time.time() - t1
    
    pid =  os.getpid()
    count = pid
    report("in process:%s"%(device))
    return Result(device, count, t2)