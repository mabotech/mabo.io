var opcua = require("node-opcua");
var async = require("async");

var client = new opcua.OPCUAClient();

//var sub1 = opcua.ClientSubscription();

var endpointUrl = "opc.tcp://127.0.0.1:49380";

var the_session = null;
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
    
     the_session.readVariableValue(["ns=2;s=Channel1.Device1.Tag1","ns=2;s=Channel1.Device1.Tag2"], function(err,dataValues,diagnostics) {
       if (!err) {
        console.log(dataValues);
         console.log(" Channel1.Device1.Tag1 = " , dataValues[0].value.value);
         console.log(" Channel1.Device1.Tag2 = " , dataValues[1].value.value);
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
 /*
   function(callback){
var subscriptionId = function(){

console.log("subscriptionId");

}

 the_subscription=new opcua.ClientSubscription(the_session,{
            requestedPublishingInterval: 100,
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
        },3000); 

   }
   */
 
  /*
     function(callback) {
    
     the_session.writeSingleNode("ns=2;s=Channel1.Device1.MT",100, function(err,dataValues,diagnostics) {
       if (!err) {
        // console.log(" Channel1.Device1.MT = " , dataValues[0].value.value);
       }

       callback(err);
     })
   },*/
 
], function(err) {
  if (err) {
    console.log(" failure ",err);
  } else {
    console.log("done!")
  }
  // disconnect regardless
  client.disconnect(function(){});
}) ;