#!/usr/bin/env python
# -*-coding:utf-8-*-
import os
import sys
os.chdir('/usr/local/bluedon')
if '/usr/local/bluedon' not in sys.path:
    sys.path.append('/usr/local/bluedon')
import json
import re
from logging import getLogger
import pyinotify

data_to_num = lambda ch: filter(lambda x: x in '0123456789.', ch)
end_of_string = lambda x: re.sub(r'[\.0-9]+', '', x)


class MyEventHandler(pyinotify.ProcessEvent):
    # getLogger('log_daemon').debug('EVENT: Starting monitor...')

    def process_IN_MODIFY(self, event):
        print "MODIFY event: ", event.pathname
        
        user_down_alert = '1MB/s'
        user_up_alert = '900KB/s'
        app_alert = '3MB/s'
        connect_alert = '100'

        a = TrafficWatch(user_down_alert, user_up_alert, app_alert, connect_alert)
        a.traffic_alert()
        a.nf_conntrack_count()
        a.write_json()


class TrafficWatch(object):

    def __init__(self, user_down, user_up, app_alert, connect_alert):
        self.user_down = user_down
        self.user_up = user_up
        self.app_alert = app_alert
        self.connect_alert = int(connect_alert)
        self.lines = []

        self.alert_dic = {'user_traffic_alert': [], 'app_traffic_alert': [], 'connect_alert': ''}

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

    def app_type(self):
        try:
            with open('/usr/local/bluedon/reportlog/nDPI_support_protocol_list.txt', 'r') as fp:
                self.lines = fp.readlines()
        except:
            pass

        num = lambda x: x.split(',')[0].strip('\n')
        name = lambda x: x.split(',')[1].strip('\n')
        name_type = {num(line).strip(): name(line).strip() for line in self.lines}
        return name_type


    def traffic_alert(self):
        f = open('/usr/local/bluedon/tmp/net_data_test.json', 'r')
        # import pytest
        # pytest.set_trace()
        f_dict = json.loads(f.read())

        user_traffic = f_dict['user']
        for dic in user_traffic:
            iDownload_data = dic['iDownload']
            iUpload_data = dic['iUpload']
            if self.compare_down(iDownload_data, self.user_down) == iDownload_data:
                # print "%s, %s, %s, user down alert" % (dic['iGroupID'], dic['sUserName'], iDownload_data)
                self.alert_dic['user_traffic_alert'].append(
                    {"Download_alert": iDownload_data, "sUserName": dic['sUserName'], "iGroupID": dic['iGroupID']})
            if self.compare_down(iUpload_data, self.user_up) == iUpload_data:
                # print "%s, %s, %s, user up alert" % (dic['iGroupID'], dic['sUserName'], iUpload_data)
                self.alert_dic['user_traffic_alert'].append(
                    {"iGroupID": dic['iGroupID'], "sUserName": dic['sUserName'], "Upload_alert": iUpload_data})

        app_traffic = f_dict['application']
        name_type = self.app_type()
        for dic in app_traffic:
            app_data = dic.values()[0]
            app_num = dic.keys()[0]
            app_type = name_type[app_num]
            if self.compare_down(app_data, self.app_alert) == app_data:
                # print "%s,type: %s" % (app_data, app_type)
                self.alert_dic['app_traffic_alert'].append({app_type: app_data})
            else:
                pass

    def nf_conntrack_count(self):
        f = open('/proc/sys/net/netfilter/nf_conntrack_count', 'r')
        f_num = int(f.read())
        if f_num >= self.connect_alert:
            # print "alert %s" % f_num
            self.alert_dic['connect_alert'] = str(f_num)
        else:
            pass

    def write_json(self):
        try:
            with open("/usr/local/bluedon/log/alert_data.json", "w") as json_file:
                json.dump(self.alert_dic, json_file)
        except ValueError:
            pass



if __name__ == '__main__':
    
    # a = TrafficWatch(user_down_alert, user_up_alert, app_alert, connect_alert)
    # a.traffic_alert()
    # a.nf_conntrack_count()
    # a.write_json()

    #Instanciate a new WatchManager (will be used to store watches)
    wm = pyinotify.WatchManager()
    # Associate this WatchManager with a Notifier (will be used to report and process events).
    eh = MyEventHandler()
    notifier = pyinotify.Notifier(wm, default_proc_fun=eh, read_freq=10)

    # Add a new watch on needed path for ALL_EVENTS.
    wm.add_watch('/usr/local/bluedon/tmp/net_data_test.json', pyinotify.ALL_EVENTS, rec=True)
    # Loop forever and handle events.
    notifier.loop()



