# -*- coding: utf-8 -*-

""" global conf """

import toml

from singleton import Singleton

class LoadConfig(object):
    """ conf """
    
    __metaclass__ = Singleton
    
    def __init__(self, conf_file=""):
        
        with open(conf_file) as confh:
            self.config = toml.loads(confh.read())      
            
def test():
    
    filename = "config.toml"
    
    conf = Config(filename).config["app"]
    
    print conf
    
if __name__ == '__main__':
    test()
