

#import Pyro.core

import OpenOPC

#import pythoncom

#from OpenOPC import OPCError


#pythoncom.CoInitialize()

#opc_client = OpenOPC.client("Graybox.OPC.DAWrapper", "127.0.0.1")

opc_client = OpenOPC.open_client("127.0.0.1", 7766)

opc_client.connect("Kepware.KEPServerEX.V5", "127.0.0.1") 

#info =  opc_client.servers()
#print info

tags = ["Digi.cool_system.A1", "Digi.cool_system.A11"]

group = "g1"

v = opc_client.read(tags = tags, group=group, update=100)

v2 = opc_client.read(group=group, update=100)

print v2

