
import os, sys
import time

import socket
import gevent

import cv2

from visionlib import findKeyPoints, drawKeyPoints

import collections

from clib import report

Result = collections.namedtuple("Result", "device pid count cost")

DEBUG = False

def detector(device, results):
    """ worker """
    
    logo = cv2.imread("logo1.png")
    
    capture = cv2.VideoCapture(0)
    
    while True:
        
        try:
            try:
                result = detect_one(device, capture, logo)
                results.put(result)
            except Exception as err:
                report(err)  
            
            #raise Exception("Exception in worker")
            
        except Exception as exc:
            report(exc)
        
        finally:
            # sleep
            gevent.sleep(0.1)
            
        
        
def detect_one(device, capture, logo):
    """ work here """
    
    ret, img_p = capture.read()
    """
    
    gevent.sleep(0.2)
    
    
    """
    start = time.time()
    skp, tkp = findKeyPoints(img_p, logo, 20)
    
    if DEBUG:
        newimg = drawKeyPoints(img_p, logo, skp, tkp, -1)
                
        #cv2.imshow("camera", newimg)
        
        filename = "p%s.png" %(start)
        cv2.imwrite(filename, newimg)
    
    
    cost = "%.3f" %(time.time() - start)
    
    pid =  os.getpid()
    count = len(skp)
    report("count:%s"%(count))
    return Result(device, pid, count, cost)