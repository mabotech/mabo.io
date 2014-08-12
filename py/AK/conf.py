



from mabopy.patterns.singleton import Singleton

from utils import get_conf

class Conf(object):
    
    __metaclass__ = Singleton
    
    def __init__(self):
        
        conf = get_conf("ak_client.toml")
        
        for item in conf["client"]:
            print item
            setattr(self, item, conf["client"][item])    

        for item in conf["logging"]:
            print item
            setattr(self, item, conf["logging"][item])      