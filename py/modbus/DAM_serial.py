

import time
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)


class RS232(object):
    
    def __init__(self):
        pass
        
    def open(self):
        pass
        
    def write(self):
        pass
        
    def read(self):
        pass
        
    def close(self):
        pass
    

def parse(val):
    
    val = val.strip()
    v =val.split("+")
    
    for item in v[1:]:
        print float(item)
    print "========"




def main():

    
    ser = serial.Serial(
        port='COM4',
        baudrate=9600,
        parity=serial.PARITY_NONE, #PARITY_ODD,
        stopbits=serial.STOPBITS_ONE ,  #STOPBITS_TWO,
        bytesize=serial.EIGHTBITS #SEVENBITS
    )

    #ser.open()
    print ser.isOpen()

    print 'COM4'



    while 1 :
            # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
            
            ser.write('#01\r')
            #print ser.read()

            out = ''
            # let's wait one second before reading output (let's give device time to answer)
            time.sleep(1)
            
            while ser.inWaiting() > 0:
                #print ser.inWaiting() 
                out += ser.read()

            if out != '':
                #print out                
                parse(out)
        
        
if __name__ == "__main__":
        main()
        
        