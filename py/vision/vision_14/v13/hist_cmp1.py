#

#import cv2
import cv2

import cv2.cv as cv

def compute_histogram(src, bins = 255 ):
    hist = cv.CreateHist([255], cv.CV_HIST_ARRAY, ranges=[(0, 256)])
    cv.CalcHist([src], hist)      #compute histogram
    cv.NormalizeHist(hist, 1.0)   #normalize hist
    return hist

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
    
    crop3  = cv.GetImage(crop1)
    crop4  = cv.GetImage(crop2)
    
    
    # save image
    cv.SaveImage("c01.jpg",crop1)
    cv.SaveImage("c02.jpg",crop2)
    
    print type(crop1)
    print type(crop2)
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