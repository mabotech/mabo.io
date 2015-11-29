

import gevent

#import Pyro.core

import OpenOPC

#import pythoncom

#from OpenOPC import OPCError

#pythoncom.CoInitialize()

from mabopy.config.load_config import LoadConfig

filename = "config.toml"
    
conf = LoadConfig(filename).config["app"]

#opc_client = OpenOPC.client("Graybox.OPC.DAWrapper", "127.0.0.1")

GATEWAY_HOST = conf["GATEWAY_HOST"]
GATEWAY_PORT = conf["GATEWAY_PORT"]

OPC_SERVER = conf["OPC_SERVER"]
OPC_HOST = conf["OPC_HOST"]

UPDATE = conf["UPDATE"]

TAGS = conf["TAGS"]

class OPCClient(object):
    
    def __init__(self):

        self.client = OpenOPC.open_client(GATEWAY_HOST, GATEWAY_PORT)

        self.client.connect(OPC_SERVER, OPC_HOST) 

        #info =  opc_client.servers()
        #print info

        #tags = ["Digi.cool_system.A1", "Digi.cool_system.A11"]

        
    def create_group(self):
        
        group = "G1"  
        
        v = self.client.read(tags = TAGS, group=group, update=UPDATE)
        
        print v
        
    def read(self):
    
        group = "G1"        

        v2 = self.client.read(group=group, update=UPDATE)

        #print v2
        
        return v2

def save(data):
    
    print data

def main():
    
    client = OPCClient()
        
    client.create_group()
    
    while True:
    
        v = client.read()
        
        print v[0][0], v[0][1]        
        
        gevent.sleep(1)
    
    

if __name__ == "__main__":
    
    main()
