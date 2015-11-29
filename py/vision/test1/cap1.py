

#import cv2.cv as cv

import cv2


vcap = cv2.VideoCapture("rtsp://192.168.2.58:554")

while(1):

    ret, frame = vcap.read()
    cv2.imshow('VIDEO', frame)
    cv2.waitKey(1)