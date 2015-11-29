# -*- coding: utf-8 -*-

"""

BEP
MAHA
HARIBA
AVL

"""

def afwd(data):
    """
    AFWD - Request 4WD status
    """
    return data

def akon(data):
    """
    AKON - Request data
    """
    return data

def astf(data):

    """
    [X] ASTF - Request active faults
    """
    #print ("data: %s" % (data) )
    return data
    

def astz(data):    
    """
    [X] ASTZ - Request actual status
    
    STBY (dyno stopping) or 
        SSIM (road load) or
        SMTR (constant speed) or
        SRPM (constant RPM) or
        SKZK (constant motor force)    
    """
    
    responds = data.split(" ")
    if len(responds) > 2:
        if responds[1] == 'STBY':
            state = 0
        elif responds[1] in ["SSIM","SMTR","SRPM","SKZK"]:
            state = 1
        else:
            print responds[1]
            state = 2
    else:
        state = 3
        
    return state

def avfi(data):
    """
    AVFI - Request actual speed and motor force
    """
    #print ("data: %s" % (data) )
    
    return data
    
    
def aweg(data):
    """
    AWEG - Request the distance traveled 
    """
    
    # business logic here
    # compare with history data in redis
    # get equipment status and send to heka
    
    #print ("data: %s" % (data) )
    
    return data    

def awrt(data):
    """
    [X] AWRT - Request actual values
    """
    
    return data
    
    
def test():
    
    data = 'SMAN STBY SLIR SVOR SBEI N/A '
    
    print astz(data)
    
    
if __name__ == "__main__":
    test()