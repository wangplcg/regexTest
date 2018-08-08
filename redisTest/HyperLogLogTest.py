#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/1 14:37
# @Author  : Aries
# @Site    : 
# @File    : HyperLogLogTest.py
# @Software: PyCharm

import redis

pool = redis.ConnectionPool(host='47.100.23.48', port=6379, decode_responses=True, password=951213)
client = redis.StrictRedis(connection_pool=pool)

for i in range(1000):
    client.pfadd("codehole", "user%d" % i)
    total = client.pfcount("codehole")
    if total != i+1:
        print(total, i+1)