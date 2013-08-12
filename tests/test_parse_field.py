from cron import tab
from test_helpers import assert_raises


def assert_bits_match(bits, expected):
    # Assert all the expected are true.
    assert all(map(bits.__getitem__, expected)), bits
    # Use a copy so the original bits can be in the assert message.
    b = bits[::]
    # Pop in reverse to avoid confusing indices.
    map(b.pop, sorted(expected, reverse=True))
    # Assert none of the others are true.
    assert not any(b), bits


def test_asserts_bits_match():
    assert_bits_match([True, False, True, False], [0, 2])
    assert_raises(AssertionError,
            assert_bits_match, [True, False, True, False], [0, 1])

def test_single_minute_field():
    bits = tab.parse_field('0', tab.MINUTE)
    assert_bits_match(bits, [0])
    bits = tab.parse_field('5', tab.MINUTE)
    assert_bits_match(bits, [5])
    bits = tab.parse_field('59', tab.MINUTE)
    assert_bits_match(bits, [59])

def test_single_out_of_range_minute_field():
    assert_raises(ValueError, tab.parse_field, '60', tab.MINUTE)

def test_single_hour_field():
    bits = tab.parse_field('0', tab.HOUR)
    assert_bits_match(bits, [0])
    bits = tab.parse_field('16', tab.HOUR)
    assert_bits_match(bits, [16])
    bits = tab.parse_field('23', tab.HOUR)
    assert_bits_match(bits, [23])
    
def test_single_dom_field():
    bits = tab.parse_field('1', tab.DOM)
    assert_bits_match(bits, [0])
    bits = tab.parse_field('12', tab.DOM)
    assert_bits_match(bits, [11])
    bits = tab.parse_field('31', tab.DOM)
    assert_bits_match(bits, [30])

def test_single_month_field():
    bits = tab.parse_field('1', tab.MONTH)
    assert_bits_match(bits, [0])
    bits = tab.parse_field('apr', tab.MONTH)
    assert_bits_match(bits, [3])
    bits = tab.parse_field('12', tab.MONTH)
    assert_bits_match(bits, [11])

def test_single_dow_field():
    # Either Sunday toggles both.
    bits = tab.parse_field('0', tab.DOW)
    assert_bits_match(bits, [0, 7])
    bits = tab.parse_field('wed', tab.DOW)
    assert_bits_match(bits, [3])
    bits = tab.parse_field('5', tab.DOW)
    assert_bits_match(bits, [5])
    bits = tab.parse_field('7', tab.DOW)
    assert_bits_match(bits, [0, 7])

def test_ranged_minute_field():
    bits = tab.parse_field('0-59', tab.MINUTE)
    assert_bits_match(bits, range(60))
    bits = tab.parse_field('0-59/5', tab.MINUTE)
    assert_bits_match(bits, range(0, 60, 5))
    bits = tab.parse_field('6-37', tab.MINUTE)
    assert_bits_match(bits, range(6, 38))
    bits = tab.parse_field('6-37/3', tab.MINUTE)
    assert_bits_match(bits, range(6, 37, 3))
    bits = tab.parse_field('*', tab.MINUTE)
    assert_bits_match(bits, range(60))
    bits = tab.parse_field('*/1', tab.MINUTE)
    assert_bits_match(bits, range(60))
    bits = tab.parse_field('*/17', tab.MINUTE)
    assert_bits_match(bits, range(0, 60, 17))

def test_ranged_hour_field():
    bits = tab.parse_field('0-23', tab.HOUR)
    assert_bits_match(bits, range(24))
    bits = tab.parse_field('0-23/5', tab.HOUR)
    assert_bits_match(bits, range(0, 24, 5))
    bits = tab.parse_field('6-18', tab.HOUR)
    assert_bits_match(bits, range(6, 19))
    bits = tab.parse_field('6-18/3', tab.HOUR)
    assert_bits_match(bits, range(6, 19, 3))
    bits = tab.parse_field('*', tab.HOUR)
    assert_bits_match(bits, range(24))
    bits = tab.parse_field('*/17', tab.HOUR)
    assert_bits_match(bits, range(0, 24, 17))

def test_ranged_month_field():
    bits = tab.parse_field('0-23', tab.HOUR)
    assert_bits_match(bits, range(24))
    bits = tab.parse_field('0-23/5', tab.HOUR)
    assert_bits_match(bits, range(0, 24, 5))
    bits = tab.parse_field('6-18', tab.HOUR)
    assert_bits_match(bits, range(6, 19))
    bits = tab.parse_field('6-18/3', tab.HOUR)
    assert_bits_match(bits, range(6, 19, 3))
    bits = tab.parse_field('*', tab.HOUR)
    assert_bits_match(bits, range(24))
    bits = tab.parse_field('*/17', tab.HOUR)
    assert_bits_match(bits, range(0, 24, 17))

