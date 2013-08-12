from cron import tab


def assert_raises(exc_cls, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except Exception, exc:
        assert isinstance(exc, exc_cls), \
               'raised {!r}, not {}'.format(exc, exc_cls)
    else:
        mesg = 'no exception, expected {}'.format(exc_cls)
        raise AssertionError, mesg


def assert_bits_match(bits, expected):
    # Assert all the expected are true.
    assert all(map(bits.__getitem__, expected)), bits
    # Use a copy so the original bits can be in the assert message.
    b = bits[::]
    # Pop in reverse to avoid confusing indices.
    map(b.pop, sorted(expected, reverse=True))
    # Assert none of the others are true.
    assert not any(b), bits


def test_assert_raises():
    def foo(x, y, z): pass
    def bar(x, y, z): raise ValueError
    # Raises nothing.
    try:
        assert_raises(Exception, foo, 1, 2, 3)
    except AssertionError as e:
        assert isinstance(e, AssertionError), 'expecting failed assertion'
    # Raises correct exception.
    assert_raises(ValueError, bar, 1, 2, z=3)
    # Raises incorrect exception.
    try:
        assert_raises(IOError, bar, 1, 2, 3)
    except AssertionError as e:
        assert isinstance(e, AssertionError), 'expecting failed assertion'

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

def test_single_out_of_range_hour_field():
    assert_raises(ValueError, tab.parse_field, '24', tab.HOUR)
    
def test_single_dom_field():
    bits = tab.parse_field('1', tab.DOM)
    assert_bits_match(bits, [0])
    bits = tab.parse_field('12', tab.DOM)
    assert_bits_match(bits, [11])
    bits = tab.parse_field('31', tab.DOM)
    assert_bits_match(bits, [30])

def test_single_out_of_range_dom_field():
    assert_raises(ValueError, tab.parse_field, '0', tab.DOM)
    assert_raises(ValueError, tab.parse_field, '32', tab.DOM)

def test_single_month_field():
    bits = tab.parse_field('1', tab.MONTH)
    assert_bits_match(bits, [0])
    bits = tab.parse_field('apr', tab.MONTH)
    assert_bits_match(bits, [3])
    bits = tab.parse_field('12', tab.MONTH)
    assert_bits_match(bits, [11])

def test_single_out_of_range_month_field():
    assert_raises(ValueError, tab.parse_field, '0', tab.MONTH)
    assert_raises(ValueError, tab.parse_field, '13', tab.MONTH)

def test_single_dow_field():
    bits = tab.parse_field('0', tab.DOW)
    assert_bits_match(bits, [0, 7])
    bits = tab.parse_field('wed', tab.DOW)
    assert_bits_match(bits, [3])
    bits = tab.parse_field('5', tab.DOW)
    assert_bits_match(bits, [5])
    bits = tab.parse_field('7', tab.DOW)
    assert_bits_match(bits, [0, 7])

def test_single_out_of_range_dow_field():
    assert_raises(ValueError, tab.parse_field, '8', tab.DOW)
