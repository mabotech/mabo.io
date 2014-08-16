# -*- coding: utf-8 -*-

"""
enqueue to redis

"""

import time

import redis

REDIS_MAX_CONNECTIONS = 100

def main():
    
    rpool = redis.ConnectionPool(host='localhost', port=6379, db=6, \
                max_connections=REDIS_MAX_CONNECTIONS)

    rclient = redis.Redis(connection_pool=rpool) 


    t = time.time()

    rclient.rpush("point:abc:def",t)


    rclient.rpush("point:abc",t)

    d = {"point:abc:timestamp":t}

    rclient.mset(d)

    rclient.mset({"point:abc:pstate":t})

    rclient.publish("point:abc","ok")
    
if __name__ == '__main__':
    main()