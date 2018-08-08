#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/7 9:42
# @Author  : Aries
# @Site    : 
# @File    : test1.py
# @Software: PyCharm

import redis
import time
from concurrent.futures import ProcessPoolExecutor

r = redis.Redis(host='47.100.23.48', port=6379, password='951213')
# pool = redis.ConnectionPool(host='47.100.23.48', port=6379, decode_responses=True, password=951213)
# r = redis.StrictRedis(connection_pool=pool)

def try_pipeline():
    start = time.time()
    with r.pipeline(transaction=False) as p:
        p.sadd('seta', 1).sadd('seta', 2).srem('seta', 2).lpush('lista', 1).lrange('lista', 0, -1)
        p.execute()
    print(time.time() - start)


def without_pipeline():
    start = time.time()
    r.sadd('seta', 1)
    r.sadd('seta', 2)
    r.srem('seta', 2)
    r.lpush('lista', 1)
    r.lrange('lista', 0, -1)
    print(time.time() - start)


def worker():
    while True:
        try_pipeline()


with ProcessPoolExecutor(max_workers=12) as pool:
    for i in range(10):
        pool.submit(worker())