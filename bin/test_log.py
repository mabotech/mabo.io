

from time import time

import logbook

from datetime import datetime
logbook.set_datetime_format("local")

import gevent

logger = logbook.Logger('app')

log = logbook.FileHandler('test1.log')

log.push_application()


while True:
    
    t = time()
    logger.info("timestamp:[%s]" % (t))
    print t
    gevent.sleep(3)