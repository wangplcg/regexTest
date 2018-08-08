#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/1 15:54
# @Author  : Aries
# @Site    : 
# @File    : HyperLogLogTest2.py
# @Software: PyCharm

import math
import random


def low_zeros(value):
    for i in range(1, 32):
        if value >> i << i != value:
            break
    return i - 1


class BitKeeper(object):

    def __init__(self):
        self.maxbits = 0

    def random(self, m):
        bits = low_zeros(m)
        if bits > self.maxbits:
            self.maxbits = bits


class Experiment(object):
    def __init__(self, n, k = 1024):
        self.n = n
        self.k = k
        self.keepers = [BitKeeper() for i in range(k)]

    def do(self):
        for i in range(self.n):
            m = random.randint(0, 1<<32-1)
            # 确保同一个整数被分配到同一个桶里面，摘取高位后取模
            keeper = self.keepers[((m & 0xffff0000) >> 16) % len(self.keepers)]
            keeper.random(m)

    def estimate(self):
        sumbits_inverse = 0  # 零位数倒数
        for keeper in self.keepers:
            sumbits_inverse += 1.0 / float(keeper.maxbits)
        # 平均零位数
        avgbits = float(self.k)/sumbits_inverse
        # 根据桶的数量对估计值进行放大
        return 2**avgbits * self.k


for i in range(100000, 1000000, 100000):
    exp = Experiment(i)
    exp.do()
    est = exp.estimate()
    print(i, '%.2f' % est, '%.2f' % (abs(est-i) / i))