

var opcua = require("node-opcua");
var async = require("async");

var i = 0

var t = new Date().getTime();


var read = function(){    
    //
    i = i +1
    if(i%1 == 0){  
        var t1 = new Date().getTime() 
        console.log(i)    
        console.log("read:",  t1 - t)      
        t = t1
        //throw("err")
    }    
}

async.waterfall([
    function(callback){
        callback(null, 'one', 'two');
    },
    function(arg1, arg2, callback){
      // arg1 now equals 'one' and arg2 now equals 'two'
        console.log(arg1)
        callback(null, 'three');
    },
    function(arg1, callback){
        // arg1 now equals 'three'
          console.log(arg1)
        callback(null, 'done');
    }
], function (err, result) {
   // result now equals 'done'    
    
    setInterval( read, 1000)
    
    console.log("result:",result)    
    
});