#!/usr/bin/env python
# -*-coding:utf-8-*-

import os
import json
import re
import pyinotify
from logging import getLogger

data_to_num = lambda ch: filter(lambda x: x in '0123456789.', ch)
end_of_string = lambda x: re.sub(r'[\.1-9]+', '', x)


class MyEventHandler(pyinotify.ProcessEvent):
    #getLogger('log_daemon').debug('EVENT: Starting monitor...')

    def process_IN_MODIFY(self, event):
        print "MODIFY event: ", event.pathname
        tw = TrafficWatch(user_down_alert, user_up_alert, app_alert, connect_alert)
        tw.traffic_alert()
        tw.nf_conntrack_count()


class TrafficWatch(object):

    def __init__(self, user_down, user_up, app_alert, connect_alert):
        self.user_down = user_down
        self.user_up = user_up
        self.app_alert = app_alert
        self.connect_alert = int(connect_alert)

    def compare_down(self, string, str_alert):
        num = float(data_to_num(string))
        num_alert = float(data_to_num(str_alert))
        str_end = end_of_string(string)
        alert_end = end_of_string(str_alert)
        if (str_end == 'KB/s' and alert_end == 'B/s') or (str_end == 'MB/s' and (alert_end == 'B/s' or alert_end == 'KB/s')):
            return string
        elif str_end == alert_end:
            return string if max(num, num_alert) == num else 'no alert'
        else:
            return 'no alert'

    def traffic_alert(self):
        f = open('/usr/local/bluedon/log/net_statistic.json', 'r')
        f_dict = json.loads(f.read())

        user_traffic = f_dict['user']
        for dic in user_traffic:
            iDownload_data = dic['iDownload']
            iUpload_data = dic['iUpload']
            if self.compare_down(iDownload_data, self.user_down) == iDownload_data:
                print "%s, %s, %s, user down alert" % (dic['iGroupID'], dic['sUserName'], iDownload_data)
                getLogger('log_daemon').debug('EVENT ALERT: user down alert:%s, %s, %s' % (dic['iGroupID'], dic['sUserName'], iDownload_data))
            elif self.compare_down(iUpload_data, self.user_up) == iUpload_data:
                print "%s, %s, %s, user up alert" % (dic['iGroupID'], dic['sUserName'], iUpload_data)
                getLogger('log_daemon').debug('EVENT ALERT: user up alert:%s, %s, %s' % (dic['iGroupID'], dic['sUserName'], iUpload_data))
            else:
                pass

        #   "application": [{"1": "28.42MB/s"}, {"0": "2.78MB/s"}],
        app_traffic = f_dict['application']
        for dic in app_traffic:
            app_data = dic.values()[0]
            app_type = dic.keys()[0]
            if self.compare_down(app_data, self.app_alert) == app_data:
                print "app alert: %s,type: %s" % (app_data, app_type)
                getLogger('log_daemon').debug('EVENT ALERT: app alert: %s, app_type: %s' % (app_data, app_type))
            else:
                pass


    def nf_conntrack_count(self):
        f = open('/proc/sys/net/netfilter/nf_conntrack_count','r')
        f_num = int(f.read())
        if f_num >= self.connect_alert:
            print "connect_count alert :%s" % f_num
            getLogger('log_daemon').debug('EVENT ALERT: connect_count: %s' % f_num)
        else:
            pass


if __name__ == '__main__':
    user_down_alert = '1MB/s'
    user_up_alert = '700KB/s'
    app_alert = '500KB/s'
    connect_alert = '40'
    #a = traffic_watch(user_down_alert, user_up_alert, app_alert, connect_alert)
    #a.traffic_alert()
    #a.nf_conntrack_count()

    # Instanciate a new WatchManager (will be used to store watches)
    wm = pyinotify.WatchManager()
    # Associate this WatchManager with a Notifier (will be used to report and process events).
    eh = MyEventHandler()
    notifier = pyinotify.Notifier(wm, default_proc_fun=eh, read_freq=180)
    # Add a new watch on needed path for ALL_EVENTS.
    wm.add_watch('/usr/local/bluedon/log/net_statistic.json', pyinotify.ALL_EVENTS, rec=True)
    # Loop forever and handle events.
    notifier.loop()

