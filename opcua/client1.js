"use strict";

/*global require,console,setTimeout */
var opcua = require("node-opcua");
var async = require("async");

var client = new opcua.OPCUAClient();
//var endpointUrl = "opc.tcp://" + require("os").hostname().toLowerCase() + ":4334/UA/SampleServer";
var endpointUrl = "opc.tcp://127.0.0.1:49380";

var the_session, the_subscription;

var connect =  function(callback)  {
        client.connect(endpointUrl,function (err) {
            if(err) {
                console.log(" cannot connect to endpoint :" , endpointUrl );
            } else {
                console.log("connected !");
            }
            callback(err);
        });
    };
    
async.series([

    // step 1 : connect to
   connect,

    // step 2 : createSession
    function(callback) {
        client.createSession( function(err,session) {
            if(!err) {
                the_session = session;
            }
            callback(err);
        });
    },

    // step 3 : browse
    function(callback) {
       the_session.browse("RootFolder", function(err,browse_result){
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
       the_session.readVariableValue("ns=2;s=Channel1.Device1.test", function(err,dataValues) {
           if (!err) {
               console.log(" val % = " , dataValues);
            /*
val % =  [ { value:
    { dataType: [Getter/Setter],
      arrayType: [Getter/Setter],
      value: 443 },
   statusCode: { value: 0, description: 'No Error', name: 'Good' },
   sourceTimestamp: null,
   sourcePicoseconds: 0,
   serverTimestamp: null,
   serverPicoseconds: 0 } ]               
               */
           }
           callback(err);
       });
    },

    // step 5: install a subscription and install a monitored item for 10 seconds
    function(callback) {
       the_subscription=new opcua.ClientSubscription(the_session,{
           requestedPublishingInterval: 1000,
           requestedLifetimeCount: 10,
           requestedMaxKeepAliveCount: 3,
           maxNotificationsPerPublish: 10,
           publishingEnabled: true,
           priority: 10
       });
       
       the_subscription.on("started",function(){
           console.log("subscription started for 2 seconds - subscriptionId=",the_subscription.subscriptionId);
       }).on("keepalive",function(){
           console.log("keepalive");
       }).on("terminated",function(){
           callback();
       });
       
       setTimeout(function(){
           // terminate 10s later.
           the_subscription.terminate();
       },10000);
       
       // install monitored item
       var monitoredItem  = the_subscription.monitor({
           nodeId: opcua.resolveNodeId("ns=2;s=Channel1.Device1.test"),
           attributeId: 13
       },
       {
           samplingInterval: 100,
           discardOldest: true,
           queueSize: 10
       });
       console.log("-------------------------------------");
       
       monitoredItem.on("changed",function(dataValue){
          console.log(" % MT val = ",dataValue.value.value);
       });
    },

    // close session
    function(callback) {
        the_session.close(function(err){
            if(err) {
                console.log("session closed failed ?");
            }
            callback();
        });
    }

],
function(err) {
    if (err) {
        console.log(" failure ",err);
    } else {
        console.log("done!");
    }
    client.disconnect(function(){});
}) ;