import cv2
import cv2.cv as cv
import numpy as np

print("11")

img = cv2.imread("target.jpg")
print("12")
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
print("13")
#circles = cv2.HoughCircles(gray,cv.CV_HOUGH_GRADIENT, 1, 10)
circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 75)
print("14")
