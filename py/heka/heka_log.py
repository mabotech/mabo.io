# -*- coding: utf-8 -*-

"""
log for heka Logfile input
"""

import logbook

from datetime import datetime
logbook.set_datetime_format("local")

import socket
import gevent

logger = logbook.Logger('app')

log = logbook.FileHandler('test.log')

log.push_application()


def main():
    
    while True:
        

        logger.info("info")
        
        gevent.sleep(3)
        
        
if __name__ == '__main__':
    main()