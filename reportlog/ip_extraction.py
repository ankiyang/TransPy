#!/usr/bin/env python
import time
import gc
import os
from reportlog.mysql_log_backup import mysql_table_exists as table_exists
from db.config1 import fetchall_sql
#today = time.strftime('%Y%m%d',time.localtime())
_day ='19700101'
today ='20100610'
tb = 'm_tblog_webapplication'
scan_list = [('m_tblog_ips',           'invasion_protect.txt'),
             ('m_tblog_webapplication','web_attract.txt'),
             ('m_tblog_ddos',          'ddos.txt'),
             ('m_tblog_evil_code',     'virus_protect.txt'),
             ('m_tblog_info_leak',     'info_leakage.txt')]

scan_record= {'m_tblog_ips':            0,
              'm_tblog_webapplication': 0,
              'm_tblog_ddos':           0,
              'm_tblog_evil_code':      0,
              'm_tblog_info_leak':      0}

RES_PATH = r'/etc/antidetect/src_file/'

def ip_extraction(log,date,target):
    tb = log + '_' + date
    #print 'processing %s to %s' % (tb,target)
    current = current_result(tb)
    pre = previous_result(target)
    new_res = current - pre
    # print new_res
    # print pre
    # print current
    with open(target,'a+') as fp:
        for res in new_res:
            fp.write(res+'\n')
    del pre
    del current
    del new_res

def current_result(tb):
    s = set()
    # index = 0 for test
    tb_type = tb[0:-9]
    index = 0
    index = int(time.time())
    global scan_record
    # if current time is newest timestamp, save it
    # scan_record is max(current_timestamp,newest_tb_timestamp)
    if scan_record[tb_type] < index:
        scan_record[tb_type] = index
    if table_exists(tb):
        # sql = 'SELECT DISTINCT id,sSourceIP FROM %s WHERE id>%s LIMIT 5000;' % (tb,scan_record[tb[0:-9]])
        sql = ('SELECT DISTINCT iTime,sSourceIP FROM %s '
               'WHERE iTime>%s GROUP BY sSourceIP LIMIT 5000;') % (tb,scan_record[tb_type])
        #sql = 'SELECT DISTINCT id,sSourceIP FROM %s' % tb
        # print sql
        result = fetchall_sql(sql)
        #for res in fetchall_sql(sql):
        for res in result:
            s.add(str(res['sSourceIP']))
            global scan_record
            # always keep the newest timestamp
            if res['iTime'] > scan_record[tb_type]:
                scan_record[tb_type] = res['iTime']
    else:
        #print '[%s] not exists' % tb
        pass
    global scan_record
    # print tb[0:-9],scan_record[tb_type]
    return s

def previous_result(txt):
    s = set()
    try:
        with open(txt,'r') as fp:
            for l in fp:
                s.add(l.strip('\n'))
        return s
    except:
        return set()

def ip_extra(start_time = 0):
    global _day
    t = time.localtime()
    today = time.strftime('%Y%m%d',t)
    # print _day,' ip_extra running... '

    if not _day == today:
        _day = today
        tmp = [os.system('rm -f %s' % RES_PATH+f[1]) for f in scan_list]
        del tmp

    tmp = [ip_extraction(tb,today,RES_PATH+fl) for (tb,fl) in scan_list]
    del tmp

if __name__ == '__main__':
    #ip_extraction(tb,today)
    #ip_extraction(scan_list[1][0],today,RES_PATH+scan_list[1][1])
    #s = previous_result(RES_PATH+scan_list[1][1])
    #print s
    #[ip_extraction(tb,today,RES_PATH+fl) for (tb,fl) in scan_list]
    while 1:
        ip_extra()
        gc.collect()
        time.sleep(1)
    pass

