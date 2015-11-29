
"""
detect circle
"""

import os,sys
import time
import traceback

import socket
import gevent
import toml
import numpy as np
import cv2

#import cvlib
from config import get_config
from redis_lua import RedisLua

conf_fn = os.sep.join(
    [os.path.split(os.path.realpath(__file__))[0], "config.toml"])

conf = get_config(conf_fn)["app"]



#conf = LoadConfig("config.toml").config

def supress(v, w):
    
    #v[0],v[1],
    #print v
    if  v[2] < w/2 and v[2] > 20:# and v[0] - v[2] >0 and v[1] - v[2]>0 :
        
        return True
        
rclient = RedisLua()

def save(x,y,r):    
    
    
    key = conf["redis_key"]
    
    if r > 0:
        
        
        data = 1
        result = conf["equipment_id"]
    
        rclient.save(key, result, data)
    else:
        pass
    

    
DEBUG = conf["DEBUG"]


def detect(img_read, pt1, pt2, w):

        try:

            t1 = time.time()
            
            crop_img  = img_read[pt1[1]:pt2[1], pt1[0]:pt2[0]]
            
            distance = conf["distance"]
            
            #skp, tkp = cvlib.findKeyPoints(crop_img , target, distance)
 
            crop_img = cv2.medianBlur(crop_img,3)
            
            gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

            circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 
                          conf["dp"],#29, ## dp
                          conf["minDist"],#100, ## minDist
                          conf["param1"],#param1=70, 
                          conf["param2"],#param2=80, ## 
                          conf["minRadius"],#minRadius=20,
                          conf["maxRadius"]) #maxRadius=0)

            j = 0
            
            cv2.rectangle(img_read, pt1, pt2, (0,255,0))
            
            if DEBUG == "false":
                
                if circles == None:
        
                    #print "None."
                    save(0,0,0)
                    return 0
                    
                else:
                    
                    circles = np.uint16(np.around(circles))
                
                    save(circles)
                
                    return 1                
                
            
            if circles == None:
                #print "."
                cv2.imshow("camera", img_read)
                save(0,0,0)
            else:                
                
                circles = np.uint16(np.around(circles))
                
                x = circles[0][0][0]
                y = circles[0][0][1]
                r = circles[0][0][2]
                save(x,y,r)
                for i in circles[0,:]:
                    
                    if supress(i, w):
                        j = j + 1
                      
                        cv2.circle(img_read,(pt1[0]+i[0],pt1[1]+i[1]),i[2],(0,255,0),2)
                        cv2.circle(img_read,(pt1[0]+i[0],pt1[1]+i[1]),2,(0,0,255),3)                       
                        
                        #cp = [ i[0], i[1] ]
                        
                        #print cp
                        
                cv2.imshow("camera", img_read)
            
        except Exception as ex:
            #print(ex)
            #print(traceback.format_exc())
            pass
            #gevent.sleep(3)
            #continue    
    
    
def main():
    
    #print conf
    
    #db = RedisLua()

    #target = cv2.imread(conf["target"])#sys.argv[2])
    
    #capture = cv2.VideoCapture(0)    
    capture = cv2.VideoCapture(conf["camera_uri"])
    
    #print(dir(capture))
    
    #capture.set(cv2.cv.CV_CAP_PROP_FPS, 50)
    
    k = 0
    
    pt1 = (conf["crop_start"][0],conf["crop_start"][1])
    w = conf["corp_width"]
    
    pt2 = (pt1[0]+w,pt1[1]+w)
    
    cp = [0,0]
    t = time.time()
    
    while True:
        
        k = k +1
        
        #time.sleep(0.1)
        #print capture.get(cv2.cv.CV_CAP_PROP_FPS)
    
        #v = int( capture.get(cv2.cv.CV_CAP_PROP_POS_FRAMES) )
        #print v
        #ret = True
        

        ret, img_read = capture.read() #cv.QueryFrame(capture)
        
        #if not capture.grab():
        #    break
            
        #img_read = capture.retrieve()

        #print type(img_read)
        
        #continue
            
        if k % 5 != 0:
            #continue
            pass
        
        if ret == False:
            #print ret,
            time.sleep(0.1)
        
        t2 = time.time()
        
        if t2 - t > 1:
            t = t2       
        
            detect(img_read, pt1, pt2, w)
        
        #cv2.waitKey(1000)
        
        if cv2.waitKey(10) == 27:
            
            break

    
    
    
if __name__ == "__main__":
    
    main()
