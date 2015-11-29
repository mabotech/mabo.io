
    var redis = require("redis"),
        client = redis.createClient();
        client.select(9)

    // if you'd like to select database 3, instead of 0 (default), call
    // client.select(3, function() { /* ... */ });

    client.on("error", function (err) {
        console.log("Error " + err);
    });

    
    /*
    client.set("string key", "string val", redis.print);
    client.hset("hash key", "hashtest 1", "some value", redis.print);
    client.hset(["hash key", "hashtest 2", "some other value"], redis.print);
    
    client.hkeys("hash key", function (err, replies) {
        console.log(replies.length + " replies:");
        replies.forEach(function (reply, i) {
            console.log("    " + i + ": " + reply);
        });
        client.quit();
    });
    
    */
    
    lua_script ='if redis.call("EXISTS", KEYS[1]) == 1 then\n' + 
'        -- redis.call("LPUSH", "c1","chan1")\n' + 
'        redis.call("PUBLISH", "c2",KEYS[1])\n' + 
'     --   redis.call("SET", "ST", ARGV[3])\n' + 
'        local payload = redis.call("GET", KEYS[1])\n' + 
'        if payload == ARGV[1] then\n' + 
'            \n' + 
'            local timestamp =  redis.call("GET", "ST")\n' + 
'            if ARGV[3] - timestamp > 10000 then\n' + 
'        redis.call("SET", "ST", ARGV[3])\n' + 
'                return ARGV[3] - timestamp \n' + 
'            else\n' + 
'                return "same" \n' + 
'            end\n' + 
'        else\n' + 
'            redis.call("SET", KEYS[1],ARGV[1])\n' + 
'            redis.call("SET", KEYS[2],ARGV[2])\n' + 
'            redis.call("LPUSH", "c1","chan2")\n' + 
'            redis.call("PUBLISH", "c2", KEYS[1])\n' + 
'            redis.call("SET", "ST", ARGV[3])\n' + 
'            return payload -- return old val\n' + 
'        end\n' + 
'    else\n' + 
'        redis.call("SET", KEYS[1],ARGV[1])\n' + 
'        redis.call("SET", KEYS[2],ARGV[2])\n' + 
'        redis.call("LPUSH", "c1","chan2")\n' + 
'        redis.call("PUBLISH", "c2", KEYS[1])\n' +
'        redis.call("SET", "ST", ARGV[3])\n' + 
'        return nil\n' + 
'    end\n'
    
    args = new Array(7)
    
args[0] = lua_script
args[1] = 2
args[2] = 'a:b:c'

args[3] = 'a:b:c_st'
args[4] = '22'
args[5] = (new Date()).valueOf()
args[6] = (new Date()).valueOf()
    
    
    
       client.eval(args, function(err, res){          
           
           console.log(err);
           console.log(res);           
           
           })
           
           
           //client.quit()