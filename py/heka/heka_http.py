"""
import socket

import gevent

import signal

signal.getsignal(signal.SIGTERM)

import sys

signal.signal(signal.SIGTERM, lambda num, frame: sys.exit(0))

while True:
    
    print "."
    
    gevent.sleep(1)
    
"""

import logging
import sys
import signal
import subprocess
    
logging.basicConfig(level=logging.WARNING,
                    filename='output.log',
                    format='%(message)s')   
def quit():
    #cleaning code here
    logging.warning('exit')
    sys.exit(0)

def handler(signum=None, frame=None):
    quit()

for sig in [signal.SIGTERM]:
    signal.signal(sig, handler)

def restart():
    command = 'cmd'
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    logging.warning('%s'%output)

restart()    