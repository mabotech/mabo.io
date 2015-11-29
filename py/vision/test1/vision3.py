
import time

import socket

import gevent

import cv2.cv as cv

import cv2
import numpy as np
import itertools
import sys



def findKeyPoints(img, template, distance=200):
    """ find key points in image """
    
    # SIFT
    FEATURE_DETECTOR = "SIFT" #"SURF" # "SIFT"
    detector = cv2.FeatureDetector_create(FEATURE_DETECTOR)
    descriptor = cv2.DescriptorExtractor_create(FEATURE_DETECTOR)

    skp = detector.detect(img)
    skp, sd = descriptor.compute(img, skp)

    tkp = detector.detect(template)
    tkp, td = descriptor.compute(template, tkp)

    flann_params = dict(algorithm=1, trees=4)
    flann = cv2.flann_Index(sd, flann_params)
    idx, dist = flann.knnSearch(td, 1, params={})
    del flann

    dist = dist[:,0]/2500.0
    dist = dist.reshape(-1,).tolist()
    idx = idx.reshape(-1).tolist()
    indices = range(len(dist))
    indices.sort(key=lambda i: dist[i])
    dist = [dist[i] for i in indices]
    idx = [idx[i] for i in indices]
    skp_final = []
    for i, dis in itertools.izip(idx, dist):
        if dis < distance:
            skp_final.append(skp[i])

    flann = cv2.flann_Index(td, flann_params)
    idx, dist = flann.knnSearch(sd, 1, params={})
    del flann

    dist = dist[:,0]/2500.0
    dist = dist.reshape(-1,).tolist()
    idx = idx.reshape(-1).tolist()
    indices = range(len(dist))
    indices.sort(key=lambda i: dist[i])
    dist = [dist[i] for i in indices]
    idx = [idx[i] for i in indices]
    tkp_final = []
    for i, dis in itertools.izip(idx, dist):
        if dis < distance:
            tkp_final.append(tkp[i])

    return skp_final, tkp_final

def drawKeyPoints(img, template, skp, tkp, num=-1):
    h1, w1 = img.shape[:2]
    h2, w2 = template.shape[:2]
    nWidth = w1+w2
    nHeight = max(h1, h2)
    hdif = (h1-h2)/2
    newimg = np.zeros((nHeight, nWidth, 3), np.uint8)
    newimg[hdif:hdif+h2, :w2] = template
    newimg[:h1, w2:w1+w2] = img

    maxlen = min(len(skp), len(tkp))
    if num < 0 or num > maxlen:
        num = maxlen
    for i in range(num):
        pt_a = (int(tkp[i].pt[0]), int(tkp[i].pt[1]+hdif))
        pt_b = (int(skp[i].pt[0]+w2), int(skp[i].pt[1]))
        cv2.line(newimg, pt_a, pt_b, (255, 0, 0))
    return newimg


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
    
    
def main():

    logo = cv2.imread("logo1.png")#sys.argv[2])
    print type(logo)
    
    #cv2.NamedWindow("camera", 1)
    
    
    #capture = cv2.VideoCapture(0)
    capture = cv2.VideoCapture("rtsp://192.168.1.58:554")
    print dir(capture)
    
    #return 1
    while True:
        #o = capture.open("rtsp://192.0.0.64:554/?network-caching=1000")
        #v = capture.isOpened()
        #print o, v
        ret, img_p = capture.read() #cv.QueryFrame(capture)
        #ret = cv.QueryFrame(capture)
        #gevent.sleep(1)
        print ret
        #continue
        #mat=cv.GetMat(img_p)
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
        try:
            
            # skp: source key points, tkp: target key points
            t1 = time.time()
            skp, tkp = findKeyPoints(img_p, logo, 20)
            print "==" * 20
            print "time:",time.time() - t1, ret
            print "skp", len(skp)#, skp
            print "tkp",len(tkp)#, tkp
            
            newimg = drawKeyPoints(img_p, logo, skp, tkp, -1)
            
            cv2.imshow("camera", newimg)
        except Exception as ex:
            print("err:",ex)
            gevent.sleep(0.01)
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
        
    cv.DestroyWindow("camera")
    
    
    
if __name__ == "__main__":
    
    main()