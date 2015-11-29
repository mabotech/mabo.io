# -*- coding: utf-8 -*-

""" local logger """

import logbook


from conf import Conf

conf = Conf()


logbook.set_datetime_format(conf.datetime_format)

log = logbook.RotatingFileHandler(conf.logfile, max_size = conf.max_size, \
                                    backup_count = conf.backup_count,\
                                    level = conf.level, \
                                    bubble=True
                                    )
#print dir(log)

log.format_string = "[{record.time:%Y-%m-%d %H:%M:%S.%f}][{record.thread},{record.module},{record.func_name},{record.lineno}] {record.level_name}: {record.channel}: {record.message}"


log.default_format_string = "[{record.time:%Y-%m-%d %H:%M:%S.%f}][{record.thread},{record.module},{record.func_name},{record.lineno}] {record.level_name}: {record.channel}: {record.message}"

log.push_application()


def get_logger(logger_name):
    """ get logger """
    
    logger = logbook.Logger(logger_name)
    #print dir(logger)
    return logger

class LocalLogger(object):
    """ local logger """
    def __init__(self):
        pass