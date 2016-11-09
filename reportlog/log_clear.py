#!/usr/bin/python
#-*- coding: utf-8 -*-
import os
import sys

os.chdir('/usr/local/bluedon')
if '/usr/local/bluedon' not in sys.path:
    sys.path.append('/usr/local/bluedon')

import time
import commands
from logging import getLogger
from homepage.system_usage import disk_usage
from db.config1 import fetchone_sql,fetchall_sql,execute_sql
from utils.log_logger import FWLOG_DEBUG


PATH_ARCH = r'/var/log_bak/'
PATH_SQLBAK = r'/var/log/log_tables_backup/'
MAX_USAGE = 17

logger = getLogger('log_daemon')

def oldest_arch_file(path):
    lst = commands.getoutput("ls -1tr %s |awk '{print i$0}' i=%s" % (path,path))
    return lst if lst == '' else lst.split()[0]

def oldest_sql_file(path):
    lst = commands.getoutput("find %s -name '*.sql'" % path).split()
    sort_lst = sorted(lst,key=lambda x:x.split('_')[-1])
    #return '\n'.join(sort_lst)
    return '' if sort_lst == [] else sort_lst[0]
    pass


def log_clear_arch(path):
    #FWLOG_DEBUG('processing...arch')
    oldfile = oldest_arch_file(path)
    if oldfile == '':
        return False
    os.remove(oldfile)
    # delete oldfile record in m_tblog_library
    sql = "delete from m_tblog_library where sFileName='%s'" % oldfile
    execute_sql(sql)
    logger.debug('Removed[arch file]%s' % oldfile)
    #FWLOG_DEBUG('Removed[arch file]%s' % oldfile)
    return True

def log_clear_sqlbak(path):
    #FWLOG_DEBUG('processing...sqlbak')
    oldfile = oldest_sql_file(path)
    if oldfile == '':
        return False
    os.remove(oldfile)
    logger.debug('Removed[sqlbak] %s' % oldfile)
    #FWLOG_DEBUG('Removed[sqlbak] %s' % oldfile)
    return True


def get_tb_list():
    get_tb_names = "SELECT TABLE_NAME from information_schema.`TABLES` WHERE TABLE_NAME LIKE 'm_tblog_%_2%';"
    tbs = [res['TABLE_NAME'] for res in fetchall_sql(get_tb_names)]
    return sorted(tbs,key=lambda x:x.split('_')[-1])

def log_clear_mysql():
    FWLOG_DEBUG('processing...mysql')
    delete_table = 'DROP TABLE %s'
    lst = get_tb_list()
    if not lst == []:
        execute_sql(delete_table % lst[0])
        logger.debug('Removed[Mysqltb] %s' % lst[0])
        #FWLOG_DEBUG('Removed[Mysqltb] %s' % lst[0])
        return True

    return False
    pass

def log_clear_release_disk(max_usage = MAX_USAGE):
    du = disk_usage()
    path_arch = PATH_ARCH
    path_sqlbak = PATH_SQLBAK
    while du > max_usage:
        logger.debug('DISK USAGE ALERT[%s]' % str(du))
        if False == log_clear_arch(path_arch):
            if False == log_clear_sqlbak(path_sqlbak):
                if False == log_clear_mysql():
                    FWLOG_DEBUG('Nothing to clear...')
                    logger.debug('Nothing to clear...')
                    break
        du = disk_usage()
    FWLOG_DEBUG('release disk done...')

if __name__ == '__main__':
    log_clear_release_disk()


    # test
    # print oldest_arch_file(PATH_ARCH)
    #print oldest_file('/var/log_bak/tmp')
    #print oldest_sql_file(PATH_SQLBAK)
    #log_clear_mysql()

    pass
