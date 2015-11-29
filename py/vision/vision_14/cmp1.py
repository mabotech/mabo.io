#

import cv2

import cv2.cv as cv

def compute_histogram(src, bins = 255 ):
    hist = cv.CreateHist([255], cv.CV_HIST_ARRAY, ranges=[(0, 256)])
    cv.CalcHist([src], hist)      #compute histogram
    cv.NormalizeHist(hist, 1.0)   #normalize hist
    return hist

def test():
    #start = time.time()
    src1 = cv.GetMat(cv.LoadImage("d1.png", 0))
    src2 = cv.GetMat(cv.LoadImage("d2.png", 0))
    

    pt1 = (100, 100)
    pt2 = (200, 200)
    
    crop1  = src1[pt1[1]:pt2[1], pt1[0]:pt2[0]]
    crop2  = src2[pt1[1]:pt2[1], pt1[0]:pt2[0]]
    
    #cv2.GetMat
    
    hist1 = compute_histogram(crop1)

    hist2 = compute_histogram(crop2)
    
    sc = cv.CompareHist(hist1, hist2, cv.CV_COMP_CHISQR)

    print sc
    
    # turn off light.
    
if __name__=="__main__":
    test()