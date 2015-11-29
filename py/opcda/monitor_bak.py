
#import Pyro.core
import os
import time

import OpenOPC

#import pythoncom

#from OpenOPC import OPCError
from redis_lua import RedisLua

from config import get_config

#pythoncom.CoInitialize()

#opc_client = OpenOPC.client("Graybox.OPC.DAWrapper", "127.0.0.1")

#conf_fn = os.sep.join(
#    [os.path.split(os.path.realpath(__file__))[0], "config.toml"])

conf_fn =  "config.toml"
conf = get_config(conf_fn)["app"]

#print conf

db = RedisLua()

def update(data):
    
    try:
        db.save(data[0], data[1], data[2])
        
    except Exception as ex:
        
        db = RedisLua()
    #print data

def main():

    opc_client = OpenOPC.open_client(conf["HOST"], conf["PORT"])

    opc_client.connect(conf["PROVIDER"], conf["OPC_HOST"]) 

    #info =  opc_client.servers()
    #print info

    tags = conf["TAGS"] # ["Digi.cool_system.A1", "Digi.cool_system.A11"]

    group = conf["GROUP"]

    v = opc_client.read(tags = tags, group=group, update=100)
    
    while True:
        
        data = opc_client.read(group=group, update=100)

        for item in data:
            
            update( item )
        
        time.sleep(conf["INTERVAL"])

if __name__ == "__main__":
    
    main()
    