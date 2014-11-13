/*

uglifyjs ua_client.js -b  --comments all > ua_client1.js
*/
var nconf = require("nconf");

var winston = require("winston");

var opcua = require("node-opcua");

var co = require("co");

nconf.file("config.json");

//console.log( nconf.get("logging"))
var logger = winston.loggers.add("server", {
    console: {
        //silent:true,
        level: "debug",
        colorize: "true",
        label: "server"
    },
    file: nconf.get("logging")
});

var endpointUrl = nconf.get("server").endpointUrl;

var client = new opcua.OPCUAClient();

//var sub1 = opcua.ClientSubscription();
var the_session = null;

var i = 0;

var t = new Date().getTime();

var tags = [ "ns=2;s=Channel1.Device1.fV1", "ns=2;s=Channel1.Device1.fV2", "ns=2;s=Channel1.Device1.MT", "ns=2;s=Channel1.Device1.Tag1", "ns=2;s=Channel1.Device1.Tag2", "ns=2;s=Channel1.Device1.test" ];

var read = function() {
    the_session.readVariableValue(//      nconf.get("server").tag_array,  //points array
    //TimestampsToReturn
    tags, function(err, dataValues, diagnostics) {
        //the_session.readVariableValue(["ns=2;s=Channel1.Device1.MT","ns=2;s=Channel1.Device1.Tag1"], function(err,dataValues,diagnostics) {
        if (!err) {
            dataValues.forEach(function(data, index) {
                console.log(tags[index]);
                console.log(data.value.value);
            });
            console.log("==============================");
        }
    });
};

var callback1 = function(err) {
        if (err) {
            console.log(" cannot connect to endpoint :", endpointUrl);
           
        } else {
            console.log("connected !");
         
        }
        return 1
    }

    var callback2 = function(err, session) {
        if (err) {
            console.log("err:", err);
            
        } else {
            the_session = session;
            console.log("session:", the_session)
            return 1
        
        }
        return 1
    }
    
co( function *() {
    
    yield function(){client.connect(endpointUrl, callback1);}
    
    
 
    yield function(){client.createSession(callback2)};
 
    // result now equals 'done'    
    //assert(the_session)
    yield function(){setInterval(read, 500);}
    console.log("result:", result);
})();