
redis = require("redis")
client = redis.createClient()


args = new Array(7)

lua_script = "\n
-- here is the problem\n
local res = redis.call('hmset', KEYS[1],ARGV[1])\n
print (res)\n
-- create secondary indexes\n
--\n
--\n
return 'Success'\n
"

args[0] = lua_script
args[1] = 1
args[2] = 'aac'
args[3] = 'id'
args[4] = '111'
args[5] = 'id2'
args[6] = '222'
callback = null

client.eval args, (err, res) ->
  console.log 'Result: ' + res