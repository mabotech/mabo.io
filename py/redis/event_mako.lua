


--[[

EVAL

EVALSHA 

]]


if redis.call("EXISTS", KEYS[1]) == 1 then
    
        redis.call("LPUSH", "c1","chan1")
        redis.call("PUBLISH", "c1","new")
        -- {a}
        local payload = redis.call("GET", KEYS[1])
        if payload == ARGV[1] then
            return "same"  
        else
            redis.call("SET", KEYS[1],ARGV[1])
            return payload
        end
    else
        redis.call("SET", KEYS[1],ARGV[1])
        return nil
    end