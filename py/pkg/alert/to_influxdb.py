

# pip install influxdb


from influxdb import client as influxdb

client_name = "cn"

host = ""
poert = 8083
username = "abc"
password = ""
database = "client_logs"

db = influxdb.InfluxDBClient(host, port, username, password, database)

data = [
  {"points":[[1.1,4.3,2.1],[1.2,2.0,2.0]],
   "name":"web_devweb01_load",
   "columns":["min1", "min5", "min15"]
  }
]
db.write_points(data)