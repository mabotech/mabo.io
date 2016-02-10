

local socket = require("socket")
local string = require("string")
local struct = require("struct")

print(socket._VERSION)


local sock = assert(socket.connect("127.0.0.1", 23800))
sock:settimeout(0)

local cmd = "ASTZ"

local len = string.len(cmd)

local fmt = string.format("!2b%ds5b",len)

print(fmt)

fmt = "<bbsbbb"

local STX = 0x02
local BLANK = 0x20
local ETX = 0x03
local K = string.byte('K')

print(K)
--local buf = struct.pack(fmt, STX, BLANK, cmd, BLANK, K, 0, BLANK, ETX)
--local buf = struct.pack(fmt, STX, cmd, BLANK,K, ETX)

--print(buf)

local f = 'bbc4bbbbb'

print(struct.size(f))

print(string.rep("==", 20))

local packed = struct.pack(f, STX, BLANK,cmd, BLANK, K, 0, BLANK, ETX)

print(packed)

sock:send(packed)
--local a,b,c,d,e,f = struct.unpack(f, packed)
--print(a)
print(struct.unpack(f, packed))


--[[
repeat
    -- 以 1K 的字节块来接收数据，并把接收到字节块输出来
    print ("repeat")
local chunk, status, partial = sock:receive(1024)

print(status)
    
until status ~= "closed"
--]]
--[[
for i=0, 10, 1 do
    local chunk, status, partial = sock:receive(2)
    print(chunk)
    --print(partial)
    print(status)
    --print(i)
end
]]


 local recvt, sendt, status = socket.select({sock}, nil, 1)
 
 print(#recvt)
 

    while #recvt > 0 do
        -- print(1)
        local response, receive_status = sock:receive()
        print(receive_status)
        if receive_status ~= "closed" then
            if response then
                --print(response)
                recvt, sendt, status = socket.select({sock}, nil, 1)
                print (#recvt)
            end
        else
            break
        end
    end

 -- sock:close()