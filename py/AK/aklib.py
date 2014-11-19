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
    
    return data
    

def astz(data):    
    """
    [X] ASTZ - Request actual status
    """
    
    return data

def avfi(data):
    """
    AVFI - Request actual speed and motor force
    """
    print ("data: %s" % (data) )
    
    return data
    
    
def aweg(data):
    """
    AWEG - Request the distance traveled 
    """
    
    # business logic here
    # compare with history data in redis
    # get equipment status and send to heka
    
    print ("data: %s" % (data) )
    
    return data    

def awrt(data):
    """
    [X] AWRT - Request actual values
    """
    
    return data
    