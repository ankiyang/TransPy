
import pyinotify

wm = pyinotify.WatchManager()

mask = pyinotify.IN_DELETE|IN_CREATE

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        print "Creating:",event.pathname
    def process_IN_DELETE(self,event):
        print "Removing:",event.pathname

notifier = pyinotify.ThreadedNotifier(wm, EventHandler())
notifier.start()

wdd = wm.add_watch('/tmp', mask, rec=True)
wm.rm_watch(wdd.values())

notifier.stop()