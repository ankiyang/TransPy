#!/usr/bin/python2.7
# -*-coding:utf-8-*-

import sqlparse


# sql = 'select * from foo where id in (select id from bar);'

sql = "CREATE TABLE `m_blacklist` (" \
      "`id` int(11) NOT NULL AUTO_INCREMENT," \
      "`sSourceAddr` varchar(64) DEFAULT NULL COMMENT '来源地址'," \
      "`sStopReason` varchar(256) DEFAULT NULL COMMENT '禁止原因'," \
      "`iStopTime` int(11) DEFAULT NULL COMMENT '禁止时间'," \
      "`iStatus` varchar(4) DEFAULT NULL," \
      "`iTime` int(11) DEFAULT NULL," \
      "PRIMARY KEY (`id`)) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='黑名单';"

print(sqlparse.format(sql, encoding='utf8', reindent=False, keyword_case='upper', identifier_case='lower', output_format='python'))