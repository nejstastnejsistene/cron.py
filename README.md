cron.py
=======

The cron daemon, in Python.

## Installation

To install from PyPI:

    pip install cron.py

Or, if you prefer to build install from source:

    git clone git@github.com:nejstastnejsistene/cron.py.git
    cd cron.py
    python setup.py install

## Basic usage

```python
import cron

def foo(x, y, z):
    '''Called once every half hour.'''

daemon = cron.Cron()
daemon.add('@weekly shell_command')
daemon.add('*/30 * * * *', foo, 1, 2, 3)
daemon.start()

# The next few times these command will run.
for entry in daemon.entries:
    for _, dt in zip(range(3), entry):
        print dt.strftime('%c'), entry.command
# Sun Aug 18 00:00:00 2013 shell_command
# Sun Aug 25 00:00:00 2013 shell_command
# Sun Sep  1 00:00:00 2013 shell_command
# Tue Aug 13 21:00:00 2013 (<function foo at 0x7f24e0201b90>, (1, 2, 3), {})
# Tue Aug 13 21:30:00 2013 (<function foo at 0x7f24e0201b90>, (1, 2, 3), {})
# Tue Aug 13 22:00:00 2013 (<function foo at 0x7f24e0201b90>, (1, 2, 3), {})
```
