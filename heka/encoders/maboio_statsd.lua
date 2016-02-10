-- 
-- 
-- 

--[[

--]]

require "cjson"

function process_message ()
    
    local time = read_message("Timestamp") -- {a="mabo"}
    --local msg = read_message("Fields[msg]")
    --local logger = read_message("Fields[logger]")
    local payload = read_message("Payload")
    --local uuid = read_message("Uuid")
    --local pid = read_message("Pid")
    local output = cjson.encode({payload=payload})
    -- local output = {name=name}
    
    -- inject_payload("json", "heka",cjson.encode(output))
    inject_payload("json","openresty",output)
    
    return 0
end

