#!/usr/bin/env python
# -*-coding:utf-8-*-
import os
import sys
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.rrule import *



#  >>>python remove_file.py [folder path] [days/months]

path = '/home/ankiy/var'

input_num = lambda x: int(re.sub("\D", "", "%s" % x))


class RemoveDaysFile(object):
    """
    threshold_date: acquire the prior date
    mid_dates: acquire a list of middle dates
    traversal: traverse the given folder and remove unnecessary file
    """

    def __init__(self):
        self.now_date = datetime.now()
        self.now = self.now_date.strftime('%Y%m%d')
        self.mid_list = []
        self.before_date = self.now_date

    def threshold_date(self, gap_days='10days'):
        if gap_days.find('day') >= 0:
            days_num = -input_num(gap_days)
            self.before_date = self.now_date + relativedelta(days=days_num)
        elif gap_days.find('month') >= 0:
            months_num = -input_num(gap_days)
            self.before_date = self.now_date + relativedelta(months=months_num)
        else:
            self.before_date = self.now_date + relativedelta(days=-10)

    def mid_dates(self):
        date_start = self.before_date
        date_end = self.now_date
        mid = list(rrule(DAILY, dtstart=date_start, until=date_end))
        self.mid_list = [m.strftime('%Y%m%d') for m in mid]

    def traversal(self, path):
        for parent, dirs, files in os.walk(path, topdown=False):
            try:
                for f in files:
                    if f.endswith(".sql") or f.endswith(".csv"):
                        file_name = f.split('.')[0]
                        if file_name[-8:] not in self.mid_list:
                            file_path = os.path.join(parent, f)
                            os.remove("%s" % file_path)
                            print "remove %s done" % file_name
                        else:
                            pass
                    else:
                        pass
            except Exception, e:
                print e


if __name__ == "__main__":

    if len(sys.argv) == 3:
        path = sys.argv[1]
        days = sys.argv[2]

        rem = RemoveDaysFile()
        rem.threshold_date(days)
        rem.mid_dates()
        rem.traversal(path)
    else:
        "INFO ERROR: Please input the path of sql folder and days/months u wanted correctly."

