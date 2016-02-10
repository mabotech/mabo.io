-- 
-- 
-- 

--[[

--]]

require "cjson"

function process_message ()
    
    local time = read_message("Timestamp") -- {a="mabo"}
    local msg = read_message("Fields[msg]")
    local logger = read_message("Fields[logger]")
    local task = read_message("Logger")
    --local uuid = read_message("Uuid")
    --local pid = read_message("Pid")
    local output = cjson.encode({time=time,msg=msg,logger=logger,task=task})
    -- local output = {name=name}
    
    -- inject_payload("json", "heka",cjson.encode(output))
    inject_payload("json","openresty",output)
    
    return 0
end

