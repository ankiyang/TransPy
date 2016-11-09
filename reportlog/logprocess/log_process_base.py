#!/usr/bin/env python
# coding=utf-8


import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time
import random
import string
import threading
import Queue
from multiprocessing import Pool, Manager
from db.config1 import execute_sql as exec_3307
from db.config import fetchall_sql as fcal_3306
from utils.log_logger import FWLOG_DEBUG, FWLOG_ERR
# from reportlog.log_size_record import log_size_record
from ..log_size_record import log_size_record
# from reportlog.log_statistics import ips_log_statistics_new
from ..log_statistics import ips_log_statistics_new


class LogImportStatus(object):
    def __init__(self):
        super(LogImportStatus, self).__init__()
        self.item = set()
        self._onoff = 'on'

    @property
    def onoff(self):
        return self._onoff

    @onoff.setter
    def onoff(self, value):
        if value not in ('on', 'off'):
            pass
        else:
            if value != self._onoff:
                self._onoff = value
                FWLOG_DEBUG('LOG import status = [%s]' % value)
                self.notify()

    def setON(self):
        self.onoff = 'on'

    def setOFF(self):
        self.onoff = 'off'

    def isON(self):
        return self.onoff == 'on'

    def attach(self, obj):
        self.item.add(obj)
        pass

    def discard(self, obj):
        self.item.discard(obj)

    def notify(self):
        for item in self.item:
            item.update(self.onoff)



