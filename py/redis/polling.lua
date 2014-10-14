-- hset and heartbeat

redis.call("HINCRBY",KEYS[1],"count",1)

redis.call("HSET", KEYS[1],"timestamp",ARGV[2])

if redis.call("HEXISTS", KEYS[1],"val") == 1 then



    local payload = redis.call("HGET", KEYS[1],"val")
    
    if payload == ARGV[1] then
        return "SAME"
    else
        redis.call("HSET", KEYS[1], "val", ARGV[1])
        redis.call("LPUSH", "Que", KEYS[1])
        redis.call("PUBLISH", "Que", "new")
        return payload
    end
else
    redis.call("HSET", KEYS[1],"val",ARGV[1])
    redis.call("LPUSH", "Que", KEYS[1])
    redis.call("PUBLISH", "Que", "new")
    return nil
end