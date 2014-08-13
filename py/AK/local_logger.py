# -*- coding: utf-8 -*-

""" local logger """

import logbook


from conf import Conf

conf = Conf()


logbook.set_datetime_format(conf.datetime_format)

log = logbook.RotatingFileHandler(conf.logfile, max_size = conf.max_size, \
                                    backup_count = conf.backup_count)

log.push_application()


def get_logger(logger_name):
    """ get logger """
    
    logger = logbook.Logger(logger_name)
    
    return logger

class LocalLogger(object):
    """ local logger """
    def __init__(self):
        pass