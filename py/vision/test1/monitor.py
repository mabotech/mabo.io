# -*- coding: utf-8 -*-

"""
object detector
"""

import os
import sys
import time

#import cv2

from feature_detector import detector

#import math

import threading
import multiprocessing

import socket
import gevent

from clib import report

def create_processes(results):    
    """ create processes"""
    
    for device in [1]:
        
        process = multiprocessing.Process(target=detector, args=(device, results))
        process.daemon = True
        process.start()
    
def monitor(results):
    """get result from queue"""
    
    while True:
        
        try:
            result = results.get()
            report("result.count:%s, cost:[%s]" %(result.count, result.cost))
            #newimg = result.cost
            #cv2.imshow("camera", newimg)
            
            #cv2.imwrite("a1.png", newimg)
            
            #report("in thread:%s [%s]" %(result.count, result.cost))
        except Exception as exc:
            report(str(exc))
        
def main():
    """ main """

    report("starting...")
    
    report(multiprocessing.cpu_count())
    
    results = multiprocessing.Queue()
    
    #create processes
    create_processes(results)
    
    # create threads
    t = threading.Thread(target=monitor, args=(results,))
    t.start()


if __name__ == "__main__":
    main()
