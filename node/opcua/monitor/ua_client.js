

var opcua = require("node-opcua");
var async = require("async");

var i = 0

var t = new Date().getTime();

var real_read = function(callback, result){
 
    i = i +1
    if(i%10 == 0){  
        var t1 = new Date().getTime() 
        console.log(i)    
        console.log("read:",  t1 - t)      
        t = t1
        
        //throw("err")
    }     
     if(i%25==0){
        //throw("err")
        callback("throw", 1)
    }else{
            
        callback(null, 0)
    }
    
}

var read = function(item, callback){    
    
    //console.log("item:", item)
    var j = 0
    async.retry(3, function(callback, result){
         j = j + 1
        i = i +1
        
        if(i%3 == 0){
            
            console.log("item " , i, j)
            callback("err")
            
            }
        
        if (item == 1){
            
            console.log("item " , i, j)
            
            }
        
        //console.log("callback:", item)
        
        
        }, function(err, result){
        
        console.log(err);
        console.log(result)
        
        })
        
    callback(null);
    //
   
}

var devices = [1,2,3]

var iterator = function(){
    
    async.each(devices, read, function(err){
        
        })
    
    }
    
async.waterfall([
    function(callback){
        callback(null, 'one', 'two');
    },
    function(arg1, arg2, callback){
      // arg1 now equals 'one' and arg2 now equals 'two'
        console.log(arg1)
        callback(null, 'three');
     }
], function (err, result) {
   // result now equals 'done'    
    
    setInterval( iterator, 1000)
    
    console.log("result:",result)    
    
});