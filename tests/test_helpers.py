
def assert_raises(exc_cls, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except Exception, exc:
        assert isinstance(exc, exc_cls), \
               'raised {!r}, not {}'.format(exc, exc_cls)
    else:
        mesg = 'no exception, expected {}'.format(exc_cls)
        raise AssertionError, mesg

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
