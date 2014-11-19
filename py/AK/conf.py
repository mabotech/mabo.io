# -*- coding: utf-8 -*-

""" global conf """

from mabopy.patterns.singleton import Singleton

from utils import get_conf

class Conf(object):
    """ conf """
    __metaclass__ = Singleton
    
    def __init__(self, conf_file=""):
        """ init conf 
            TODO: flat to 'ins.attr'
        """
        
        conf = get_conf(conf_file)
        
        for item in conf["client"]:
            #print item
            setattr(self, item, conf["client"][item])    

        for item in conf["logging"]:
            #print item
            setattr(self, item, conf["logging"][item])      

