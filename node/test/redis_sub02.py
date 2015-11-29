
# -*- coding: utf-8 -*-

import redis

import time

from time import strftime, localtime

r = redis.Redis(host='localhost', port=6379, db=9) 

import json

from influxdb import client as influxdb

class InfluxDB(object):
    
    def __init__(self, host, port, username, password, database):
        """ initial db connection """
        
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        
        self.tsname = "ts02"
        
        self.db = influxdb.InfluxDBClient(self.host, self.port, self.username, self.password, self.database)

    def reconnect(self):
        """ reconnect """
        
        print("reconnect")
        self.db = influxdb.InfluxDBClient(self.host, self.port, self.username, self.password, self.database)
    
    def post(self, json_body):
        
        self.db.write_points(json_body, time_precision='ms')
    

def main():
    
    
    #print(dir(r))
    #influx = InfluxDB("192.168.147.140", "8086", "root","root","monitor")
    
    p = r.pubsub()
    #r.publish('Que',"New")
    #print(dir(p))
    p.subscribe("act")
    
    
    for message in p.listen():
        
        print message
        
        #v = r.hgetall("a:b")
        
        #print v
        
     
        loop = True
            
        while loop:
            
            val = r.lpop("Queue")
            x = strftime("%Y-%m-%d %H:%M:%S",localtime())
            if val != None:
                #post(val)
                #print type(val)
                json_body = json.loads(val)
                #print json.dumps(json_body)
                
                #influx.post(json_body)
                #print x, val
            else:
                loop = False
        

    """
    while True:
        print 1
        message = p.get_message()
        
        if message:
            # do something with the message
            v = 1
            
            while v:
                
                v = r.lpop("Que")
                if v != None:
                    post(v)
                
                #print v
            
            #print message
        time.sleep(0.001) 
    """
    
if __name__ == "__main__":
    
    
    print strftime("%Y-%m-%d %H:%M:%S",localtime())
    
    
    main()     