#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/7 9:30
# @Author  : Aries
# @Site    : 
# @File    : SimpleLimit.py
# @Software: PyCharm

# coding: utf8

import time
import redis

pool = redis.ConnectionPool(host='47.100.23.48', port=6379, decode_responses=True, password=951213)
client = redis.StrictRedis(connection_pool=pool)


def is_action_allowed(user_id, action_key, period, max_count):
    key = 'hist:%s:%s' % (user_id, action_key)
    now_ts = int(time.time() * 1000)  # 毫秒时间戳
    with client.pipeline() as pipe:  # client 是 StrictRedis 实例
        # 记录行为
        pipe.zadd(key, now_ts, now_ts)  # value 和 score 都使用毫秒时间戳
        # 移除时间窗口之前的行为记录，剩下的都是时间窗口内的
        pipe.zremrangebyscore(key, 0, now_ts - period * 1000)
        # 获取窗口内的行为数量
        pipe.zcard(key)
        # 设置 zset 过期时间，避免冷用户持续占用内存
        # 过期时间应该等于时间窗口的长度，再多宽限 1s
        pipe.expire(key, period + 1)
        # 批量执行
        # _, _, current_count, _ = pipe.execute()
        print(pipe.execute())
    # 比较数量是否超标
    # return current_count <= max_count
    return True

for i in range(20):
    print(is_action_allowed("laoqian", "reply", 60, 5))