def test_ranged_dom_field():
    bits = tab.parse_field('1-31', tab.DOM)
    assert_bits_match(bits, range(31))
    bits = tab.parse_field('1-31/5', tab.DOM)
    assert_bits_match(bits, range(0, 31, 5))
    bits = tab.parse_field('6-26', tab.DOM)
    assert_bits_match(bits, range(5, 26))
    bits = tab.parse_field('6-26/4', tab.DOM)
    assert_bits_match(bits, range(5, 26, 4))
    bits = tab.parse_field('*', tab.DOM)
    assert_bits_match(bits, range(31))
    bits = tab.parse_field('*/5', tab.DOM)
    assert_bits_match(bits, range(0, 31, 5))

def test_ranged_month_field():
    bits = tab.parse_field('1-12', tab.MONTH)
    assert_bits_match(bits, range(12))
    bits = tab.parse_field('1-12/5', tab.MONTH)
    assert_bits_match(bits, range(0, 12, 5))
    bits = tab.parse_field('6-9', tab.MONTH)
    assert_bits_match(bits, range(5, 9))
    bits = tab.parse_field('6-9/3', tab.MONTH)
    assert_bits_match(bits, range(5, 9, 3))
    bits = tab.parse_field('*', tab.MONTH)
    assert_bits_match(bits, range(12))
    bits = tab.parse_field('*/5', tab.MONTH)
    assert_bits_match(bits, range(0, 12, 5))

def test_ranged_month_field():
    # Either Sunday toggles both.
    bits = tab.parse_field('0-7', tab.DOW)
    assert_bits_match(bits, range(8))
    bits = tab.parse_field('0-7/3', tab.DOW)
    assert_bits_match(bits, range(0, 8, 3) + [7])
    bits = tab.parse_field('2-5', tab.DOW)
    assert_bits_match(bits, range(2, 6))
    bits = tab.parse_field('1-6/2', tab.DOW)
    assert_bits_match(bits, range(1, 7, 2))
    bits = tab.parse_field('*', tab.DOW)
    assert_bits_match(bits, range(8))
    bits = tab.parse_field('*/3', tab.DOW)
    assert_bits_match(bits, range(0, 8, 3) + [7])

def test_commas_in_fields():
    bits = tab.parse_field('0,1,2', tab.MINUTE)
    assert_bits_match(bits, range(3))
    bits = tab.parse_field('0-10,20-30', tab.MINUTE)
    assert_bits_match(bits, range(11) + range(20, 31))
    bits = tab.parse_field('0-10,20-30,40-50/3', tab.MINUTE)
    assert_bits_match(bits, range(11) + range(20, 31) + range(40, 51, 3))

def test_out_of_range_errors():
    assert_raises(ValueError, tab.parse_field, '60', tab.MINUTE)
    assert_raises(ValueError, tab.parse_field, '0-60', tab.MINUTE)
    assert_raises(ValueError, tab.parse_field, '24', tab.HOUR)
    assert_raises(ValueError, tab.parse_field, '0-24', tab.HOUR)
    assert_raises(ValueError, tab.parse_field, '0', tab.DOM)
    assert_raises(ValueError, tab.parse_field, '32', tab.DOM)
    assert_raises(ValueError, tab.parse_field, '0-31', tab.DOM)
    assert_raises(ValueError, tab.parse_field, '1-32', tab.DOM)
    assert_raises(ValueError, tab.parse_field, '0', tab.MONTH)
    assert_raises(ValueError, tab.parse_field, '13', tab.MONTH)
    assert_raises(ValueError, tab.parse_field, 'jan-13', tab.MONTH)
    assert_raises(ValueError, tab.parse_field, '0-dec', tab.MONTH)
    assert_raises(ValueError, tab.parse_field, '8', tab.DOW)
    assert_raises(ValueError, tab.parse_field, 'sun-8', tab.DOW)
    # Enforce start < stop.
    assert_raises(ValueError, tab.parse_field, '1-1', tab.MINUTE)
    # However it's okay to do it with sunday to sunday.
    tab.parse_field('7-0', tab.DOW)
    tab.parse_field('sun-sun', tab.DOW)

def test_badly_formatted_fields():
    assert_raises(ValueError, tab.parse_field, '', tab.MINUTE)
    assert_raises(ValueError, tab.parse_field, '0-', tab.MINUTE)
    assert_raises(ValueError, tab.parse_field, '-59', tab.MINUTE)
    assert_raises(ValueError, tab.parse_field, '*/', tab.MINUTE)
    assert_raises(ValueError, tab.parse_field, '/2', tab.MINUTE)
    assert_raises(ValueError, tab.parse_field, '1,', tab.MINUTE)
    assert_raises(ValueError, tab.parse_field, ',1', tab.MINUTE)
    assert_raises(ValueError, tab.parse_field, '1,,1', tab.MINUTE)
