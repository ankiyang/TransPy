#!/usr/bin/python2.7
# -*-coding:utf-8-*-

import sqlparse

sql = 'select * from "someschema"."mytable" where id = 1'
parsed = sqlparse.parse(sql)

stmt = parsed[0]
print stmt.tokens

str(stmt) # 'select * from "someschema"."mytable" where id = 1'

str(stmt.tokens[-1])  # or just the WHERE part #'where id = 1'