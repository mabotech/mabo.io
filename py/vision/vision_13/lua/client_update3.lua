
--[[

for AK, Vision, OPC, DB ...

]]
-- key1,argv1,argv2,argv3,argv4
-- KEYS[1], equipment
-- ARGV[1], new status value
-- ARGV[2], timestamp
-- ARGV[3], message 
-- ARGV[4], ttl

local old_status = redis.call("HGET", KEYS[1],"val")  

local is_camera = string.find(KEYS[1], "camera")

local heartbeat_key = string.format("%s_%s", KEYS[1], "heartbeat")

-- set ttl for equipment
redis.call("SET", heartbeat_key, ARGV[2], "EX", 8 ) -- 10 seconds, ARGV[4]

-- set off: 1 / not off: 0
redis.call("HSET", KEYS[1],"off",0)

-- compare old status and new status
if old_status == ARGV[1] then
    -- same val
    
    -- redis.call("LPUSH", "c1","chan2")
    redis.call("HSET", KEYS[1],"heartbeat",ARGV[2])
    
    -- redis.call("SET", heartbeat_key, "1","EX", ARGV[4])
    return "same"

else    
    -- status / value changed
    
    local starton = redis.call("HGET", KEYS[1],"starton")    
    
    -- no key?
    if starton == false then
        starton = ARGV[2]
    end
    
    local equipment_id    
    local msg
    
    if is_camera == nil then
        
        equipment_id = KEYS[1] 
    
        msg = cmsgpack.pack(
            {id=equipment_id, -- key
             pstatus = old_status,  -- only for reference
             duration = ARGV[2] - starton, 
             ch_ori_eqpt = ARGV[1], -- channel, last status
             heartbeat = ARGV[2], 
             rawdata = ARGV[3],  
             time_precision="ms"} )
    else
       -- camera
       
        equipment_id = string.sub(KEYS[1], 0, -8)  -- remove: _camera
    
        msg = cmsgpack.pack(
            {id=equipment_id, -- key
             pstatus = old_status,  -- only for reference
             duration = ARGV[2] - starton, 
             ch_occupied = ARGV[1], -- channel, last status
             heartbeat = ARGV[2], 
             rawdata = ARGV[3],  
             time_precision="ms"} )       
        
    end
    
    redis.call("HSET", KEYS[1],"val",ARGV[1]) -- equipment status
    redis.call("HSET", KEYS[1],"starton",ARGV[2])
    redis.call("HSET", KEYS[1],"heartbeat",ARGV[2])
    redis.call("HSET", KEYS[1],"rawdata",ARGV[3])
    
    -- redis.call("SET", heartbeat_key, "1","EX",ARGV[4])
    
    redis.call("RPUSH", "data_queue",msg) -- msg queue    
    redis.call("PUBLISH", "new_data","new") -- notice
    
    return old_status -- return old val
    
end

 