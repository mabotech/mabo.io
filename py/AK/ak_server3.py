
# simulator for ak server
import sys

import socket
import struct

import toml

import SocketServer

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print "{} wrote:".format(self.client_address[0])
        print self.data
        # just send back the same data, but upper-cased
        self.request.sendall(self.data)
        
        self.request.close()

if __name__ == "__main__":
    
    # Commands and replies are exchanged on TCP port 23800.  
    # real time data is available via TCP (port 23805)
    conf_fn = "ak_server.toml"
    
    with open(conf_fn) as conf_fh:
        
        conf = toml.loads(conf_fh.read())
    
    
    #print conf
    
    HOST = conf["server"]["host"]
    PORT = conf["server"]["port"]
    
    #HOST, PORT = "localhost", 23805 
    
    
    #sys.exit(0)

    # Create the server, binding to localhost on port
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    print("AK Host Simulator on %s:%s" %(HOST, PORT))
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()