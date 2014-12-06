# -*- coding: utf-8 -*-

"""
object detector
"""

import os
import sys
import time

import collections
#import math

import threading
import multiprocessing

import socket
import gevent


Result = collections.namedtuple("Result", "id count time")

def report(message="", error=False):
    """ print message in multiprocessing script """
    message = str(message)
    
    if len(message) >= 70 and not error:
        message = message[:67] + "..."
    sys.stdout.write("\r{:70}{}".format(message, "\n" if error else ""))
    sys.stdout.flush()

def create_processes(results):    
    
    for id in [1,2,3]:
        
        process = multiprocessing.Process(target=worker, args=(id, results))
        process.daemon = True
        process.start()

def worker(id, results):
    
    while True:
        
        try:
            try:
                result = detect_one(id)
                results.put(result)
            except Exception as err:
                report(err)  
            
            #raise Exception("Exception in worker")
            
        except Exception as exc:
            report(exc)
        
        finally:
            gevent.sleep(3)
        
def detect_one(id):
    """ work here """
    t1 = time.time()
    gevent.sleep(0.2)
    t2 = time.time() - t1
    pid =  os.getpid()
    count = pid
    report("in process:%s"%(id))
    return Result(id, count, t2)
    
def getter(results):
    """get result from queue"""
    
    while True:
        
        result = results.get()
        report("in thread:%s [%s]" %(result.count, result.id))    
        
def main():
    

    report("starting...")
    
    report(multiprocessing.cpu_count())
    
    results = multiprocessing.Queue()
    
    #create processes
    create_processes(results)
    
    # create threads
    t = threading.Thread(target=getter, args=(results,))
    t.start()


if __name__ == "__main__":
    main()
