cron.py
=======

The cron daemon, in Python.

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
