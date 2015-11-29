
import numpy as np
import cv2

cap = cv2.VideoCapture("rtsp://192.168.1.58:554")

#cap.open(0)
print cap.get(3) 
print cap.get(4)
import time
time.sleep(3)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    print ret
    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    try:
        cv2.imshow('frame',frame)
    except:
        pass
    time.sleep(0.1)
    if cv2.waitKey(10) == 27:
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()