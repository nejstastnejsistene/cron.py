from cron import tab
from test_helpers import assert_raises


def test_parse_entry_generic():
    entry = tab.parse_entry('* * * * * cmd')
    assert entry.fields[0] == [True for i in range(60)]
    assert entry.fields[1] == [True for i in range(24)]
    assert entry.fields[2] == [True for i in range(31)]
    assert entry.fields[3] == [True for i in range(12)]
    assert entry.fields[4] == [True for i in range(8)]
    assert entry.command == 'cmd'
    assert entry.dom_or_dow_star
    assert not entry.when_reboot

def test_reboot():
    entry = tab.parse_entry('@reboot cmd')
    assert entry.fields is None
    assert entry.when_reboot
    assert entry.when_reboot

def test_yearly():
    for token in ('@yearly', '@annually'):
        entry = tab.parse_entry(token + ' cmd')
        assert entry.fields[0] == [True] + [False for i in range(59)]
        assert entry.fields[1] == [True] + [False for i in range(23)]
        assert entry.fields[2] == [True] + [False for i in range(30)]
        assert entry.fields[3] == [True] + [False for i in range(11)]
        assert entry.fields[4] == [True for i in range(8)]
        assert entry.command == 'cmd'
        assert entry.dom_or_dow_star
        assert not entry.when_reboot

def test_monthly():
    entry = tab.parse_entry('@monthly cmd')
    assert entry.fields[0] == [True] + [False for i in range(59)]
    assert entry.fields[1] == [True] + [False for i in range(23)]
    assert entry.fields[2] == [True] + [False for i in range(30)]
    assert entry.fields[3] == [True for i in range(12)]
    assert entry.fields[4] == [True for i in range(8)]
    assert entry.command == 'cmd'
    assert entry.dom_or_dow_star
    assert not entry.when_reboot

def test_weekly():
    entry = tab.parse_entry('@weekly cmd')
    assert entry.fields[0] == [True] + [False for i in range(59)]
    assert entry.fields[1] == [True] + [False for i in range(23)]
    assert entry.fields[2] == [True for i in range(31)]
    assert entry.fields[3] == [True for i in range(12)]
    assert entry.fields[4] == [True] + [False for i in range(6)] + [True]
    assert entry.command == 'cmd'
    assert entry.dom_or_dow_star
    assert not entry.when_reboot

def test_daily():
    for token in ('@daily', '@midnight'):
        entry = tab.parse_entry(token + ' cmd')
        assert entry.fields[0] == [True] + [False for i in range(59)]
        assert entry.fields[1] == [True] + [False for i in range(23)]
        assert entry.fields[2] == [True for i in range(31)]
        assert entry.fields[3] == [True for i in range(12)]
        assert entry.fields[4] == [True for i in range(8)]
        assert entry.command == 'cmd'
        assert entry.dom_or_dow_star
        assert not entry.when_reboot

def test_hourly():
    entry = tab.parse_entry('@hourly cmd')
    assert entry.fields[0] == [True] + [False for i in range(59)]
    assert entry.fields[1] == [True for i in range(24)]
    assert entry.fields[2] == [True for i in range(31)]
    assert entry.fields[3] == [True for i in range(12)]
    assert entry.fields[4] == [True for i in range(8)]
    assert entry.command == 'cmd'
    assert entry.dom_or_dow_star
    assert not entry.when_reboot

def test_mistakes():
    assert_raises(tab.CronTabError, tab.parse_entry, '@hourly')
    assert_raises(tab.CronTabError, tab.parse_entry, '* * * * cmd')
