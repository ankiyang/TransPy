import os
import time
from db.config1 import execute_sql,fetchone_sql,fetchall_sql
from db.db_log_tables_reset import TB_3307
from utils.log_logger import FWLOG_DEBUG


tb_list=["http_log","dns_log","fast_log","eve_json",
         "iptables-ng_log","ddos_log","url_log","app_admin",
         "evil_code","info_leak","webaudit_log","web_app"]

class log_size_record():
    def __init__(self,path = "log_size_record"):

        execute_sql(TB_3307('m_tblog_size_record'))
        sql = 'SELECT COUNT(*) FROM m_tblog_size_record;'
        t = int(time.time())

        for tb in tb_list:
            sql = 'select * from m_tblog_size_record where sLogName="%s"'
            if fetchone_sql(sql % tb) == None:
                _sql = ('insert into m_tblog_size_record(sLogName,sImportSize,'
                        'iTime) values("%s",%s,%s)')
                execute_sql(_sql % (tb,0,t))


    def set_record(self,log,size):
        if not log in tb_list:
            FWLOG_DEBUG('Invalid Log Name')
            return
        t = int(time.time())

        sql = 'update m_tblog_size_record set sImportSize=%s,iTime=%s where sLogName="%s"' % (size,t,log)
        execute_sql(sql)


    def update_record(self):
        pass

    def get_record_by(self,log):
        sql = 'select sImportSize from m_tblog_size_record where sLogName="%s"' % log
        res = int(fetchone_sql(sql)['sImportSize'])

        return res

    def get_record(self):
        sql = 'select sLogName,sImportSize from m_tblog_size_record'
        d = {str(res['sLogName']):int(res['sImportSize']) for res in fetchall_sql(sql)}
        return d

    def clear_record(self,tb='all'):
        if tb == 'all':
            for t in tb_list:
                self.set_record(t,0)
        elif tb in tb_list:
            self.set_record(tb,0)
        else:
            FWLOG_DEBUG('log_size_record:no tb name %s' % tb)
if __name__ == "__main__":
    #log_record().update_record()
    lr = log_size_record()
    #lr.set_record("http_log",1023)
    #lr.clear_record('web_app')
    ##lr.update_record()
    lr.get_record_by('fast_log')
    #lr.get_record()


