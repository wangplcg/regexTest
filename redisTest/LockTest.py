#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/1 10:00
# @Author  : Aries
# @Site    : 
# @File    : LockTest.py
# @Software: PyCharm

import redis
import threading


locks = threading.local()
locks.redis = {}


def key_for(user_id):
    return "account_{}".format(user_id)


def _lock(client, key):
    return bool(client.set(key, True, nx=True, ex=5))


def _unlock(client, key):
    client.delete(key)


def lock(client, user_id):
    key = key_for(user_id)
    if key in locks.redis:
        locks.redis[key] += 1
        return True
    ok = _lock(client, key)
    if not ok:
        return False
    locks.redis[key] = 1
    return True


def unlock(client, user_id):
    key = key_for(user_id)
    if key in locks.redis:
        locks.redis[key] -= 1
        if locks.redis[key] <= 0:
            del locks.redis[key]
        return True
    return False


# host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
pool = redis.ConnectionPool(host='47.100.23.48', port=6379, decode_responses=True, password=951213)
client = redis.StrictRedis(connection_pool=pool)
print("lock", lock(client, "codehole"))
print("lock", lock(client, "codehole"))
print("unlock", unlock(client, "codehole"))
print("unlock", unlock(client, "codehole"))