class LogProcessBase(threading.Thread):
    def __init__(self,log_name, tb_name, path, keys):
        super(LogProcessBase, self).__init__()

        self.onoff = 'on'
        self.path = path
        self.log_name = log_name
        self.tb_name = tb_name
        self.tb = tb_name
        self.last_line = ''
        self.last_cnt = 0
        self.last_date = ''
        self.last_tb = tb_name
        self.MAX_LINE = 50000
        self.MAX_BUF = 800000
        self.MAX_PROCESS = 1
        self.interval = 1
        self.workdone = False
        self.data_files = Queue.Queue()
        self.commit_jos = None
        self.null = ("","")
        # self.imported_size = lambda x :log_size_record().get_recrod()[x]
        self.keys = ','.join(keys)
        self.event = threading.Event()
        self.fsize = lambda x: os.path.getsize(x) if os.path.exists(x) else 0

        # delete tmp files
        os.system('rm -f /dev/shm/.db_firewall_log_{n:}*'.format(n=self.tb_name))


    def update(self, onoff='on'):
        self.onoff = onoff
        if self.onoff == 'off':
            # log here
            FWLOG_ERR('%s is off' % self.tb)
        pass


    def get_ts_date(self, s, fmt):
        ta = time.strptime(s, fmt)
        ts = time.mktime(ta)
        date = time.strftime('%Y%m%d', ta)
        return int(ts), date


    def date_change(self, date):
        if self.last_date == '':
            self.last_date = date
            self.tb = self.tb_name + '_' + self.last_date
            sql = "CREATE TABLE IF NOT EXISTS `%s` LIKE `%s`" % (self.tb,
                                                                 self.tb_name)
            exec_3307(sql)

        if self.last_date != date:
            FWLOG_DEBUG('date change from %s to %s' % (self.last_date, date))
            tb = self.tb_name + '_' + date
            sql = "CREATE TABLE IF NOT EXISTS `%s` LIKE `%s`" % (tb,
                                                                 self.tb_name)
            exec_3307(sql)
            self.last_date = date
            return True

        return False

    # rewrite in subclass
    def parser_line(self, line):
        return self.null

    # rewrite in subclass
    def other_jobs(self, args):
        pass

    def create_tmp_file(self, name):
        while 1:
            randstr = ''.join (random.sample(string.ascii_letters+string.digits,9))
            data_file = r'/dev/shm/.db_firewall_log_' + name + '_' + randstr + '.xyz'
            if os.path.exists(data_file):
                continue
            else:
                os.system('touch %s' % data_file)
                break

        FWLOG_DEBUG('create file %s' % data_file)
        return data_file

    # can rewrite in subclass if args need more process
    def save_to_file(self, args, name):
        _file = self.create_tmp_file(name)
        with open(_file, 'a+') as fp:
            fp.write('\n'.join(args))
        return _file, name

    def run_process(self):
        pass
        # manager = Manager()
        # q = manager.Queue(self.MAX_PROCESS)
        # pool = Pool()
        # for i in range(self.MAX_PROCESS):
        #     pool.apply_async(self.main_loop, args=(i,))

        # while not self.workdone:
        #     time.sleep(1)

        # pool.close()
        # pool.join()


    def main_loop(self):
        args = []
        cnt = 0
        recorder = log_size_record()

        try:
            fp = open(self.path, 'r')
            fsize = self.fsize(self.path)
            imported_size = recorder.get_record_by(self.log_name)

            if imported_size == fsize:
                # import done, wait for new log
                # FWLOG_DEBUG(' import done, wait for new log')
                fp.seek(fsize)
                return

            if imported_size > fsize:
                # log file is rotated, import from beginning
                FWLOG_DEBUG('log file is rotated, import from beginning')
                recorder.set_record(self.log_name, 0)
                imported_size = 0

            fp.seek(imported_size, 0)
            where = fp.tell()
            done = False

            while not done:
                lines = fp.readlines(self.MAX_BUF)

                #if event is set
                if self.event.isSet():
                    done = True
                    break

                # end of file
                if not lines:
                    done = True
                    # self.workdone = True
                    FWLOG_DEBUG('no more line at...%s' % fp.tell())
                    continue
                for line in lines:
                    l, date = self.parser_line(line)
                    if l == '':
                        FWLOG_DEBUG('I see null line...at %s' % fp.tell())
                        continue

                    if self.last_line == '':
                        self.last_line = l

                    if self.last_line != l:
                        args.append(self.last_line + '|' + str(cnt))
                        self.last_line = l
                        cnt = 1
                    else:
                        cnt += 1


                    if self.date_change(date):
                        f, n = self.save_to_file(args, self.tb)
                        self.data_files.put((f, n))
                        self.other_jobs(args)
                        # change self.tb so next time data will save to new
                        # file
                        self.tb = self.tb_name + '_' + self.last_date
                        args = []

                    elif len(args) > self.MAX_LINE:
                        # write args to file here
                        f, n = self.save_to_file(args, self.tb)
                        self.data_files.put((f, n))
                        self.other_jobs(args)
                        args = []

            if len(args) != 0:
                # write args to file here
                f, n = self.save_to_file(args, self.tb)
                self.data_files.put((f, n))
                self.other_jobs(args)
                args = []

        except Exception as e:
            FWLOG_ERR('%s error: %s' % (self.tb_name, e))

        finally:
            recorder.set_record(self.log_name, fp.tell())
            fp.close()

        pass


    # implement with thread
    def load_data_infile(self):
        t = None

        while 1:
            if self.event.isSet():
                break
            _file, _name = self.data_files.get()
            FWLOG_DEBUG('%s Get %s, %s' % (self.tb_name, _file, _name))
            if _file and _name:
                sql = ('load data infile "%s" ignore into table `%s` '
                       'character set utf8 fields TERMINATED BY "|" '
                       'LINES TERMINATED BY "\n" ({k:})').format(k=self.keys)

                def mysql_task(f, n):
                    FWLOG_DEBUG('committing %s at table %s...' % (f, n))
                    exec_3307('ALTER TABLE %s DISABLE KEYS;' % n)
                    exec_3307(sql % (f, n))
                    exec_3307('ALTER TABLE %s ENABLE KEYS;' % n)
                    os.system('rm -f %s' % f)
                    FWLOG_DEBUG('committing %s at table %s...done' % (f, n))


                t = threading.Thread(target=mysql_task, args=(_file, _name))
                t.setDaemon(True)
                t.start()
            else:
                pass
                FWLOG_DEBUG('%s get the last message...haha' % self.tb_name)
            time.sleep(1)

        if t is not None:
            FWLOG_DEBUG('waiting load_data_infile exit...')
            t.join()
            pass
        FWLOG_DEBUG('load_data_infile exit...')
        pass

    def run(self):
        # start load_data_infile thread
        self.load_thread = threading.Thread(target=self.load_data_infile)
        self.load_thread.setDaemon(True)
        self.load_thread.start()

        while not self.workdone:
            if self.event.isSet():
                FWLOG_DEBUG('%s main_loop Event is Set...' % self.tb_name)
                self.workdone = True
                break
            if self.onoff == 'on':
                self.main_loop()

            time.sleep(self.interval)

        self.workdone = True
        self.event.set()
        self.data_files.put((None,None))
        self.load_thread.join()
        pass

    def start(self):
        super(LogProcessBase, self).start()
        pass

    def stop(self):
        self.event.set()
        self.join()

        pass


if __name__ == '__main__':
    pass
