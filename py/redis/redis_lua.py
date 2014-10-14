# -*- coding: utf-8 -*-


"""

redis lua

redis eval, notyify in lua script

"""

import time

import redis



def main(key, val):
    # connection pool
    r = redis.Redis(host='localhost', port=6379, db=5)  

    d = {"a":"v1"}
    
    """
    eval("lua script","number of kkeys", keys[],argv[])
    KEYS[1]
    ARGV[1]
    
    compare value 
    update value when change
    create job to update db when value change
    set heartbeat pre tag
    """

    
    lua_code = """if redis.call("EXISTS", KEYS[1]) == 1 then
        
        redis.call("SET", "ST", ARGV[2])
        
        redis.call("LPUSH", "c1","chan1")
        redis.call("PUBLISH", "c1","new")
        -- {a}
        local payload = redis.call("GET", KEYS[1])
        if payload == ARGV[1] then
            return "same"  
        else
            redis.call("SET", KEYS[1],ARGV[1])
            return payload
        end
    else
        redis.call("SET", KEYS[1],ARGV[1])
        redis.call("LPUSH", "c1","chan1")
        return nil
    end""".format(**d)
    
    #print(lua_code)
    #benchmark
    """
    0.22 ms
    4545 times/second
    """
    t1 = time.time()
    
    stamp = t1*1000
    
    n = 1
    for i in xrange(0, n):
        v = r.eval(lua_code, 1, key, val, stamp)

    t2 = time.time()

    t =  (t2-t1)*1000/n

    print("%sms" %(t))
    #print(1000/t)
    print(v)
    
    h = r.script_load(lua_code)
    print h
    #print dir(r)
    
if __name__ == "__main__":
    key = "x"
    val = "abc"
    main(key, val)