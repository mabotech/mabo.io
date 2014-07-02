"use strict";

/*
  *
  */

var winston = require('winston');

var nconf = require('nconf');

/*global require,console,setTimeout */
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
        filename: 'logs/opcua.log',
        label: 'server',
        level: 'debug',
        json: false,
        maxsize: 10240000,
        maxFiles: 10
    }
});

nconf.file('config.json');

var client = new opcua.OPCUAClient();

//var endpointUrl = "opc.tcp://" + require("os").hostname().toLowerCase() + ":4334/UA/SampleServer";
var endpointUrl = nconf.get("server").endpointUrl; //"opc.tcp://127.0.0.1:49380";
//tags for subscription
var tags = nconf.get("server").tags;

var the_session, the_subscription;


/*
  *
  */
var connect = function(callback) {
    client.connect(endpointUrl, function(err) {
        if (err) {
            //reconnect ? 
            console.log(" cannot connect to endpoint :", endpointUrl);
        } 
        else {
            
            logger.info("connected !");
            console.log("connected !");
        }
        callback(err);
    });
};

/*
  *
  */
var createSession = function(callback) {
    client.createSession(function(err, session) {
        if (!err) {
            the_session = session;
        }
        callback(err);
    });
};

/*
  *
  */
var browse = function(callback) {
    the_session.browse("RootFolder", function(err, browse_result) {
        if (!err) {
            browse_result[0].references.forEach(function(reference) {
                console.log(reference.browseName);
            });
        }
        callback(err);
    });
};

/*
  *
  */
var readVal = function(callback) {
    the_session.readVariableValue("ns=2;s=Channel1.Device1.test", function(err, dataValues) {
        if (!err) {
            console.log(" val % = ", dataValues);
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
};

/*
  *
  */
var subscribe = function(callback) {

    // options of subscription
    the_subscription = new opcua.ClientSubscription(the_session, {
        requestedPublishingInterval: 1000,
        requestedLifetimeCount: 10,
        requestedMaxKeepAliveCount: 3,
        maxNotificationsPerPublish: 10,
        publishingEnabled: true,
        priority: 10
    });

    the_subscription.on("started", function() {
        console.log("subscription started for 2 seconds - subscriptionId=", the_subscription.subscriptionId);
    }).on("keepalive", function() {
        console.log("keepalive");
    }).on("terminated", function() {
        callback();
    });

    /*
       setTimeout(function(){
           // terminate 10s later.
           the_subscription.terminate();
       },1000000);
       */

    // install monitored item
    var i = 0

    for (i = 0; i < tags.length; i++) {
        
        var tag = tags[i].tag;

        var monitoredItem = the_subscription.monitor({
            nodeId: opcua.resolveNodeId(tag),
            attributeId: 13 //
        }, {
            samplingInterval: 100, //
            discardOldest: true,
            queueSize: 10
        });
        console.log("subscrbe ", tag);
        monitoredItem.on("changed", function(dataValue) {
            // to kue/mqtt
            logger.debug(" % val = ", dataValue.value.value);
            console.log(" % val = ", dataValue.value.value);
        });
    }
};

/* 
 *close session
 */
var close = function(callback) {
    the_session.close(function(err) {
        if (err) {
            console.log("session closed failed ?");
        }
        callback();
    });
};

//async    
async.series([

        // step 1 : connect to
        connect,

        // step 2 : createSession
        createSession,

        // step 3 : browse
        // browse,

        // step 4 : read a variable
        //readVal,

        // step 5: install a subscription and install a monitored item for 10 seconds
        subscribe,

        // close session
        close

    ],
    function(err) {
        if (err) {
            console.log(" failure ", err);
        } else {
            console.log("done!");
        }
        client.disconnect(function() {});
    });
// <- End async
