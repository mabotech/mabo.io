


import logbook

from datetime import datetime
logbook.set_datetime_format("local")

import gevent

logger = logbook.Logger('app')

log = logbook.FileHandler('test.log')

log.push_application()


while True:
    

    logger.info("info")
    
    gevent.sleep(3)