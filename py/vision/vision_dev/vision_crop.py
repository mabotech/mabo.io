
import time

import socket

import gevent



import sys

import cv2

from load_config import LoadConfig

import cvlib

conf = LoadConfig("config/vision.toml").config

"""

def match():
    img = cv2.imread("box_in_scene2.png")#sys.argv[1])
    temp = cv2.imread("box4.png")#sys.argv[2])
    try:
    	dist = int(sys.argv[3])
    except IndexError:
    	dist = 200
    try:
    	num = int(sys.argv[4])
    except IndexError:
    	num = -1
    skp, tkp = findKeyPoints(img, temp, dist)
    newimg = drawKeyPoints(img, temp, skp, tkp, num)
    cv2.imshow("image", newimg)
    cv2.waitKey(0)
"""    
    
def main():
    
    print conf

    target = cv2.imread(conf["app"]["target"])#sys.argv[2])
    
    #print type(target)
    
    #cv2.NamedWindow("camera", 1)
    

    
    #capture = cv2.VideoCapture(0)
    capture = cv2.VideoCapture(conf["app"]["camera_uri"])
    
    i = 0
    
    pt1 = (conf["app"]["crop_start"][0],conf["app"]["crop_start"][1])
    w = conf["app"]["corp_width"]
    pt2 = (pt1[0]+w,pt1[1]+w)
    
    debug = 1# conf["app"]["debug"]

    while True:
        i = i +1
        #if i > 200:
        #    i = 0
        print i
        ret, img_read = capture.read() #cv.QueryFrame(capture)
        
        
        
        if i == 1:

                pass
        
        if ret == False:
            raise(Exception("can't connect camera"))
        #mat=cv2.GetMat(img)
        #img_p = np.asarray(mat)
        
        #img_p  = cv.CreateImage(cv.GetSize(img),cv.IPL_DEPTH_8U,1)
        
        #print dir(img)
        
        """
        im_gray  = cv.CreateImage(cv.GetSize(img),cv.IPL_DEPTH_8U,1)
        cv.CvtColor(img,im_gray,cv.CV_RGB2GRAY)
        
        
        # Sobel operator
        dstSobel = cv.CreateMat(im_gray.height, im_gray.width, cv.CV_32FC1)
        # Sobel(src, dst, xorder, yorder, apertureSize = 3)
        cv.Sobel(im_gray,dstSobel,1,1,3)
        """
        #print ret
        try:
            
            # skp: source key points, tkp: target key points
            t1 = time.time()
            

            
            #img[200:400, 100:300] # Crop from x, y, w, h -> 100, 200, 300, 400
            #im[y1:y2, x1:x2]
            crop_img  = img_read[pt1[1]:pt2[1], pt1[0]:pt2[0]]
            
            #print(len(crop_img))
            distance = conf["app"]["distance"]
            
            skp, tkp = cvlib.findKeyPoints(crop_img , target, distance)
            
            if skp == None:
                print("skp is none")
                continue
            else:

                print "==" * 20
                print "time:[%.3f]" %(time.time() - t1)
                print "skp", len(skp)#, skp
                print "tkp",len(tkp)#, tkp

            
            if debug:
            
                newimg = cvlib.drawKeyPoints(img_read, target, skp, tkp, pt1, pt2, -1)
            
                cv2.imshow("camera", newimg)
                
            #gevent.sleep(1)
            
        except Exception as ex:
            print(ex)
            #gevent.sleep(3)
            continue
        #cv.ShowImage('camera', newimg)
        
        
        # image smoothing and subtraction
    #    imageBlur = cv.CreateImage(cv.GetSize(im_gray), im_gray.depth, im_gray.nChannels)
    #    # filering the original image
    #    # Smooth(src, dst, smoothtype=CV_GAUSSIAN, param1=3, param2=0, param3=0, param4=0)
    #    cv.Smooth(im_gray, imageBlur, cv.CV_BLUR, 11, 11)
    #    diff = cv.CreateImage(cv.GetSize(im_gray), im_gray.depth, im_gray.nChannels)
    #    # subtraction (original - filtered)
    #    cv.AbsDiff(im_gray,imageBlur,diff)
    #    cv.ShowImage('camera', diff)
        
        if cv2.waitKey(10) == 27:
            break
            
        #gevent.sleep(0.1)
        
    # cv2.destroyWindow("camera")
    
    
    
if __name__ == "__main__":
    
    main()
