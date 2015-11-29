/*

uglifyjs ua_client.js -b  --comments all > ua_client1.js
*/
var nconf = require("nconf");

var winston = require("winston");

var opcua = require("node-opcua");

var async = require("async");

var redis = require("redis");
var    client = redis.createClient();
client.select(9)

    // if you'd like to select database 3, instead of 0 (default), call
    // client.select(3, function() { /* ... */ });

    client.on("error", function (err) {
        console.log("Error " + err);
    });

nconf.file("config.json");

//console.log( nconf.get("logging"))
var logger = winston.loggers.add("server", {
    console: {
        silent:true,
        level: "debug",
        colorize: "false",
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

/*
var tags = [ "ns=2;s=Channel1.Device1.fV1", "ns=2;s=Channel1.Device1.fV2", "ns=2;s=Channel1.Device1.MT", "ns=2;s=Channel1.Device1.Tag1", "ns=2;s=Channel1.Device1.Tag2", "ns=2;s=Channel1.Device1.test" ];
*/

var tags =['ns=2;s=CA_OP10E_D.cool_system.Cool_System_Press5', 'ns=2;s=CA_OP10E_D.cool_system.Cool_System_Press4'];
/*
, 'ns=2;s=CA_OP10E_D.cool_system.Cool_System_Press3', 'ns=2;s=CA_OP10E_D.cool_system.Cool_System_Press2', 'ns=2;s=CA_OP10E_D.cool_system.Cool_System_Press1', 'ns=2;s=CA_OP10E_D.cool_system.Cool_System_Press', 'ns=2;s=CA_OP10E_D.cool_system.Cool_System_Flow5', 'ns=2;s=CA_OP10E_D.cool_system.Cool_System_Flow4', 'ns=2;s=CA_OP10E_D.cool_system.Cool_System_Flow3', 'ns=2;s=CA_OP10E_D.cool_system.Cool_System_Flow2', 'ns=2;s=CA_OP10E_D.cool_system.Cool_System_Flow1', 'ns=2;s=CA_OP10E_D.cool_system.Cool_System_Flow', 'ns=2;s=CA_OP10E_D.cool_system.Cool_Motor1_Vibr5', 'ns=2;s=CA_OP10E_D.cool_system.Cool_Motor1_Vibr4', 'ns=2;s=CA_OP10E_D.cool_system.Cool_Motor1_Vibr3', 'ns=2;s=CA_OP10E_D.cool_system.Cool_Motor1_Vibr2', 'ns=2;s=CA_OP10E_D.cool_system.Cool_Motor1_Vibr1', 'ns=2;s=CA_OP10E_D.cool_system.Cool_Motor1_Vibr', 'ns=2;s=CA_OP10E_D.cool_system.Cool_Motor1_Temp5', 'ns=2;s=CA_OP10E_D.cool_system.Cool_Motor1_Temp4', 'ns=2;s=CA_OP10E_D.cool_system.Cool_Motor1_Temp3', 'ns=2;s=CA_OP10E_D.cool_system.Cool_Motor1_Temp2', 'ns=2;s=CA_OP10E_D.cool_system.Cool_Motor1_Temp1', 'ns=2;s=CA_OP10E_D.cool_system.Cool_Motor1_Temp', 'ns=2;s=CA_OP10E_D.cool_system.Cool_GearBox_Temp5', 'ns=2;s=CA_OP10E_D.cool_system.Cool_GearBox_Temp4', 'ns=2;s=CA_OP10E_D.cool_system.Cool_GearBox_Temp3', 'ns=2;s=CA_OP10E_D.cool_system.Cool_GearBox_Temp2', 'ns=2;s=CA_OP10E_D.cool_system.Cool_GearBox_Temp1', 'ns=2;s=CA_OP10E_D.cool_system.Cool_GearBox_Temp', 'ns=2;s=CA_OP10E_D.cool_system.Cool_Filter_DiffPress5', 'ns=2;s=CA_OP10E_D.cool_system.Cool_Filter_DiffPress4', 'ns=2;s=CA_OP10E_D.cool_system.Cool_Filter_DiffPress3', 'ns=2;s=CA_OP10E_D.cool_system.Cool_Filter_DiffPress2', 'ns=2;s=CA_OP10E_D.cool_system.Cool_Filter_DiffPress1', 'ns=2;s=CA_OP10E_D.cool_system.Cool_Filter_DiffPress', 'ns=2;s=CA_OP10E_D.cool_system.Cool_ChipMotor1_Vibr5', 'ns=2;s=CA_OP10E_D.cool_system.Cool_ChipMotor1_Vibr4', 'ns=2;s=CA_OP10E_D.cool_system.Cool_ChipMotor1_Vibr3', 'ns=2;s=CA_OP10E_D.cool_system.Cool_ChipMotor1_Vibr2', 'ns=2;s=CA_OP10E_D.cool_system.Cool_ChipMotor1_Vibr1', 'ns=2;s=CA_OP10E_D.cool_system.Cool_ChipMotor1_Vibr', 'ns=2;s=CA_OP10E_D.cool_system.Cool_ChipMotor1_Temp5', 'ns=2;s=CA_OP10E_D.cool_system.Cool_ChipMotor1_Temp4', 'ns=2;s=CA_OP10E_D.cool_system.Cool_ChipMotor1_Temp3', 'ns=2;s=CA_OP10E_D.cool_system.Cool_ChipMotor1_Temp2', 'ns=2;s=CA_OP10E_D.cool_system.Cool_ChipMotor1_Temp1', 'ns=2;s=CA_OP10E_D.cool_system.Cool_ChipMotor1_Temp', 'ns=2;s=CA_OP10E_D.cool_system.Cool_ChipMotor1_CurrC5', 'ns=2;s=CA_OP10E_D.cool_system.Cool_ChipMotor1_CurrC4', 'ns=2;s=CA_OP10E_D.cool_system.Cool_ChipMotor1_CurrC3', 'ns=2;s=CA_OP10E_D.cool_system.Cool_ChipMotor1_CurrC2', 'ns=2;s=CA_OP10E_D.cool_system.Cool_ChipMotor1_CurrC1', 'ns=2;s=CA_OP10E_D.cool_system.Cool_ChipMotor1_CurrC', 'ns=2;s=CA_OP10E_D.cool_system.Cool_ChipMotor1_CurrB5', 'ns=2;s=CA_OP10E_D.cool_system.Cool_ChipMotor1_CurrB4', 'ns=2;s=CA_OP10E_D.cool_system.Cool_ChipMotor1_CurrB3', 'ns=2;s=CA_OP10E_D.cool_system.Cool_ChipMotor1_CurrB2', 'ns=2;s=CA_OP10E_D.cool_system.Cool_ChipMotor1_CurrB1', 'ns=2;s=CA_OP10E_D.cool_system.Cool_ChipMotor1_CurrB', 'ns=2;s=CA_OP10E_D.cool_system.Cool_ChipMotor1_CurrA5', 'ns=2;s=CA_OP10E_D.cool_system.Cool_ChipMotor1_CurrA4', 'ns=2;s=CA_OP10E_D.cool_system.Cool_ChipMotor1_CurrA3', 'ns=2;s=CA_OP10E_D.cool_system.Cool_ChipMotor1_CurrA2', 'ns=2;s=CA_OP10E_D.cool_system.Cool_ChipMotor1_CurrA1', 'ns=2;s=CA_OP10E_D.cool_system.Cool_ChipMotor1_CurrA'];
*/
var time = process.hrtime();


var read = function() {
    
    /*
    var date = new Date();
    console.log("r",date.getTime()/1000 );  
    console.log("-")
    */
    the_session.readVariableValue(//      nconf.get("server").tag_array,  //points array
    //TimestampsToReturn
    tags, function(err, dataValues, diagnostics) {
        //the_session.readVariableValue(["ns=2;s=Channel1.Device1.MT","ns=2;s=Channel1.Device1.Tag1"], function(err,dataValues,diagnostics) {
        
        //console.log(dataValues)
        var now = (new Date()).valueOf();
        
        //console.log(now.getMillisconds() );
        
        //var date = new Date();
        //console.log("g",date.getTime()/1000 );  
        
        //var hrTime = process.hrtime()
        
        //console.log(hrTime)
        //console.log(hrTime[0] * 1000000 + hrTime[1] / 1000)
        
        /*
        var diff = process.hrtime(time);
        
        var d = (diff[0] * 1e9 + diff[1])/1000000
        
        console.log('benchmark took %d ms', d);
        */
        if (!err) {
            
            
            var points = {"points":[[now]], "name":"ts02","columns":["time","Cool_System_Press5", "Cool_System_Press4", "Cool_System_Press3", "Cool_System_Press2", "Cool_System_Press1", "Cool_System_Press", "Cool_System_Flow5", "Cool_System_Flow4", "Cool_System_Flow3", "Cool_System_Flow2", "Cool_System_Flow1", "Cool_System_Flow", "Cool_Motor1_Vibr5", "Cool_Motor1_Vibr4", "Cool_Motor1_Vibr3", "Cool_Motor1_Vibr2", "Cool_Motor1_Vibr1", "Cool_Motor1_Vibr", "Cool_Motor1_Temp5", "Cool_Motor1_Temp4", "Cool_Motor1_Temp3", "Cool_Motor1_Temp2", "Cool_Motor1_Temp1", "Cool_Motor1_Temp", "Cool_GearBox_Temp5", "Cool_GearBox_Temp4", "Cool_GearBox_Temp3", "Cool_GearBox_Temp2", "Cool_GearBox_Temp1", "Cool_GearBox_Temp", "Cool_Filter_DiffPress5", "Cool_Filter_DiffPress4", "Cool_Filter_DiffPress3", "Cool_Filter_DiffPress2", "Cool_Filter_DiffPress1", "Cool_Filter_DiffPress", "Cool_ChipMotor1_Vibr5", "Cool_ChipMotor1_Vibr4", "Cool_ChipMotor1_Vibr3", "Cool_ChipMotor1_Vibr2", "Cool_ChipMotor1_Vibr1", "Cool_ChipMotor1_Vibr", "Cool_ChipMotor1_Temp5", "Cool_ChipMotor1_Temp4", "Cool_ChipMotor1_Temp3", "Cool_ChipMotor1_Temp2", "Cool_ChipMotor1_Temp1", "Cool_ChipMotor1_Temp", "Cool_ChipMotor1_CurrC5", "Cool_ChipMotor1_CurrC4", "Cool_ChipMotor1_CurrC3", "Cool_ChipMotor1_CurrC2", "Cool_ChipMotor1_CurrC1", "Cool_ChipMotor1_CurrC", "Cool_ChipMotor1_CurrB5", "Cool_ChipMotor1_CurrB4", "Cool_ChipMotor1_CurrB3", "Cool_ChipMotor1_CurrB2", "Cool_ChipMotor1_CurrB1", "Cool_ChipMotor1_CurrB", "Cool_ChipMotor1_CurrA5", "Cool_ChipMotor1_CurrA4", "Cool_ChipMotor1_CurrA3", "Cool_ChipMotor1_CurrA2", "Cool_ChipMotor1_CurrA1", "Cool_ChipMotor1_CurrA"]}
            
            dataValues.forEach(function(data, index) {
                
                var tag = tags[index]
                var p = tag.split("=")[2]
                //console.log(p)
                var tag1 = p.replace(/\./g,":")
                
               // console.log(tag1);
                var d = data.value.value
                
                points.points[0].push(d)
                //console.log(d)
                //console.log(d);
                //logger.debug(tags[index]);
               // logger.debug(d)
            });
            
            points_str = JSON.stringify([points])
            //console.log(JSON.stringify(points));
            
           
          
      
            points_push(points_str)
            
        }
    }
    );
};


function points_push(points_str){
    
    console.log(points_str) 
           
    
    }

    
    
    async.waterfall([ function(callback) {
    client.connect(endpointUrl, function(err) {
        if (err) {
            console.log(" cannot connect to endpoint :", endpointUrl);
            callback("err");
        } else {
            console.log("connected !");
            callback(null, "connected");
        }
    });
}, function(status, callback) {
    console.log("createSession:", status);
    client.createSession(function(err, session) {
        if (err) {
            console.log("err:", err);
            callback("err");
        } else {
            the_session = session;
            //console.log("session:", the_session)
            callback(null, "session");
        }
    });
} ], function(err, result) {
    // result now equals 'done'    
    //assert(the_session)
    setInterval(read, 1000);
    console.log("result:", result);
});