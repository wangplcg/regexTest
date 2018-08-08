#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/1 14:37
# @Author  : Aries
# @Site    : 
# @File    : Connection.py
# @Software: PyCharm

import redis

# host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
def getClient() :
    pool = redis.ConnectionPool(host='47.100.23.48', port=6379, decode_responses=True, password=951213)
    client = redis.StrictRedis(connection_pool=pool)
    return client