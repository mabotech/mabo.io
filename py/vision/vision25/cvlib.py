

import cv2
import numpy as np

import itertools

def findKeyPoints(img, template, distance=200):
    """ find key points in image """
    
    # SIFT
    FEATURE_DETECTOR = "SIFT" #"SURF" # "SIFT"
    detector = cv2.FeatureDetector_create(FEATURE_DETECTOR)
    descriptor = cv2.DescriptorExtractor_create(FEATURE_DETECTOR)
    
    #print(dir(descriptor))
    #print descriptor.paramType()
    skp = detector.detect(img)
    skp, sd = descriptor.compute(img, skp)

    if sd == None:
            return None, None

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
    
    #print descriptor.getParams()

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

def drawKeyPoints(img, template, skp, tkp, pt1, pt2, num=-1):
    h1, w1 = img.shape[:2]
    h2, w2 = template.shape[:2]
    nWidth = w1+w2
    nHeight = max(h1, h2)
    hdif = (h1-h2)/2
    
    pt11 = (pt1[0]+w2, pt1[1])
    pt22 = (pt2[0]+w2, pt2[1])
    
    newimg = np.zeros((nHeight, nWidth, 3), np.uint8)
    newimg[hdif:hdif+h2, :w2] = template
    newimg[:h1, w2:w1+w2] = img

    maxlen = min(len(skp), len(tkp))
    if num < 0 or num > maxlen:
        num = maxlen
    for i in range(num):
        
        pt_a = (int(tkp[i].pt[0]), int(tkp[i].pt[1]+hdif))
        
        pt_b = (int(skp[i].pt[0]+w2)+pt1[0], int(skp[i].pt[1])+pt1[1])
        
        cv2.line(newimg, pt_a, pt_b, (255, 0, 0))
    
    cv2.rectangle(newimg, pt11, pt22, (0,255,0))
        
    return newimg