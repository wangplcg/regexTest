#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/29 16:31
# @Author  : Aries
# @Site    : 
# @File    : sqlParserUtil.py
# @Software: PyCharm
import sqlparse
import re


class SQLParserUtil(object):
    def __init__(self, sqlPath):
        self.operPatternDict = {
                       # 'CREATE': r'^create\s+table\s+(\w{1,50})[.\s]*',
                       'ALTER': '^alter\s+table\s+(\w{1,50})[.\s]*',
                       'UPDATE': r'^update\s+(\w{1,50})[.\s]*',
                       'INSERT': r'^insert\s+into\s+(\w{1,50})[.\s]*'}
        self.sqlPath = sqlPath


    # 获取解析之后的SQL语句
    def getListSQL(self):
        with open(self.sqlPath, 'r', encoding='utf8') as sql_file:
            file_parse = sqlparse.split(sql_file.read().strip())

        rtnsql = []
        for sql in file_parse:
            sql = re.sub(r'^--.*\n', "", str(sql), re.I)
            if sql:
                rtnsql.append(sql)
        return rtnsql

    # 获取DDL语句的表名，用于后续备份
    def getDDLTableName(self):
        tableNames = []
        sqlList = self.getListSQL()
        for sql in sqlList:
            parsedSql = sqlparse.parse(sql, encoding="UTF-8")

            for item in parsedSql[0].flatten():
                if item.ttype in [sqlparse.tokens.Keyword.DDL, sqlparse.tokens.Keyword.DML] and item.value.upper() in self.operPatternDict.keys():
                    table = re.match(str(self.operPatternDict[item.value.upper()]), item.parent.value, re.I)
                    if table:
                        tableNames.append(table.group(1))
        return tableNames


if __name__ == '__main__':
    sqlParser = SQLParserUtil('E:/test/sqlfile/wscl_alter.sql')
    print("SQL 语句解析如下：\n")
    for sql in sqlParser.getListSQL():
        print(sql)
        print()

    print("SQL DDL表名为：")
    print(sqlParser.getDDLTableName())