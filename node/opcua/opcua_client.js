
/*
* opc ua client
*/
var nconf = require('nconf');
var winston = require('winston');

var opcua = require("node-opcua");
var async = require("async");


var logger = winston.loggers.add('server', {
    console: {
        //silent:true,
        level: 'debug',
        colorize: 'true',
        label: 'server'
    },
    file: {
        filename: 'logs/client.log',
        label: 'client',
        level: 'debug',
        json: false,
        maxsize: 10240000,
        maxFiles: 10
    }
});

var client = new opcua.OPCUAClient();

//var sub1 = opcua.ClientSubscription();

var endpointUrl = "opc.tcp://127.0.0.1:49380";

var the_session = null;

var hb = Math.floor(new Date() / 1000)

function main(){

async.series([


    // step 1 : connect to
    function(callback)  {
      client.connect(endpointUrl,function (err) {
         if(err) {
           console.log(" cannot connect to endpoint :" , endpointUrl );
         } else {
          console.log("connected !");

         }
         callback(err);
      });
   },

 
   // step 2 : createSession
   function(callback) {
     client.createSession( function(err,session) {
         if(!err) {
           the_session = session;
           /*
           console.log(session.name);
           console.log(session.sessionId);
           console.log(session.authenticationToken);
           console.log(session.serverNonce);
           console.log(session.serverCertificate);
           console.log(session.serverSignature);
           console.log(session.timeout);
           //console.log(session.name);
           */
           console.log(the_session.readVariableValue);

         }
         callback(err);
     });

   },

 
   // step 3 : browse
  
   function(callback) {

     the_session.browse("RootFolder", function(err,browse_result,diagnostics){
        if(!err) {
          browse_result[0].references.forEach(function(reference) {
            console.log( reference.browseName);
          });
        }
        callback(err);
     });
   },
  
   // step 4 : read a variable

 
   function(callback) {
    
     the_session.readVariableValue(["ns=2;s=Channel1.Device1.MT","ns=2;s=Channel1.Device1.Tag1"], function(err,dataValues,diagnostics) {
       if (!err) {
        console.log(dataValues);
         console.log(" Channel1.Device1.MT = " , dataValues[0].value.value);
         console.log(" Channel1.Device1.Tag1 = " , dataValues[1].value.value);
       }

       callback(err);
     })
   },
/*
   function(callback){

    the_session.createSubscription({"ns=2;s=Channel1.Device1.MT"}, function(err,response){

      console.log("ns=2;s=Channel1.Device1.MT");
    })


   }
*/
 
   function(callback){
       
       the_subscription=new opcua.ClientSubscription(the_session,{
    requestedPublishingInterval: 100,
    requestedLifetimeCount: 60,
    requestedMaxKeepAliveCount: 20,
    maxNotificationsPerPublish: 20,
    publishingEnabled: true,
    priority: 10
});

the_subscription.on("started",function(){
    console.log("subscription started for 2 seconds - subscriptionId=",the_subscription.subscriptionId);
}).on("keepalive",function(){
    
    hb = Math.floor(new Date() / 1000)
    console.log("keepalive");
    
    
}).on("terminated",function(){
    callback();
});

setTimeout(function(){
    the_subscription.terminate();
},1000000);

// install monitored item
console.log("-------------------------------------");
var monitoredItem  = the_subscription.monitor({
    nodeId: opcua.resolveNodeId("ns=2;s=Channel1.Device1.test"),
    attributeId: 13
},
{
    samplingInterval: 100,
    discardOldest: false,
    queueSize: 10
});


monitoredItem.on("changed",function(dataValue){
   console.log(" test = ",dataValue.value.value);
});


var monitoredItem2  = the_subscription.monitor({
    nodeId: opcua.resolveNodeId("ns=2;s=Channel1.Device1.Tag2"),
    attributeId: 13
},
{
    samplingInterval: 100,
    discardOldest: true,
    queueSize: 10
});


monitoredItem2.on("changed",function(dataValue){
   console.log(" Tag2 = ",dataValue.value.value);
});

       
       /*
var subscriptionId = function(){

console.log("subscriptionId");

}

 the_subscription=new opcua.ClientSubscription(the_session,{
            requestedPublishingInterval: 1000,
            requestedLifetimeCount: 10,
            requestedMaxKeepAliveCount: 2,
            maxNotificationsPerPublish: 10,
            publishingEnabled: false,
            priority: 10
        });
        the_subscription.on("started",function(subscriptionId){
            console.log("started",the_subscription);
        }).on("keepalive",function(){
            console.log("keepalive")
        }).on("terminated",function(){
            callback();
        }).on("received_notifications", function(){
            console.log("received_notifications")
        });

        setTimeout(function(){
            the_subscription.terminate();
        },300000); 
        
        
        // install monitored item
var monitoredItem  = the_subscription.monitor({
    nodeId: opcua.resolveNodeId("ns=2;s=Channel1.Device1.Tag1"),
    attributeId: 13
},
{
    samplingInterval: 100,
    discardOldest: true,
    queueSize: 10
});
console.log("-------------------------------------");

monitoredItem.on("changed",function(dataValue){
   console.log(" % free mem = ",dataValue.value.value);
});
        
*/
   }
  
 
  /*
     function(callback) {
    
     the_session.writeSingleNode("ns=2;s=Channel1.Device1.MT",6226, function(err,dataValues,diagnostics) {
       if (!err) {
         console.log(" Channel1.Device1.MT = " , dataValues[0].value.value);
       }

       callback(err);
     })
   },
 */
], function(err) {
  if (err) {
    console.log(" failure ",err);
  } else {
    console.log("done!")
  }
  // disconnect regardless
  client.disconnect(function(){
      
    console.log("disconnect")
      
      });
}) ;

} // end main

main()

var retry = 0

function loop(){

    setTimeout(function(){
        
        var now = Math.floor(new Date() / 1000)
        
        if (now - hb > 6){
            hb = Math.floor(new Date() / 1000) // consider connection time
            console.log("disconnected")   
            logger.debug('disconnected, '+hb);
            //reconnect
            
            main()
        }  else{
            
            console.log("ok")   
            
            }          
        loop()
    },2000);

} // end loop

loop()