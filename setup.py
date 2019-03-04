#!/usr/bin/env python3

from setuptools import setup

setup(name='alexdns',
  version='0.1',
  description='local dns resolver',
  author='Alex Couture-Beil',
  url='https://github.com/alexcb/alexdns',
  packages=[
      'alexdns',
      'alexdns/common',
      'alexdns/handlers',
      ],
  install_requires=[
    'dnslib',
    'dnspython',
    ],
 )
