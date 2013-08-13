import cron
import threading
import time


def test_cron_stop():
    print('This test might take a few seconds.')
    daemon = cron.Cron()
    daemon.start()
    daemon.stop()
    assert not daemon.thread.isAlive()

def test_cron_daemon():
    print('This test might take up to a minute.')
    dct = {}
    def cmd():
        dct['it works!'] = True
    daemon = cron.Cron()
    daemon.add('* * * * *', cmd)
    daemon.start()
    for i in range(60):
        time.sleep(1)
        if 'it works!' in dct:
            break
    assert dct.get('it works!', False)
    daemon.stop()

