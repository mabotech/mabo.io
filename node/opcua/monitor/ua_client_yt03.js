/*

uglifyjs ua_client.js -b  --comments all > ua_client1.js
*/
var nconf = require("nconf");
nconf.file("config3.json");

var winston = require("winston");
var opcua = require("node-opcua");
var async = require("async");
var redis = require("redis");

var endpointUrl = nconf.get("server").endpointUrl;

var client = new opcua.OPCUAClient();

//var sub1 = opcua.ClientSubscription();
var the_session = null;

var db = redis.createClient();
db.select(9)

db.on("error", function (err) {
    console.log("Error " + err);
});

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

var logger2 = winston.loggers.add("server", {
    file: nconf.get("logging2")
});


var i = 0;

var t = new Date().getTime();

/*
var tags = [ "ns=2;s=Channel1.Device1.fV1", "ns=2;s=Channel1.Device1.fV2", "ns=2;s=Channel1.Device1.MT", "ns=2;s=Channel1.Device1.Tag1", "ns=2;s=Channel1.Device1.Tag2", "ns=2;s=Channel1.Device1.test" ];
*/

/*
var tags =['ns=2;s=CP_OP10C_D.cool_system.Cool_ChipMotor1_CurrA', 'ns=2;s=CP_OP10C_D.cool_system.Cool_ChipMotor1_CurrB', 'ns=2;s=CP_OP10C_D.cool_system.Cool_ChipMotor1_CurrC', 'ns=2;s=CP_OP10C_D.cool_system.Cool_ChipMotor1_Temp', 'ns=2;s=CP_OP10C_D.cool_system.Cool_ChipMotor1_Vibr', 'ns=2;s=CP_OP10C_D.cool_system.Cool_Filter_DiffPress', 'ns=2;s=CP_OP10C_D.cool_system.Cool_GearBox_Temp', 'ns=2;s=CP_OP10C_D.cool_system.Cool_Motor1_Temp', 'ns=2;s=CP_OP10C_D.cool_system.Cool_Motor1_Vibr', 'ns=2;s=CP_OP10C_D.cool_system.Cool_System_Flow', 'ns=2;s=CP_OP10C_D.cool_system.Cool_System_Press','ns=2;s=CP_OP10C_D.hyd_system.Hyd_FrDoorCls_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_FrDoorOpen_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_IndexUclamp_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_MaClampClp_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_MaClampDep_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_MaClampUcl_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_Motor1_CurrA', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_Motor1_CurrB', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_Motor1_CurrC', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_Motor1_Temp', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_PotClp_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_PotSlidMag_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_PotSlidSpdl_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_PotUcl_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_SideClp_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_SideUcl_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_SpToolClp_Press', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_System_Flow', 'ns=2;s=CP_OP10C_D.hyd_system.Hyd_System_Oiltemp']
*/
var points =  nconf.get("server").points;

console.log(tags);


var time = process.hrtime();

var mk = (new Date()).valueOf();


function make_tags(ns, points){

 var tags_a = []
    
    for(var i=0; i < points.length; i ++){
        
        z =  points[i]
        z2 = "ns=" + ns + ";s=" + z
        tags_a.push(z2)
        
        
        }
    //console.log(tags_a);
        
    return tags_a;
    
}

var tags = make_tags(2, points);

console.log(tags.length)
console.log(tags)

var last = (new Date()).valueOf()

