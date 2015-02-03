
"""
get image by requests response.raw.read() 
and convert it to numpy.ndarray
"""

import numpy

from StringIO import StringIO

from PIL import Image

def main():
    
    """
    image = Image.open("a1422866084343.jpg")   # image is a PIL image 
    print image
    array = numpy.array(image)  
    """
    
    with open("a1422866084343.jpg","rb") as fileh:
        
        s = fileh.read()
        
        image_file = StringIO(s)
        
        #print dir(image_file)
        
        image = Image.open(image_file)
        
        array = numpy.array(image) 
        
        print type( array )
    
if __name__ == "__main__":
    
    main()