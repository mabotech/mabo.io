


from time import time

import logbook

from logbook.queues import RedisHandler

from datetime import datetime
logbook.set_datetime_format("local")

import gevent

logger = logbook.Logger('logger')

log = logbook.FileHandler('test_debug.log', level='DEBUG')

log.push_application()

log2 =  RedisHandler('127.0.0.1', port='6379', key='logQ')
#logbook.FileHandler('test_info.log')

log2.push_application()

while True:
    
    t = time()
    logger.debug("debug,timestamp:[%s]" % (t))
    logger.info("timestamp:[%s]" % (t))
    print t
    gevent.sleep(3)