var read = function() {
    
    /*
    var date = new Date();
    console.log("r",date.getTime()/1000 );  
    console.log("-")
    */
     var now = new Date()
    
    var s001 = now.valueOf() 
    
    var read_diff = s001- last
    last = s001
    
    the_session.readVariableValue(//      nconf.get("server").tag_array,  //points array
    //TimestampsToReturn
    tags, function(err, dataValues, diagnostics) {       
        
        console.log(dataValues)
        
        //console.log(diagnostics)
        //var diff = process.hrtime(time);        
        //var d = (diff[0] * 1e9 + diff[1])/1000000
        //console.log('benchmark took %d ms', d);
        
        if (!err) {
        /*
            var points = {"points":[[now]], "name":"ts02","columns":[]}
            */
                
            console.log(".")
             var points  = []
                
            var timestamp = now.toISOString() 
            
            points.push(timestamp)
            points.push(read_diff)
            
            dataValues.forEach(function(data, index) {
                
                var tag = tags[index]
                var d;             
           
                if (data.value != null){
                    // d = data.value.value;
                       d = data.value.value;//.toFixed(2);
                }else{
                    d = null;                    
                    }
               
                points.push(d)

            });            
            //console.log( JSON.stringify(points))
            //console.log(".")
            s01 = JSON.stringify(points).replace("[",",")
            s01 = s01.replace("]","")
            logger.debug( s01)            
            //points_str = JSON.stringify([points])
            //console.log(JSON.stringify(points)); 
           //points_push(points_str);     
            
        }
        else{
            
            console.log(err)
            
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
    
    header = ["timestamp", "diff", "CP_OP10C_D.cool_system.Cool_ChipMotor1_CurrA", "CP_OP10C_D.cool_system.Cool_ChipMotor1_CurrB", "CP_OP10C_D.cool_system.Cool_ChipMotor1_CurrC", "CP_OP10C_D.cool_system.Cool_ChipMotor1_Temp", "CP_OP10C_D.cool_system.Cool_ChipMotor1_Vibr", "CP_OP10C_D.cool_system.Cool_Filter_DiffPress", "CP_OP10C_D.cool_system.Cool_GearBox_Temp", "CP_OP10C_D.cool_system.Cool_Motor1_Temp", "CP_OP10C_D.cool_system.Cool_Motor1_Vibr", "CP_OP10C_D.cool_system.Cool_System_Flow", "CP_OP10C_D.cool_system.Cool_System_Press", "CP_OP10C_D.hyd_system.Hyd_FrDoorCls_Press", "CP_OP10C_D.hyd_system.Hyd_FrDoorOpen_Press", "CP_OP10C_D.hyd_system.Hyd_IndexUclamp_Press", "CP_OP10C_D.hyd_system.Hyd_MaClampClp_Press", "CP_OP10C_D.hyd_system.Hyd_MaClampDep_Press", "CP_OP10C_D.hyd_system.Hyd_MaClampUcl_Press", "CP_OP10C_D.hyd_system.Hyd_Motor1_CurrA", "CP_OP10C_D.hyd_system.Hyd_Motor1_CurrB", "CP_OP10C_D.hyd_system.Hyd_Motor1_CurrC", "CP_OP10C_D.hyd_system.Hyd_Motor1_Temp", "CP_OP10C_D.hyd_system.Hyd_PotClp_Press", "CP_OP10C_D.hyd_system.Hyd_PotSlidMag_Press", "CP_OP10C_D.hyd_system.Hyd_PotSlidSpdl_Press", "CP_OP10C_D.hyd_system.Hyd_PotUcl_Press", "CP_OP10C_D.hyd_system.Hyd_SideClp_Press", "CP_OP10C_D.hyd_system.Hyd_SideUcl_Press", "CP_OP10C_D.hyd_system.Hyd_SpToolClp_Press", "CP_OP10C_D.hyd_system.Hyd_System_Flow", "CP_OP10C_D.hyd_system.Hyd_System_Oiltemp", "CP_OP10C_D.power_system.Power_Involtage_A", "CP_OP10C_D.power_system.Power_Involtage_B", "CP_OP10C_D.power_system.Power_Involtage_C", "CP_OP10C_D.screw_system.Screw_Lub_Press", "CP_OP10C_D.sp_system.Sp_Cool_Flow", "CP_OP10C_D.sp_system.Sp_Cool_Press", "CP_OP10C_D.sp_system.Sp_CoolFilt_DiffPress", "CP_OP10C_D.sp_system.Sp_CoolMotor1_CurrA", "CP_OP10C_D.sp_system.Sp_CoolMotor1_CurrB", "CP_OP10C_D.sp_system.Sp_CoolMotor1_CurrC", "CP_OP10C_D.sp_system.Sp_CoolOil_Water", "CP_OP10C_D.sp_system.Sp_CoolReoil_Temp", "CP_OP10C_D.sp_system.Sp_Lub_Temp", "CP_OP10C_D.TEST.TEST_DATE", "CP_OP10C_D.TEST.TEST_MC", "CP_OP20C_D.cool_system.Cool_ChipMotor1_CurrA", "CP_OP20C_D.cool_system.Cool_ChipMotor1_CurrB", "CP_OP20C_D.cool_system.Cool_ChipMotor1_CurrC", "CP_OP20C_D.cool_system.Cool_ChipMotor1_Temp", "CP_OP20C_D.cool_system.Cool_ChipMotor1_Vibr", "CP_OP20C_D.cool_system.Cool_Filter_DiffPress", "CP_OP20C_D.cool_system.Cool_GearBox_Temp", "CP_OP20C_D.cool_system.Cool_Motor1_Temp", "CP_OP20C_D.cool_system.Cool_Motor1_Vibr", "CP_OP20C_D.cool_system.Cool_System_Flow", "CP_OP20C_D.cool_system.Cool_System_Press", "CP_OP20C_D.hyd_system.Hyd_FrDoorCls_Press", "CP_OP20C_D.hyd_system.Hyd_FrDoorOpen_Press", "CP_OP20C_D.hyd_system.Hyd_IndexUclamp_Press", "CP_OP20C_D.hyd_system.Hyd_MaClampClp_Press", "CP_OP20C_D.hyd_system.Hyd_MaClampDep_Press", "CP_OP20C_D.hyd_system.Hyd_MaClampUcl_Press", "CP_OP20C_D.hyd_system.Hyd_Motor1_CurrA", "CP_OP20C_D.hyd_system.Hyd_Motor1_CurrB", "CP_OP20C_D.hyd_system.Hyd_Motor1_CurrC", "CP_OP20C_D.hyd_system.Hyd_Motor1_Temp", "CP_OP20C_D.hyd_system.Hyd_PotClp_Press", "CP_OP20C_D.hyd_system.Hyd_PotSlidMag_Press", "CP_OP20C_D.hyd_system.Hyd_PotSlidSpdl_Press", "CP_OP20C_D.hyd_system.Hyd_PotUcl_Press", "CP_OP20C_D.hyd_system.Hyd_SideClp_Press", "CP_OP20C_D.hyd_system.Hyd_SideUcl_Press", "CP_OP20C_D.hyd_system.Hyd_SpToolClp_Press", "CP_OP20C_D.hyd_system.Hyd_System_Flow", "CP_OP20C_D.hyd_system.Hyd_System_Oiltemp", "CP_OP20C_D.power_system.Power_Involtage_A", "CP_OP20C_D.power_system.Power_Involtage_B", "CP_OP20C_D.power_system.Power_Involtage_C", "CP_OP20C_D.screw_system.Screw_Lub_Press", "CP_OP20C_D.sp_system.Sp_Cool_Flow", "CP_OP20C_D.sp_system.Sp_Cool_Press", "CP_OP20C_D.sp_system.Sp_CoolFilt_DiffPress", "CP_OP20C_D.sp_system.Sp_CoolMotor1_CurrA", "CP_OP20C_D.sp_system.Sp_CoolMotor1_CurrB", "CP_OP20C_D.sp_system.Sp_CoolMotor1_CurrC", "CP_OP20C_D.sp_system.Sp_CoolOil_Water", "CP_OP20C_D.sp_system.Sp_CoolReoil_Temp", "CP_OP20C_D.sp_system.Sp_Lub_Temp", "CP_OP20C_D.TEST.TEST_DATE", "CP_OP20C_D.TEST.TEST_MC"]
    
    h01 = JSON.stringify(header).replace("[",",")
    h01 = h01.replace("]","")
    //logger.debug( h01) 
    
    //read()
    setInterval(read, 1000);
    /*
    db.subscribe("act", function(msg){console.log("msg")});
        
    db.on("subscribe", function(channel, count){
        
        console.log(channel)
        
        });
    
        db.on("message", function(channel, message){
            
            //console.log(channel, message)
            read()
            
            });
            
     */       
    console.log("result:", result);
});

/*


var net = require('net');

var server = net.createServer(function (socket) {
  //socket.write('Echo server\r\n');
    
       
    
   socket.pipe(socket);
    socket.on("data", function(data){
        
          var now = new Date()
    
    //var s001 = now.valueOf() 
    
   // console.log(s001/1000)
        
        //read() // take time to run
        
        })
    socket.on("error", function(err){
    
    console.log(err)
    
    })
});

server.listen(1337, '127.0.0.1');
*/