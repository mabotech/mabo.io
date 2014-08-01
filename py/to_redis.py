

"""
save data to redis by call lua script.

if point value changed, trigger action.

lua script template

gevent pool for multi-point read

openopc, opc_client

"""

import time

import redis

import socket
import gevent

"""
import logbook

import toml


"""

"""
point:
    val:
    timestamp:
    status:
    seconds:

"""

"""

alert:

last_sent:
messages:[]

alert_rule:

"""

"""
circuit breaker:

status: (connecting, connected, broken)

connecting - waiting
connected - read
broken - waiting / quit

retried:

modifiedon:
modifiedby:


"""

def alert():
    
    """
    redis connection broken
    opc server connection broken
    gevent pool timeout
    
    """
    
def init():
    """ init """
    pass
    
    
def read(point):
    """
    read opc server    
    """
    
    broken = circuit_broken()
    
    if broken:
        alert()
    else:
        print(1000 * time.time())

def call_lua():
    """call lua script"""
    pass
    
def circuit_broken():
    """ circuit breaker """
    
    return False
    #True

    
def main():
    """
    main
    
    dynanic add/remove point?
    
    tonado?
    
    gevent.Timeout
    
    """
    
    points = [1, 2]
    
    while True:        
        
        for point in points:
            read(point)
        
        gevent.sleep(1)
    
    
if __name__ == '__main__':
    main()