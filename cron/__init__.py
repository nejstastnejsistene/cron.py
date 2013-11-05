import datetime
import sys
import threading
import time

from . import tab


class Cron(object):

    def __init__(self):
        self.entries = []

    def add(self, *args):
        '''Add a cron job to be executed regularly.'''
        self.entries.append(tab.parse_entry(*args))

    def start(self):
        '''Start the main loop in a new daemon thread.'''
        self.thread = threading.Thread(target=self.main, name='cron.py')
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        '''Stop the daemon and wait for it to exit.'''
        self.stopped = True
        self.thread.join()

    def main(self):
        '''Run jobs when they are supposed to be run, until stopped.'''
        self.stopped = False

        # Run @reboot entries.
        for entry in self.entries:
            if entry.when_reboot:
                self.run_entry(entry)

        while not self.stopped:
            # Sleep until the start of the next minute.
            self.do_sleep()
            now = datetime.datetime.now()

            # Run entries if it is time for them to run.
            for entry in self.entries:
                if entry.should_run(now):
                    self.run_entry(entry)

    def run_entry(self, entry):
        '''Run a cron job in a new thread.'''
        threading.Thread(target=entry, name=entry.name()).start()

    def do_sleep(self):
        '''Sleep until the start of the next minute.'''
        now = int(time.time())
        # Round up to the start of the next minute.
        then = (now + 60) // 60 * 60 
        # Sleep in one second increments so it can exit without
        # a huge delay.
        for i in range(then - now):
            time.sleep(1)
            if self.stopped:
                sys.exit(0)
