
-- for ak_client.py
-- key1,argv1,argv2

local payload = redis.call("HGET", KEYS[1],"val")

--redis.call("HSET", KEYS[1],"tag",ARGV[1])
--redis.call("HSET", KEYS[1],"x",ARGV[3])
--redis.call("HSET", KEYS[1],"y",ARGV[4])

if payload == ARGV[2] then
    -- redis.call("LPUSH", "c1","chan2")
    redis.call("HSET", KEYS[1],"heartbeat",ARGV[2])
    redis.call("HSET", KEYS[1],"off",0)
    
    return "same"
else            
    local starton = redis.call("HGET", KEYS[1],"starton")
    if starton == false then
        starton = ARGV[4]
    end
    
    local msg = cmsgpack.pack( 
        {id=KEYS[1], pstatus = payload, 
         duration = ARGV[4] - starton, 
         ch_ori_eqpt = ARGV[2], heartbeat=ARGV[4], 
         time_precision="ms"} 
    )
    
    redis.call("HSET", KEYS[1],"val",ARGV[2])    
    redis.call("HSET", KEYS[1],"starton",ARGV[4])
    redis.call("HSET", KEYS[1],"heartbeat",ARGV[4])
    redis.call("HSET", KEYS[1],"off",0)
    
    redis.call("RPUSH", "data_queue",msg) -- msg queue
    
    redis.call("PUBLISH", "new_data","new") -- notice
    
    return payload -- return old val
    
end

 