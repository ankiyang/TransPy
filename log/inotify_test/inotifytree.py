#!/usr/bin/env python
# -*-coding:utf-8-*-

from inotify import adapters
from inotify import constants

i_tree = adapters.InotifyTree(path='home/ankiy/log/sys_statistic.json', mask=constants.IN_ALL_EVENTS, )

for event in i_tree.event_gen():
    if event is not None:
        (header, type_names, watch_path, filename) = event
        print "WD=(%d) MASK=(%d) COOKIE=(%d) LEN=(%d) MASK->NAMES=%s WATCH-PATH=[%s] FILENAME=[%s]"\
              %(header.wd, header.mask, header.cookie, header.len, type_names, watch_path, filename)


