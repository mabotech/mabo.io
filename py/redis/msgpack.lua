--[[

cmsgpack.pack(lua_obj)

]]

local msgpack = cmsgpack.pack({time = ARGV[2],  state = KEYS[1]})

redis.call("LPUSH", "q2", msgpack) 

return 1