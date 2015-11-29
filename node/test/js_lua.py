


lua_script = """if redis.call("EXISTS", KEYS[1]) == 1 then
        -- redis.call("LPUSH", "c1","chan1")
        -- redis.call("PUBLISH", "c1","new")
        local payload = redis.call("GET", KEYS[1])
        if payload == ARGV[1] then
            
            local timestamp =  redis.call("GET", KEYS[1])
            if ARGV[3] - timestamp > 3 then
                return "heartbeat"
            else
                return "same" 
            end
        else
            redis.call("SET", KEYS[1],ARGV[1])
            redis.call("SET", KEYS[2],ARGV[2])
            redis.call("LPUSH", "c1","chan2")
            redis.call("SET", "ST", ARGV[3])
            return payload -- return old val
        end
    else
        redis.call("SET", KEYS[1],ARGV[1])
        redis.call("SET", KEYS[2],ARGV[2])
        redis.call("LPUSH", "c1","chan2")
        redis.call("SET", "ST", ARGV[3])
        return nil
    end"""
    
    
for line in lua_script.split("\n"):
    print "'%s\\n' + "  % line