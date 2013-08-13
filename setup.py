from distutils.core import setup

with open('version.txt') as f:
    version = f.read().strip()

url = 'https://github.com/nejstastnejsistene/cron.py'

classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Natural Language :: English',
    'Operating System :: POSIX',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: Implementation :: CPython',
    'Topic :: Utilities',
    ]

setup(
    name = 'cron.py',
    packages = ['cron'],
    version = version,
    description = 'The cron daemon, in Python.',
    author = 'Peter Johnson',
    author_email = 'pajohnson@email.wm.edu',
    url = url,
    download_url = url + '/releases',
    keywords = [],
    classifiers = classifiers,
    long_description = '''\
This is a WIP' it is being developed concurrently with another
project that is using it.
'''
    )
