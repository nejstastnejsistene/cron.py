cron.py
=======

The cron daemon, in Python.

## Installation

To install from PyPI:

    pip install cron.py

Or, if you prefer to build from source:

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
daemon.add('*/30 * * * *', foo, 1, 2, z=3)
daemon.start()
```
