

import time

t0 = time.time()
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


t1 = time.time()

print "t1,",t1-t0

opc_client = OpenOPC.open_client(GATEWAY_HOST, GATEWAY_PORT)

t2 = time.time()

print t2 - t1

opc_client.connect(OPC_SERVER, OPC_HOST) 

t3 = time.time()

print t3 - t2
#info =  opc_client.servers()
#print info

#tags = ["Digi.cool_system.A1", "Digi.cool_system.A11"]

TAGS = conf["TAGS"]

group = "G1"

v = opc_client.read(tags = TAGS, group=group, update=UPDATE)

t4 = time.time()

print t4 - t3

v2 = opc_client.read(group=group, update=UPDATE)

print v2

t5= time.time()

print t5- t4

