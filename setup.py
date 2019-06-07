#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup for the Safecast Tracker.

Source:: https://github.com/ampledata/safehook
"""


__title__ = 'safehook'
__version__ = '1.0.0b1'
__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2019 Greg Albrecht'


import os
import sys

import setuptools


def publish():
    """Function for publishing package to pypi."""
    if sys.argv[-1] == 'publish':
        os.system('python setup.py sdist upload')
        sys.exit()


publish()


setup(
    name='safehook',
    version=__version__,
    description='Safecast Tracker for APRS.',
    author='Greg Albrecht',
    author_email='oss@undef.net',
    packages=['safehook'],
    package_data={'': ['LICENSE']},
    license=open('LICENSE').read(),
    long_description=open('README.rst').read(),
    url='https://github.com/ampledata/safehook',
    setup_requires=[
      'coverage >= 3.7.1',
      'nose >= 1.3.7'
    ],
    install_requires=[
        'pygatt',
        'pynmea2 >= 1.4.2',
        'pyserial >= 2.7',
        'requests'
    ],
    package_dir={'safehook': 'safehook'},
    zip_safe=False,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'safehook = safehook.cmd:sc_tracker'
        ],
    }
)
