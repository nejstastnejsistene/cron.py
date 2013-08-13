import datetime
import sys
import threading
import time

from . import tab


class Cron(object):

    def __init__(self):
        self.entries = []

    def add(self, *args):
        self.entries.append(tab.parse_entry(*args))

    def start(self):
        self.thread = threading.Thread(target=self.main, name='cron.py')
        self.thread.start()

    def stop(self):
        self.stopped = True
        self.thread.join()

    def main(self):
        self.stopped = False
        while not self.stopped:
            self.do_sleep()
            now = datetime.datetime.now()
            for entry in self.entries:
                if entry.should_run(now):
                    threading.Thread(target=entry).start()

    def do_sleep(self):
        now = int(time.time())
        # Round up to the start of the next minute.
        then = (now + 60) // 60 * 60 
        for i in range(then - now):
            time.sleep(1)
            if self.stopped:
                sys.exit(0)
