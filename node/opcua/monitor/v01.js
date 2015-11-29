



var time = process.hrtime();
// [ 1800216, 25 ]

/*
setTimeout(function() {
  var diff = process.hrtime(time);
  // [ 1, 552 ]

  console.log('benchmark took %d nanoseconds', diff[0] * 1e9 + diff[1]);
  // benchmark took 1000000527 nanoseconds
}, 1000);

*/

var v1 = (new Date()).valueOf()

function read(){
    
      var diff = process.hrtime(time);
    
    var v2 = (new Date()).valueOf()
    
    console.log( v2 - v1 )
    
    v1 = v2
    
    time = process.hrtime()
    
  // [ 1, 552 ]

  console.log('benchmark took %d nanoseconds', (diff[0] * 1e9 + diff[1])/1000000 )
    
    for(var i =0; i < 5000000; i ++){
        
        var z = i * i * i 
        
        }
    
    
    }


//setInterval(read, 100)
    
    
var net = require('net');

var server = net.createServer(function (socket) {
  //socket.write('Echo server\r\n');
    
       
    
   socket.pipe(socket);
    socket.on("data", function(data){
        
          var now = new Date()
    
    var s001 = now.valueOf() 
    
    console.log(s001/1000)
        
        read() // take time to run
        
        })
    socket.on("error", function(err){
    
    console.log(err)
    
    })
});

server.listen(1337, '127.0.0.1');