



var client = influx({

  //cluster configuration
  hosts : [
    {
      host : '192.168.147.140',
      port : 8060 //optional. default 8086
    }
  ],
  // or single-host configuration
  host : '192.168.147.140',
  port : 8086, // optional, default 8086
  username : 'root',
  password : 'root',
  database : 'monitor'
});