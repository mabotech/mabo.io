

/*

npm install node-opcua

*/

/*
* opc ua client
*/
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

//logger.debug("debug")
/*
{
        filename: 'logs/client.log',
        label: 'client',
        level: 'debug',
        json: false,
        maxsize: 10240000,
        maxFiles: 10
    }
*/



var port = nconf.get("server").port
console.log(port)
//var endpointUrl = "opc.tcp://127.0.0.1:49380";
var endpointUrl = nconf.get("server").endpointUrl


var client = new opcua.OPCUAClient();

//var sub1 = opcua.ClientSubscription();



var the_session = null;

var hb = Math.floor(new Date() / 1000)

function main(){

async.waterfall([


    // step 1 : connect to
    function(callback)  {
      client.connect(endpointUrl,function (err) {
         if(err) {
           console.log(" cannot connect to endpoint :" , endpointUrl );
             callback(err);
         } else {
          console.log("connected !");
        callback(null);
         }
         
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
            callback(null)
         }else{
         callback(err);
         }
     });

   },

 
   // step 3 : browse
  /*
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
  */
   
   // step 4 : read a variable 
   function(callback) {
       
       
setTimeout(function(){
        
        
          
    
        the_session.readVariableValue(nconf.get("server").tag_array, function(err,dataValues,diagnostics) {
        //the_session.readVariableValue(["ns=2;s=Channel1.Device1.MT","ns=2;s=Channel1.Device1.Tag1"], function(err,dataValues,diagnostics) {
           if (!err) {
            //console.log("dataValues: ");
            console.log(dataValues[1].value.value);
            // console.log(" Channel1.Device1.MT = " , dataValues[0].value.value);
            // console.log(" Channel1.Device1.Tag1 = " , dataValues[1].value.value);
               callback(null)
           }else{
               
               callback(err)
               
               }

           //console.log(err);
         })}, 1000)
     
     
     
   },
   
   
/*
   function(callback){

    the_session.createSubscription({"ns=2;s=Channel1.Device1.MT"}, function(err,response){

      console.log("ns=2;s=Channel1.Device1.MT");
    })


   }
*/
  
 
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
  /*
  client.disconnect(function(){
      
    console.log("disconnect")
      
      });
      
      */
}) ;

} // end main

main()

var retry = 0

var INTERVAL = 100

function loop(){

    setTimeout(function(){
        
        
          
    
        the_session.readVariableValue(nconf.get("server").tag_array, function(err,dataValues,diagnostics) {
        //the_session.readVariableValue(["ns=2;s=Channel1.Device1.MT","ns=2;s=Channel1.Device1.Tag1"], function(err,dataValues,diagnostics) {
           if (!err) {
            //console.log("dataValues: ");
            console.log(dataValues[1].value.value);
            // console.log(" Channel1.Device1.MT = " , dataValues[0].value.value);
            // console.log(" Channel1.Device1.Tag1 = " , dataValues[1].value.value);
           }

           //console.log(err);
         })
         
   
        
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
INTERVAL = 500            
        loop()
    }, INTERVAL);

} // end loop

//loop()

//TODO: reload config,   tag or lisenter?
// writer
// polling or subscription ?
