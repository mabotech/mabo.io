import cv2
import numpy as np



from mabopy.config.load_config import LoadConfig

import cvlib

conf = LoadConfig("config.toml").config

capture = cv2.VideoCapture(conf["app"]["camera_uri"])

i = 0

pt1 = (conf["app"]["crop_start"][0],conf["app"]["crop_start"][1])
w = conf["app"]["corp_width"]
pt2 = (pt1[0]+w,pt1[1]+w)


while True:
        
    ret, img_read = capture.read()
    
    print capture.get()

    img  = img_read[pt1[1]:pt2[1], pt1[0]:pt2[0]]
    
    #img = cv2.imread('N17.png',0)
    img = cv2.medianBlur(img,5)
    """
    try:
        cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    except Exception as ex:
        print ex
    """
    #gray = cv2.cvtColor (img, cv2.COLOR_BGR2GRAY)
    
    #gb_kernel = cv2.getGaborKernel((10, 10),18,10,16,0,0,cv2.CV_32F)
    
    #img = cv2.filter2D(gray, cv2.CV_32F, gb_kernel.transpose())
    
    #img = cv2.filter2D(gray, cv2.CV_8U, gb_kernel.transpose())
    """
    circles = cv2.HoughCircles(cimg,cv2.cv.CV_HOUGH_GRADIENT,1,150,
                                param1=150,param2=20,minRadius=0,maxRadius=100)

    circles = np.uint16(np.around(circles))
    
    for i in circles[0,:]:
        # draw the outer circle
        # if  i[2] >40:
            
        #cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        #cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)
        pass
    """
    cv2.imshow('detected circles',img_read)

    #cv2.imwrite("cd34.jpg", cimg)


    if cv2.waitKey(10) == 27:
        break
cv2.destroyAllWindows()