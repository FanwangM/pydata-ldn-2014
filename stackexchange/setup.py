from __future__ import unicode_literals

import os

from setuptools import setup


VERSION = '0.0.1dev1'


def write_version_py(filename=None):
    if filename is None:
        filename = os.path.join(os.path.dirname(__file__),
                                'stackimport', 'version.py')
    ver = """\
version = '{version}'
"""
    fh = open(filename, 'wb')
    try:
        fh.write(ver.format(version=VERSION).encode('utf-8'))
    finally:
        fh.close()


write_version_py()


setup(
    name='stackimport',
    version=VERSION,
    url='https://github.com/enthought/pydata-ldn-2014',
    author='Simon Jagoe',
    author_email='simon@simonjagoe.com',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
    ],
    description='Postgresql importer for stackexchange data',
    packages=['stackimport'],
)
