# -*- coding: utf-8 -*-

""" influxdb points generator """

import time

import random

import socket

import gevent

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
    
    def gen(self):
        """ generate data """
        
        timestamp_now = time.time() #-8*60*60
        
        val_a = random.randint(1, 40)
        val_b = random.randint(1, 4)
        val_c = random.randint(1, 24)
        val_d = random.randint(1, 64)
        val_e = random.randint(1, 14)
        val_f = random.randint(1, 44)
        val_g = random.randint(1, 34)
        val_h = random.randint(1, 54)
        val_i = random.randint(1, 44)
        val_j = random.randint(1, 4)         
        
        print(timestamp_now, val_a, val_c, val_c)
        #timestamp2 = timestamp_now+10

        json_body = [
          {
            "points": [
                [1000*timestamp_now, val_a,val_b,val_c,val_d,val_e,val_f,val_g, val_h,val_i,val_j]             
            ],
            "name": self.tsname,
            "columns": ["time", "a","b","c","d","e","f","g","h","i","j"]
          }
        ]

        """
        result = self.db.query('select count(a) from t2;')

        print (result)
        """
        json_body = [{"points":[[1000*timestamp_now,0,0,0,0,0,0,3,3,3,3,3,3,64,64,64,64,64,64,0,0,0,20,0,10,0,0,0,1,15,0,54,54,54,54,54,54,6,6,6,6,6,6,2.059999942779541,2.059999942779541,2.059999942779541,0,0,0,0,0,0,0,0,0,44.15999984741211,2,0,3,64,0,0,54,6,3,0,2]],"name":"ts02","columns":["time","Cool_System_Press5","Cool_System_Press4","Cool_System_Press3","Cool_System_Press2","Cool_System_Press1","Cool_System_Press","Cool_System_Flow5","Cool_System_Flow4","Cool_System_Flow3","Cool_System_Flow2","Cool_System_Flow1","Cool_System_Flow","Cool_Motor1_Vibr5","Cool_Motor1_Vibr4","Cool_Motor1_Vibr3","Cool_Motor1_Vibr2","Cool_Motor1_Vibr1","Cool_Motor1_Vibr","Cool_Motor1_Temp5","Cool_Motor1_Temp4","Cool_Motor1_Temp3","Cool_Motor1_Temp2","Cool_Motor1_Temp1","Cool_Motor1_Temp","Cool_GearBox_Temp5","Cool_GearBox_Temp4","Cool_GearBox_Temp3","Cool_GearBox_Temp2","Cool_GearBox_Temp1","Cool_GearBox_Temp","Cool_Filter_DiffPress5","Cool_Filter_DiffPress4","Cool_Filter_DiffPress3","Cool_Filter_DiffPress2","Cool_Filter_DiffPress1","Cool_Filter_DiffPress","Cool_ChipMotor1_Vibr5","Cool_ChipMotor1_Vibr4","Cool_ChipMotor1_Vibr3","Cool_ChipMotor1_Vibr2","Cool_ChipMotor1_Vibr1","Cool_ChipMotor1_Vibr","Cool_ChipMotor1_Temp5","Cool_ChipMotor1_Temp4","Cool_ChipMotor1_Temp3","Cool_ChipMotor1_Temp2","Cool_ChipMotor1_Temp1","Cool_ChipMotor1_Temp","Cool_ChipMotor1_CurrC5","Cool_ChipMotor1_CurrC4","Cool_ChipMotor1_CurrC3","Cool_ChipMotor1_CurrC2","Cool_ChipMotor1_CurrC1","Cool_ChipMotor1_CurrC","Cool_ChipMotor1_CurrB5","Cool_ChipMotor1_CurrB4","Cool_ChipMotor1_CurrB3","Cool_ChipMotor1_CurrB2","Cool_ChipMotor1_CurrB1","Cool_ChipMotor1_CurrB","Cool_ChipMotor1_CurrA5","Cool_ChipMotor1_CurrA4","Cool_ChipMotor1_CurrA3","Cool_ChipMotor1_CurrA2","Cool_ChipMotor1_CurrA1","Cool_ChipMotor1_CurrA"]}]
        print (json_body)
        self.db.write_points(json_body, time_precision='ms')


def main(sleep_seconds):
    """ main """
    
    influx = InfluxDB("192.168.147.140", "8086", "root","root","monitor")
    i = 1
    while True:
        i = i + 1
        if i > 100:
            break
        try:
            influx.gen()
            gevent.sleep(sleep_seconds)
        #except ConnectionError as cerr:
        #    influx.reconnect()
        #    raise(Exception("err"))
        except Exception as exc:
            print(exc)
            raise(Exception("err"))
        
if __name__ == "__main__":
    sleep_seconds = 1
    main(sleep_seconds)
