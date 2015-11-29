      
local payload = redis.call("HGET", KEYS[1],"val")        
 
if payload == ARGV[1] then
    -- redis.call("LPUSH", "c1","chan2")
    redis.call("HSET", KEYS[1],"heartbeat",ARGV[2])
    redis.call("HSET", KEYS[1],"off",0)
    
    return "same"
else            
    local starton = redis.call("HGET", KEYS[1],"starton")
    if starton == false then
        starton = ARGV[2]
    end
    
    local msg = cmsgpack.pack( 
        {id=KEYS[1], pstatus = payload, 
         duration = ARGV[2] - starton, 
         ch_ori_eqpt=ARGV[1], heartbeat=ARGV[2], 
         time_precision="ms"} 
    )
    
    redis.call("HSET", KEYS[1],"val",ARGV[1])    
    redis.call("HSET", KEYS[1],"starton",ARGV[2])
    redis.call("HSET", KEYS[1],"heartbeat",ARGV[2])
    redis.call("HSET", KEYS[1],"off",0)
    
    redis.call("RPUSH", "data_queue",msg) -- msg queue
    
    redis.call("PUBLISH", "new_data","new") -- notice
    
    return payload -- return old val
    
end

 