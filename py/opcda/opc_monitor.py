
#import Pyro.core
import os
import time

import toml
import json

import OpenOPC

#import pythoncom

#from OpenOPC import OPCError

#from config import get_config

#pythoncom.CoInitialize()

#opc_client = OpenOPC.client("Graybox.OPC.DAWrapper", "127.0.0.1")

#conf_fn = os.sep.join(
#    [os.path.split(os.path.realpath(__file__))[0], "config.toml"])

from multi_logging import get_logger



conf_fn =  "config/opc_monitor.toml"

with open(conf_fn, "r") as conf_fh:

    cfg = toml.loads(conf_fh.read())

    conf = cfg["app"]

with open(conf["logging_config"], "r") as fh:
    
    json_str = fh.read() 

conf_json = json.loads(json_str)

logger = get_logger(conf["log_base"], conf["app_name"], conf_json)

logger.debug(conf)

from redis_lua import RedisLua


#conf = get_config(conf_fn)["app"]

#print conf

#db = RedisLua()

class OPCMonitor(object):
    
    def __init__(self):

        self.connected = 0
        self.closed = 0        
        
        self.i = 0
        
        self.retry = 0   

        self.last_errno = 0
        
        self.db = RedisLua()
        
        self.equipment_id = conf["equipment_id"]
        
        self.tags = conf["TAGS"]
        self.group = conf["GROUP"]
        
        
    def connect(self):
        
        logger.debug("connect...............")
        
        try:
            
            if conf["Use_Wrapper"]  == True:
                
                logger.debug(conf["DAWrapper"])
                
                self.opc_client = OpenOPC.client(conf["DAWrapper"], conf["HOST"])

                
            else:
                
                logger.debug(conf["PROVIDER"])
            
                self.opc_client = OpenOPC.open_client(conf["HOST"], conf["PORT"])

            self.opc_client.connect(conf["PROVIDER"], conf["OPC_HOST"]) 
                
            self.connected = 1
            
        except Exception as ex:
            logger.debug(ex)
            self.connected = 0
            
            
    def check_conn(self):
        
        #logger.debug(self.connected)
        
        if self.connected == 0:
            self.connect()
            
        if self.connected == 0:
            
            return 0
        else:
            self.connected = 1
            return 1
            
    def check(self):
        
        try:
            
            data = self.opc_client.read(tags = self.tags, group=self.group, update=100)
            
            tag_val = data[0][1]
            
        except Exception as ex:
            
            tag_val = False   
        
        
        if tag_val == True:
            val = 1
        else:
            val = 0
            
        self.post(val)
        
    def post(self, val):
        
        key = self.equipment_id
        
        result = ""
        logger.debug("%s,%s" % (key, val))
        
        ttl = 2 *conf["INTERVAL"]
        
        rtn = self.db.save(key, result, 1, ttl)
        
        #print rtn
        


def update(data):
    
    try:
        db.save(data[0], data[1], data[2])
        
    except Exception as ex:
        
        db = RedisLua()
    #print data

def main():

    #opc_client = OpenOPC.open_client(conf["HOST"], conf["PORT"])

    #opc_client.connect(conf["PROVIDER"], conf["OPC_HOST"]) 

    #info =  opc_client.servers()
    #print info

    #tags = conf["TAGS"] # ["Digi.cool_system.A1", "Digi.cool_system.A11"]

    #group = conf["GROUP"]

    #v = opc_client.read(tags = tags, group=group, update=100)
    
    monitor = OPCMonitor()
    
    while True:
        """
        data = opc_client.read(group=group, update=100)

        for item in data:
            
            update( item )
        """
        
        monitor.check_conn()
        
        monitor.check()
        
        time.sleep(conf["INTERVAL"])

if __name__ == "__main__":
    
    main()
    