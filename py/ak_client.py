
""" AK Protocol Test"""

import socket

import struct


import aklib



class AKClient(object):
    
    """ 
    AK Protocol Test, 
    
    * BEP/Burke E. Porter
    * MAHA
    * Horiba
    * AVL    
    """

    def __init__(self):
        """ socket connect"""
        
        host = '127.0.0.1'    # The remote host
        port = 6010           # The same port as used by the server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    
    @classmethod
    def pack(cls, i):
        """ pack """
        
        cmd = "AVFI"
        cmd = " " + cmd + " "
        leng = len(cmd)
        fmt = "!b%ds3b" % (leng)
        buf = struct.pack(fmt, 0x02, cmd, 0x41+i, 0x20, 3)

        print repr(buf)
        
        print(buf) 
    
        return buf
    
    def send(self, buf):
        """ send """
        
        self.sock.sendall(buf)
        
    def recv(self):
        """ recv """
        
        data = self.sock.recv(1024)
        fmt = "%db" % (len(data))
        val = struct.unpack(fmt, data)
        
        print 'Received', repr(data)
        
        print val
        print repr(val)
        
    
    def close(self):
        """ close socket """
        self.sock.close()
 
def main():
    """ main """
    
    ak_client = AKClient()
    
    for i in xrange(0, 3):
        
        buf = ak_client.pack(i)
        ak_client.send(buf)
        ak_client.recv()
    
    ak_client.close()        
        
if __name__ == '__main__':
    
    main()
    
    