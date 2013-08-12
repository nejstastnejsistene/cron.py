from cron import tab

def test_iter_field():
    entry = tab.parse_entry('* * * * * cmd')
    assert list(entry.iter_field(tab.MINUTE)) == list(range(60))
    assert list(entry.iter_field(tab.HOUR))   == list(range(24))
    assert list(entry.iter_field(tab.DOM))    == list(range(1, 32))
    assert list(entry.iter_field(tab.MONTH))  == list(range(1, 13))
    assert list(entry.iter_field(tab.DOW))    == list(range(8))
    entry = tab.parse_entry('*/17 4-9 2-27/8 MAY-AUG MON-FRI cmd')
    assert list(entry.iter_field(tab.MINUTE)) == list(range(0, 60, 17))
    assert list(entry.iter_field(tab.HOUR))   == list(range(4, 10))
    assert list(entry.iter_field(tab.DOM))    == list(range(2, 28, 8))
    assert list(entry.iter_field(tab.MONTH))  == list(range(5, 9))
    assert list(entry.iter_field(tab.DOW))    == list(range(1, 6))
