

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):

     #read frame from capture
     img = cap.read()

     ##############################
     # here do the whole stuff with circles and your actual image
     ##############################

     cv2.imshow('show image', img)

     #exit condition to leave the loop
     k = cv2.waitKey(30) & 0xff
     if k == 27:
          break

cv2.destroyAllWindows()
cap.release()

