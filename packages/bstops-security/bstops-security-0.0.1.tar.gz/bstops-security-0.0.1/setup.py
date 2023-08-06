#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = 'bstops-security',
    version = '0.0.1',
    keywords = ['pip', 'bstops', 'security'],
    description = 'Security package',
    license = 'MIT Licence',

    url = 'https://github.com/viger1228/bstops-security',
    author = 'walker',
    author_email = 'walkerIVI@gmail.com',

    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = [
        'bstops-tool',
    ]
)
