#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/30 11:02
# @Author  : Aries
# @Site    : 
# @File    : test.py
# @Software: PyCharm
import re

table = re.match(r'^alter\s+table\s+(\w{1,50})[.\s]*', "ALTER table WS_SQQK add wzh_start_time DATE default to_date('1970-01-01','YYYY-MM-DD');", re.I)

print(table.group(1))