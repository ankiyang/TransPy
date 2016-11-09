# Example: loops monitoring events forever.
#
import pyinotify

# Instanciate a new WatchManager (will be used to store watches).
wm = pyinotify.WatchManager()
# Associate this WatchManager with a Notifier (will be used to report and
# process events).
notifier = pyinotify.Notifier(wm)
# Add a new watch on /tmp for ALL_EVENTS.
wm.add_watch('/home/ankiy/log/detect_folder/sys_statistic.json', pyinotify.ALL_EVENTS,
             rec=True, do_glob=True, auto_add=True)
# Loop forever and handle events.
notifier.loop()

