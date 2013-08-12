from cron import tab

def test_iter_field():
    entry = tab.parse_entry('* * * * * cmd')
    assert list(entry.iter_field(tab.MINUTE)) == range(60)
    assert list(entry.iter_field(tab.HOUR))   == range(24)
    assert list(entry.iter_field(tab.DOM))    == range(1, 32)
    assert list(entry.iter_field(tab.MONTH))  == range(1, 13)
    assert list(entry.iter_field(tab.DOW))    == range(8)
    entry = tab.parse_entry('*/17 4-9 2-27/8 MAY-AUG MON-FRI cmd')
    assert list(entry.iter_field(tab.MINUTE)) == range(0, 60, 17)
    assert list(entry.iter_field(tab.HOUR))   == range(4, 10)
    assert list(entry.iter_field(tab.DOM))    == range(2, 28, 8)
    assert list(entry.iter_field(tab.MONTH))  == range(5, 9)
    assert list(entry.iter_field(tab.DOW))    == range(1, 6)
