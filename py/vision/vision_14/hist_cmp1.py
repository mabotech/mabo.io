#

#import cv2

import cv2.cv as cv

def compute_histogram(src, bins = 255 ):
    hist = cv.CreateHist([255], cv.CV_HIST_ARRAY, ranges=[(0, 256)])
    cv.CalcHist([src], hist)      #compute histogram
    cv.NormalizeHist(hist, 1.0)   #normalize hist
    return hist

def test():
    #start = time.time()
    
    #
    src1 =  cv.LoadImage("target_all_nl1.png", 0)
    src2 =  cv.LoadImage("target_all.png", 0)
    

    # crop area
    pt1 = (100, 100)
    pt2 = (200, 200)
    
    #get img size and compare
    
    
    
    # convert cvMat to IplImage
    crop1  = cv.GetImage(src1[pt1[1]:pt2[1], pt1[0]:pt2[0]])
    crop2  = cv.GetImage(src2[pt1[1]:pt2[1], pt1[0]:pt2[0]])
    
    
    # save image
    cv.SaveImage("c1.jpg",crop1)
    cv.SaveImage("c2.jpg",crop2)
    
    print type(crop2)
    print type(src2)
    #cv2.GetMat
    
    # compute
    
    hist1 = compute_histogram(crop1)
    hist2 = compute_histogram(crop2)

    # compare
    sc = cv.CompareHist(hist1, hist2, cv.CV_COMP_CHISQR)

    print sc    
    
    # val
    # turn off light.
    
if __name__=="__main__":
    test()