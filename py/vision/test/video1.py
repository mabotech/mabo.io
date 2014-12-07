
import socket
import gevent

import cv2


cap = cv2.VideoCapture("rtsp://192.168.1.58:554")

#cap = cv2.VideoCapture(0)

if cap.isOpened()==False:
 print cap
 print "cv2.VideoCapture.isOpened() ",cap.isOpened()
 #raise(Exception("err"))
 

while True:
    #cap = cv2.VideoCapture("rtsp://192.168.1.58:554")
    ret, im = cap.read()
    
    print ret
    
    if ret == True:
    
        cv2.imshow("video", im)
        #cv2.imwrite("abc.jpg", im)
        
        #break
    
    if cv2.waitKey(10) == 27:
        break
        
    gevent.sleep(3)