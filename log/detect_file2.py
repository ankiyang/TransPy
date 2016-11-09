#!/usr/bin/env python
# -*-coding:utf-8-*-

# import pyinotify,subprocess
#
#
# def onChange(ev):
#     cmd = ['/bin/echo', 'File', ev.pathname, 'changed']
#     subprocess.Popen(cmd).communicate()
#
#
# wm = pyinotify.WatchManager()
# wm.add_watch('file.watched', pyinotify.IN_MODIFY, onChange)
# notifier = pyinotify.Notifier(wm)
# notifier.loop()

import os
import datetime
import pyinotify
import logging
from user_traffic_alert import traffic_watch

user_down_alert = '8MB/s'
user_up_alert = '1MB/s'
app_down_alert = '8MB/s'
app_up_alert = '2MB/s'
connect_alert = '34'

class MyEventHandler(pyinotify.ProcessEvent):
    logging.basicConfig(level=logging.INFO, filename='/home/ankiy/log/monitor/monitor.log')

    logging.info("Starting monitor...")

    def process_IN_ACCESS(self, event):
        print "ACCESS event:", event.pathname
        logging.info("ACCESS event : %s  %s" % (os.path.join(event.path, event.name), datetime.datetime.now()))

    def process_IN_ATTRIB(self, event):
        print "ATTRIB event:", event.pathname
        logging.info("IN_ATTRIB event : %s  %s" % (os.path.join(event.path, event.name), datetime.datetime.now()))

    def process_IN_CLOSE_NOWRITE(self, event):
        print "CLOSE_NOWRITE event:", event.pathname
        logging.info("CLOSE_NOWRITE event : %s  %s" % (os.path.join(event.path, event.name), datetime.datetime.now()))


    def process_IN_CLOSE_WRITE(self, event):
        print "CLOSE_WRITE event:", event.pathname
        logging.info("CLOSE_WRITE event : %s  %s" % (os.path.join(event.path, event.name), datetime.datetime.now()))


    def process_IN_CREATE(self, event):
        print "CREATE event:", event.pathname
        logging.info("CREATE event : %s  %s" % (os.path.join(event.path, event.name), datetime.datetime.now()))


    def process_IN_DELETE(self, event):
        print "DELETE event:", event.pathname
        logging.info("DELETE event : %s  %s" % (os.path.join(event.path, event.name), datetime.datetime.now()))

    # def process_IN_MODIFY(self, event):
    #     print "MODIFY event:", event.pathname
    #     a = traffic_watch(user_down_alert, user_up_alert, app_down_alert, app_up_alert, connect_alert)
    #     a.traffic_alert()
    #     a.nf_conntrack_count()
    #     logging.info("MODIFY event : %s  %s" % (os.path.join(event.path, event.name), datetime.datetime.now()))



    def process_IN_OPEN(self, event):
        print "OPEN event:", event.pathname
        logging.info("OPEN event : %s  %s" % (os.path.join(event.path, event.name), datetime.datetime.now()))


def main():
    # watch manager
    wm = pyinotify.WatchManager()
    # event handler
    eh = MyEventHandler()
    # notifier
    notifier = pyinotify.Notifier(wm, default_proc_fun=eh, read_freq=20)
    # Add a new watch on /tmp for ALL_EVENTS.
    wm.add_watch('/home/ankiy/log/detect_folder', pyinotify.ALL_EVENTS, rec=True)
    # Loop forever and handle events.
    notifier.loop()

if __name__ == '__main__':
    main()