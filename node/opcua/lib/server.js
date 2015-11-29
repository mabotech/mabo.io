var net = require('net');

var server = net.createServer(function(socket) {
    //socket.write('Echo server\r\n'); 
    
    socket.pipe(socket);
    socket.on("data", function(data) {

        
        console.log(data.toString('utf8'))
    
        var now = new Date()
        
        console.log(now.valueOf())


    })
    socket.on("error", function(err) {

        console.log(err)

    })
});

var port = 1337

console.log("listen on: ", port)

server.listen(port, '127.0.0.1');
