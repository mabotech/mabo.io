#
import numpy as np
#import cv2
import cv2

import cv2.cv as cv

def compute_histogram(src, bins = 255 ):
    #hist = cv2.createHist([255], cv.CV_HIST_ARRAY, ranges=[(0, 256)])
    #hist = cv2.calcHist([src], [0])      #compute histogram
    #cv.NormalizeHist(hist, 1.0)   #normalize hist
    
    
    hist_item = cv2.calcHist([src],[0],None,[256],[0,255])
    cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
    
    return hist_item

def test():
    #start = time.time()
    
    #
    src1 =  cv.LoadImage("all.png", 0)
    src2 =  cv.LoadImage("dark3.png", 0)
    

    # crop area
    w = 100
    pt1 = (535, 60)
    pt2 = (pt1[0]+w, pt1[1]+w)
    
    
    print pt1
    print pt2
    
    #get img size and compare
    
    
    
    # convert cvMat to IplImage
    crop1 = src1[pt1[1]:pt2[1], pt1[0]:pt2[0]]
    crop2 = src2[pt1[1]:pt2[1], pt1[0]:pt2[0]]
    
    crop3  = cv.GetImage(cv.GetSubRect(src1, (10, 10, 100, 100)) )
    crop4  = cv.GetImage(cv.GetSubRect(src2, (10, 10, 100, 100)) )
    
    
    # save image
    cv.SaveImage("c01.jpg",crop1)
    cv.SaveImage("c02.jpg",crop2)

    cv.SaveImage("c03.jpg",crop3)
    cv.SaveImage("c04.jpg",crop4)
    
    
    print type(src1)
    print type(crop3)
    #cv2.GetMat
    
    # compute
    #return 1
    hist1 = compute_histogram(crop3)
    hist2 = compute_histogram(crop4)

    # compare
    sc = cv.CompareHist(hist1, hist2, cv.CV_COMP_CHISQR)

    print sc    
    
    # val
    # turn off light.
    
if __name__=="__main__":
    test()