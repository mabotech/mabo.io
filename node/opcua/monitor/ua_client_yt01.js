/*

uglifyjs ua_client.js -b  --comments all > ua_client1.js
*/
var nconf = require("nconf");

var winston = require("winston");

var opcua = require("node-opcua");

var async = require("async");

var redis = require("redis");
var    db = redis.createClient();
db.select(9)

    // if you'd like to select database 3, instead of 0 (default), call
    // client.select(3, function() { /* ... */ });

db.on("error", function (err) {
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

var tags =['ns=2;s=CP_OP10C_D.cool_system.Cool_ChipMotor1_CurrA', 'ns=2;s=CP_OP10C_D.cool_system.Cool_ChipMotor1_CurrB', 'ns=2;s=CP_OP10C_D.cool_system.Cool_ChipMotor1_CurrC', 'ns=2;s=CP_OP10C_D.cool_system.Cool_ChipMotor1_Temp', 'ns=2;s=CP_OP10C_D.cool_system.Cool_ChipMotor1_Vibr', 'ns=2;s=CP_OP10C_D.cool_system.Cool_Filter_DiffPress', 'ns=2;s=CP_OP10C_D.cool_system.Cool_GearBox_Temp', 'ns=2;s=CP_OP10C_D.cool_system.Cool_Motor1_Temp', 'ns=2;s=CP_OP10C_D.cool_system.Cool_Motor1_Vibr', 'ns=2;s=CP_OP10C_D.cool_system.Cool_System_Flow', 'ns=2;s=CP_OP10C_D.cool_system.Cool_System_Press','ns=2;s=CP_OP10C_D.hyd_system.Hyd_FrDoorCls_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_FrDoorOpen_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_IndexUclamp_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_MaClampClp_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_MaClampDep_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_MaClampUcl_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_Motor1_CurrA', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_Motor1_CurrB', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_Motor1_CurrC', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_Motor1_Temp', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_PotClp_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_PotSlidMag_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_PotSlidSpdl_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_PotUcl_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_SideClp_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_SideUcl_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_SpToolClp_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_System_Flow', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_System_Oiltemp']



var time = process.hrtime();

var mk = (new Date()).valueOf();

var read = function() {
    
    /*
    var date = new Date();
    console.log("r",date.getTime()/1000 );  
    console.log("-")
    */
     var now = new Date()
    
    the_session.readVariableValue(//      nconf.get("server").tag_array,  //points array
    //TimestampsToReturn
    tags, function(err, dataValues, diagnostics) {
        //the_session.readVariableValue(["ns=2;s=Channel1.Device1.MT","ns=2;s=Channel1.Device1.Tag1"], function(err,dataValues,diagnostics) {
        
        //console.log(dataValues)
        /*
        .valueOf();
        
        var df = now - mk
        
        mk = now
        */
        //console.log(now.getMillisconds() );
        
        //var date = new Date();
        //console.log("g",date.getTime()/1000 );  
        
        //var hrTime = process.hrtime()
        
        //console.log(hrTime)
        //console.log(hrTime[0] * 1000000 + hrTime[1] / 1000)
        
        
        var diff = process.hrtime(time);
        
        var d = (diff[0] * 1e9 + diff[1])/1000000
        
        console.log('benchmark took %d ms', d);
        
        if (!err) {
            
            //console.log(dataValues);
            
            /*
            var points = {"points":[[now]], "name":"ts02","columns":["time","Cool_System_Press5", "Cool_System_Press4", "Cool_System_Press3", "Cool_System_Press2", "Cool_System_Press1", "Cool_System_Press", "Cool_System_Flow5", "Cool_System_Flow4", "Cool_System_Flow3", "Cool_System_Flow2", "Cool_System_Flow1", "Cool_System_Flow", "Cool_Motor1_Vibr5", "Cool_Motor1_Vibr4", "Cool_Motor1_Vibr3", "Cool_Motor1_Vibr2", "Cool_Motor1_Vibr1", "Cool_Motor1_Vibr", "Cool_Motor1_Temp5", "Cool_Motor1_Temp4", "Cool_Motor1_Temp3", "Cool_Motor1_Temp2", "Cool_Motor1_Temp1", "Cool_Motor1_Temp", "Cool_GearBox_Temp5", "Cool_GearBox_Temp4", "Cool_GearBox_Temp3", "Cool_GearBox_Temp2", "Cool_GearBox_Temp1", "Cool_GearBox_Temp", "Cool_Filter_DiffPress5", "Cool_Filter_DiffPress4", "Cool_Filter_DiffPress3", "Cool_Filter_DiffPress2", "Cool_Filter_DiffPress1", "Cool_Filter_DiffPress", "Cool_ChipMotor1_Vibr5", "Cool_ChipMotor1_Vibr4", "Cool_ChipMotor1_Vibr3", "Cool_ChipMotor1_Vibr2", "Cool_ChipMotor1_Vibr1", "Cool_ChipMotor1_Vibr", "Cool_ChipMotor1_Temp5", "Cool_ChipMotor1_Temp4", "Cool_ChipMotor1_Temp3", "Cool_ChipMotor1_Temp2", "Cool_ChipMotor1_Temp1", "Cool_ChipMotor1_Temp", "Cool_ChipMotor1_CurrC5", "Cool_ChipMotor1_CurrC4", "Cool_ChipMotor1_CurrC3", "Cool_ChipMotor1_CurrC2", "Cool_ChipMotor1_CurrC1", "Cool_ChipMotor1_CurrC", "Cool_ChipMotor1_CurrB5", "Cool_ChipMotor1_CurrB4", "Cool_ChipMotor1_CurrB3", "Cool_ChipMotor1_CurrB2", "Cool_ChipMotor1_CurrB1", "Cool_ChipMotor1_CurrB", "Cool_ChipMotor1_CurrA5", "Cool_ChipMotor1_CurrA4", "Cool_ChipMotor1_CurrA3", "Cool_ChipMotor1_CurrA2", "Cool_ChipMotor1_CurrA1", "Cool_ChipMotor1_CurrA"]}
            */
                
                
             var points  = []
                
            var timestamp = now.toISOString() 
            
            points.push(timestamp)
            
            dataValues.forEach(function(data, index) {
                
                var tag = tags[index]
                var p = tag.split("=")[2]
                //console.log(p)
                var tag1 = p.replace(/\./g,":")
                
               // console.log(tag1);
                var d;
             
           
                if (data.value != null){
                    // d = data.value.value;
                       d = data.value.value.toFixed(2);
                }else{
                    d = null;
                    
                    }
               
                points.push(d)
                //console.log(d)
                //console.log(d);
                //logger.debug(tags[index]);
               // logger.debug(d)
            });
            
            //console.log( JSON.stringify(points))
            console.log(".")
            s01 = JSON.stringify(points).replace("[",",")
            s01 = s01.replace("]","")
            logger.debug( s01)
            
            points_str = JSON.stringify([points])
            //console.log(JSON.stringify(points));
            
           
          
           //points_push(points_str);
            
            
        }
    }
    );
};


function points_push(points_str){
    
    db.publish("act","msg")
    db.lpush("Queue", points_str)  
    
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
    
    header = ["timestamp", "cool_system.Cool_ChipMotor1_CurrA", "cool_system.Cool_ChipMotor1_CurrB", "cool_system.Cool_ChipMotor1_CurrC", "cool_system.Cool_ChipMotor1_Temp", "cool_system.Cool_ChipMotor1_Vibr", "cool_system.Cool_Filter_DiffPress", "cool_system.Cool_GearBox_Temp", "cool_system.Cool_Motor1_Temp", "cool_system.Cool_Motor1_Vibr", "cool_system.Cool_System_Flow", "cool_system.Cool_System_Press", "hyd_system.Hyd_FrDoorCls_Press", "hyd_system.Hyd_FrDoorOpen_Press", "hyd_system.Hyd_IndexUclamp_Press", "hyd_system.Hyd_MaClampClp_Press", "hyd_system.Hyd_MaClampDep_Press", "hyd_system.Hyd_MaClampUcl_Press", "hyd_system.Hyd_Motor1_CurrA", "hyd_system.Hyd_Motor1_CurrB", "hyd_system.Hyd_Motor1_CurrC", "hyd_system.Hyd_Motor1_Temp", "hyd_system.Hyd_PotClp_Press", "hyd_system.Hyd_PotSlidMag_Press", "hyd_system.Hyd_PotSlidSpdl_Press", "hyd_system.Hyd_PotUcl_Press", "hyd_system.Hyd_SideClp_Press", "hyd_system.Hyd_SideUcl_Press", "hyd_system.Hyd_SpToolClp_Press", "hyd_system.Hyd_System_Flow", "hyd_system.Hyd_System_Oiltemp"]
    
    h01 = JSON.stringify(header).replace("[",",")
    h01 = h01.replace("]","")
    //logger.debug( h01) 

    
    setInterval(read, 90);
    console.log("result:", result);
});