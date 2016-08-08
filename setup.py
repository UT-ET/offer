#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of offer.
# https://github.com/musically-ut/offer

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Utkarsh Upadhyay <musically.ut@gmail.com>

from setuptools import setup, find_packages
from offer import __version__
import io
from os.path import dirname
from os.path import join

tests_require = [
    'mock',
    'nose',
    'coverage',
    'yanc',
    'preggy',
    'tox',
    'ipdb',
    'coveralls',
    'sphinx',
]


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


setup(
    name='offer',
    version=__version__,
    description='Quickly host files for local transfer.',
    long_description=read('README.rst'),
    keywords='host,network,local',
    author='Utkarsh Upadhyay',
    author_email='musically.ut@gmail.com',
    url='https://github.com/musically-ut/offer',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=False,
    install_requires=[
        # add your dependencies here
        # remember to use 'package-name>=x.y.z,<x.y+1.0' notation
        # (this way you get bugfixes)
        "netifaces>=0.10.4,<0.11.0"
    ],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
            'offer=offer.offerCLI:main'
        ],
    },
    zip_safe=True
)
