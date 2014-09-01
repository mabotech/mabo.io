# -*- coding: utf-8 -*-

import time


from influxdb import client as influxdb

db = influxdb.InfluxDBClient("192.168.100.112", "8086", "root","root","monitor")



t1 = time.time()
t2 = t1+10
json_body = [
  {
    "points": [
        [t1, "1", 11, 31.0],
        [t2, "2", 21, 21.0]
    ],
    "name": "t2",
    "columns": ["time", "c", "a", "b"]
  }
]

result = db.query('select count(a) from t2;')

print (result)

db.write_points(json_body)


