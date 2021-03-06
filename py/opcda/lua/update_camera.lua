
-- 
-- key1,argv1,argv2
-- 
-- 
-- ttl : ARGV[4]

local payload = redis.call("HGET", KEYS[1],"val")  

local heartbeat_key = string.format("%s_%s", KEYS[1], "heartbeat")

redis.call("SET", heartbeat_key, "1","EX", 20) -- ARGV[4]

if payload == ARGV[1] then
    -- redis.call("LPUSH", "c1","chan2")
    redis.call("HSET", KEYS[1],"heartbeat",ARGV[2])
    redis.call("HSET", KEYS[1],"off",0)
    -- redis.call("SET", heartbeat_key, "1","EX", ARGV[4])
    return "same"
else            
    local starton = redis.call("HGET", KEYS[1],"starton")
    
    local equipment_id = string.sub(KEYS[1], 0, -8) -- remove: _canera
    
    if starton == false then
        starton = ARGV[2]
    end
    
    local msg = cmsgpack.pack( 
        {id=equipment_id, pstatus = payload, 
         duration = ARGV[2] - starton, 
         ch_occupied=ARGV[1], 
         heartbeat=ARGV[2], 
         rawdata=ARGV[3], 
         time_precision="ms"} 
    )
    
    redis.call("HSET", KEYS[1],"val",ARGV[1])    
    redis.call("HSET", KEYS[1],"starton",ARGV[2])
    redis.call("HSET", KEYS[1],"heartbeat",ARGV[2])
    redis.call("HSET", KEYS[1],"rawdata",ARGV[3])
    redis.call("HSET", KEYS[1],"off",0)
    
    -- redis.call("SET", heartbeat_key, "1","EX",ARGV[4])
    
    redis.call("RPUSH", "data_queue",msg) -- msg queue
    
    redis.call("PUBLISH", "new_data","new") -- notice
    
    return payload -- return old val
    
end

 