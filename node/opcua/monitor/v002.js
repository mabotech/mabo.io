var handler = {
  'add' : function(a, b, response) {
     response.result( a + b );
   }
}

var rpc = require('msgpack-rpc');
rpc.createServer();
rpc.setHandler(handler);
rpc.listen(8123);