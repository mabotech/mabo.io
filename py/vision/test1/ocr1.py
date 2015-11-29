import tesseract
api = tesseract.TessBaseAPI()
api.SetOutputName("outputName");
api.Init("E:\\Tesseract-OCR\\test-slim","eng",tesseract.OEM_DEFAULT)
api.SetPageSegMode(tesseract.PSM_AUTO)
mImgFile = "eurotext.jpg"
pixImage=tesseract.pixRead(mImgFile)
api.SetImage(pixImage)
outText=api.GetUTF8Text()
print("OCR output:\n%s"%outText);
api.End()