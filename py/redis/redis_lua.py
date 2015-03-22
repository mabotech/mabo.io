# -*- coding: utf-8 -*-


"""

redis lua

redis eval, notyify in lua script

"""

import time

import redis



def main(key, val, key2, val2):
    # connection pool
    r = redis.Redis(host='192.168.147.137', port=6389, db=0)  

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
        
        -- redis.call("SET", "ST", ARGV[3])
        
        -- redis.call("LPUSH", "c1","chan1")
        -- redis.call("PUBLISH", "c1","new")
        -- 
        local payload = redis.call("GET", KEYS[1])
        if payload == ARGV[1] then
            return "same"  
        else
            redis.call("SET", KEYS[1],ARGV[1])
            redis.call("SET", KEYS[2],ARGV[2])
            redis.call("LPUSH", "c1","chan2")
            return payload -- return old val
        end
    else
        redis.call("SET", KEYS[1],ARGV[1])
        redis.call("SET", KEYS[2],ARGV[2])
        redis.call("LPUSH", "c1","chan2")
        return nil
    end"""
    #.format(**d)
    
    #print(lua_code)
    #benchmark
    """
    0.22 ms
    4545 times/second
    """
    t1 = time.time()
    
    stamp = t1*1000
    val2 = t1*1000
    
    n = 1
    for i in xrange(0, n):
        
        v = r.eval(lua_code, 2, key, key2,  val, val2, stamp)

    t2 = time.time()

    t =  (t2-t1)*1000/n

    print("%sms" %(t))
    #print(1000/t)
    print(v)
    
    h = r.script_load(lua_code)
    print h
    
    print("evalsha %s %s %s %s %s %s %s" % (h, 2, key, key2,  val, val2, stamp)) 
    
    #print dir(r)
    
if __name__ == "__main__":
    
    key = "y:a:c"
    val = "10.8890"
    
    key2 = "y:a:c_st"
    val2 = time.time()
    
    main(key, val, key2, val2)