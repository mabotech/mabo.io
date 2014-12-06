import cv2.cv as cv
import tesseract

import time

start = time.time()

image=cv.LoadImage("app2.jpg", cv.CV_LOAD_IMAGE_GRAYSCALE)

api = tesseract.TessBaseAPI()
api.Init("E:\\Tesseract-OCR\\test-slim","eng",tesseract.OEM_DEFAULT)
#api.SetPageSegMode(tesseract.PSM_SINGLE_WORD)

api.SetPageSegMode(tesseract.PSM_AUTO)
tesseract.SetCvImage(image,api)
text=api.GetUTF8Text()
conf=api.MeanTextConf()
image=None

print "text:",text
print "conf:",conf 

#api.SetPageSegMode(tesseract.PSM_AUTO)
mImgFile = "app3.jpg"


result = tesseract.ProcessPagesWrapper(mImgFile,api)
print "result(ProcessPagesWrapper)=",result
print time.time() - start
#api.ProcessPages(mImgFile,None, 0, result)
#print "abc"
result = tesseract.ProcessPagesFileStream(mImgFile,api)
print "result(ProcessPagesFileStream)=",result
print time.time() - start
result = tesseract.ProcessPagesRaw(mImgFile,api)
print "result(ProcessPagesRaw)",result
print time.time() - start
f=open(mImgFile,"rb")
mBuffer=f.read()
f.close()
result = tesseract.ProcessPagesBuffer(mBuffer,len(mBuffer),api)
mBuffer=None
print "result(ProcessPagesBuffer)=",result
print time.time() - start