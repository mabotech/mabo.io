# -*- coding: utf-8 -*-

import json
import requests

import redis
import msgpack

import time


from mabopy.config.load_config import LoadConfig

filename = "config/config.toml"
    
conf = LoadConfig(filename).config["app"]


HOST = conf["HOST"]
PORT = conf["PORT"]
DB = conf["DB"]

CHANNEL = conf["CHANNEL"]
QUEUE = conf["QUEUE"]

db = redis.Redis(host=HOST, port=PORT, db=DB) 

def post(data):
    
    #val = r.hget(tag, "val")
    #timestamp = r.hget(tag, "timestamp")
    #print("%s, %s-%s" % (tag, timestamp,val) )
    
    URL = conf["URL"] #'http://127.0.0.1:6226/api/v1/callproc.call'
    
    #mtp_update_equipemnt_cs1
    payload = {
                "jsonrpc":"2.0",
                "id":"r2",
                "method":"call",
                "params":
                {
                    "method":"mtp_upsert_cs10",
                    "table":"equipment", 
                    "pkey":"id",
                    "columns":{
                    "id":1,                    
                    "camera":1,
                    "api":0
                    },
                   "context":{"user":"mt", "languageid":"1033", "sessionid":"123" } 
               }
            }
            
    HEADERS = {'content-type': 'application/json', 'accept':'json','User-Agent':'mabo'}
    #headers = HEADERS
    #headers = {'Accept':'json'}
    payload = json.dumps(payload)

    r = requests.post(URL, data =   payload , headers=HEADERS)
    print  r.headers
    #v = r.text #json.loads(r.text)
    #print r.text,
    print json.loads(r.text)
    
    print("%s" % (data) ) 
    

def heartbeat():
    pass
    
def main():
    
    
    #print(dir(r))
    
    pubsub = db.pubsub()
    #r.publish('Que',"New")
    #print(dir(p))
    pubsub.subscribe(CHANNEL)    
    
    # block here
    for message in pubsub.listen():
        
        print message
        
        loop = True
            
        while loop:
            
            val = db.lpop(QUEUE)
            
            if val != None:
                
                data = msgpack.unpackb(val)
                
                #post(data)
                
            else:
                #print "no val"
                loop = False
        

    
if __name__ == "__main__":
    
    
    #post("1")
    """
    time.sleep(0.1)
    post("2")
    time.sleep(0.1)
    post("2")
    """    
    main()     