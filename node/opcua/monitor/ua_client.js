

var nconf = require('nconf');
var winston = require('winston');

var opcua = require("node-opcua");
var async = require("async");

nconf.file('config.json');

console.log( nconf.get("logging"))
var logger = winston.loggers.add('server', {
    console: {
        //silent:true,
        level: 'debug',
        colorize: 'true',
        label: 'server'
    },
    file: nconf.get("logging")
});


var endpointUrl = nconf.get("server").endpointUrl


var client = new opcua.OPCUAClient();

//var sub1 = opcua.ClientSubscription();



var the_session = null;


var i = 0

var t = new Date().getTime();

var real_read = function(){
 
         the_session.readVariableValue(
       //      nconf.get("server").tag_array,  //points array
            //TimestampsToReturn
            ["ns=2;s=Channel1.Device1.MT","ns=2;s=Channel1.Device1.Tag1","ns=2;s=Channel1.Device1.Tag2","ns=2;s=Channel1.Device1.test"], 
       
            function(err,dataValues,diagnostics) {
            //the_session.readVariableValue(["ns=2;s=Channel1.Device1.MT","ns=2;s=Channel1.Device1.Tag1"], function(err,dataValues,diagnostics) {
               if (!err) {
                   
                /*
                console.log("dataValues: ");
                console.log(dataValues[0].value.value); 
                console.log(dataValues[1].value.value);
                console.log("sourceTimestamp:", dataValues[0].sourceTimestamp)
                console.log("serverTimestamp:", dataValues[0].serverTimestamp)
                // console.log(" Channel1.Device1.MT = " , dataValues[0].value.value);
                // console.log(" Channel1.Device1.Tag1 = " , dataValues[1].value.value);
                   */
               }
                
             //  callback(err);
             } // End function
             )
    
}

var read = function(item, callback){    
    
    //console.log("item:", item)
    var j = 0
    async.retry(3, function(callback, result){
    
         the_session.readVariableValue(
       //      nconf.get("server").tag_array,  //points array
            //TimestampsToReturn
            ["ns=2;s=Channel1.Device1.MT","ns=2;s=Channel1.Device1.Tag1","ns=2;s=Channel1.Device1.Tag2","ns=2;s=Channel1.Device1.test"], 
       
            function(err,dataValues,diagnostics) {
            //the_session.readVariableValue(["ns=2;s=Channel1.Device1.MT","ns=2;s=Channel1.Device1.Tag1"], function(err,dataValues,diagnostics) {
               if (!err) {
                   
                /*
                console.log("dataValues: ");
                console.log(dataValues[0].value.value); 
                console.log(dataValues[1].value.value);
                console.log("sourceTimestamp:", dataValues[0].sourceTimestamp)
                console.log("serverTimestamp:", dataValues[0].serverTimestamp)
                // console.log(" Channel1.Device1.MT = " , dataValues[0].value.value);
                // console.log(" Channel1.Device1.Tag1 = " , dataValues[1].value.value);
                   */
               }
                
               callback(err);
             } // End function
             )
        
        
        
        }, function(err, result){
        
       // console.log(err);
       // console.log(result)
        
        })
        
    callback(null);
    //
   
}

var devices = [3]

var iterator = function(){
    
    async.each(devices, read, function(err){
        
        })
    
    }
    
async.waterfall([
    function(callback){
      client.connect(endpointUrl,function (err) {
         if(err) {
           console.log(" cannot connect to endpoint :" , endpointUrl );
              callback("err");
         } else {
          console.log("connected !");
          callback(null);
         }
        
      });
    },
    function(callback){
  client.createSession( function(err,session) {
         if(!err) {
           the_session = session;
         }
     });
     
        callback(null);
     }
], function (err, result) {
   // result now equals 'done'    
    
    setInterval( real_read, 50)
    
    console.log("result:",result)    
    
});