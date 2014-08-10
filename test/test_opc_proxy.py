# -*- coding: utf-8 -*-

""" test opc proxy"""

import  unittest

from mabopy.opc.opc_proxy import OPCProxy

class TestOPCServer(unittest.TestCase): 

    def setUp(self):
        """ setup """
        
        opc_server = "SWToolbox.TOPServer.V5"
        
        host = 'mabo01'
        port = 7766
        opc_host = 'mabo01'
        
        mode = 'dcom'
        
        self.opc = OPCProxy(mode, host, port, opc_server, opc_host , 20000)
        self.opc.connect()
    
    def test_read(self):
        """ test read """
        #assert "company" == get_foreign_table("company_id")
        #print opc.read2(["MT", "Tag1", "Tag2"], "Channel1.Device1")
        values = self.opc.read2(["Channel1.Device1.MT", "Channel1.Device1.Tag1", "Channel1.Device1.Tag2"], "Channel1.Device1")
        
        assert values[0][2] == 'Good'
        assert values[1][2] == 'Good'
        assert values[2][2] == 'Good'
    
if __name__ == "__main__":
    
    unittest.main()    
    

