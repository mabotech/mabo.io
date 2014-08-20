# -*- coding: utf-8 -*-


from influxdb import client as influxdb

db = influxdb.InfluxDBClient("192.168.100.112", "8086", "root","root","monitor")

result = db.query('select a from t1;')

print (result)
