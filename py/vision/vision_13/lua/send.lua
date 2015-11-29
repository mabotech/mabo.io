
if redis.call("EXISTS", KEYS[1]) == 1 then
        
        --[[
        
        heardbeat when pooling 
        
        ]] 
        
        
        
        -- redis.call("SET", "ST", ARGV[3])
        
        -- redis.call("LPUSH", "c1","chan1")
        -- redis.call("PUBLISH", "c1","new")
        
        local payload = redis.call("GET", KEYS[1])
        if payload == ARGV[1] then
            redis.call("LPUSH", "c1","chan2")
            return "same"  
        else
            redis.call("SET", KEYS[1],ARGV[1])
            redis.call("SET", KEYS[2],ARGV[2])
            redis.call("LPUSH", "c1","chan2")
            return payload -- return old val
        end
    else
        redis.call("SET", KEYS[1],ARGV[1])
        redis.call("SET", KEYS[2],ARGV[2])
        redis.call("LPUSH", "c1","chan2")
        return nil
    end