#!/usr/bin/env python
from setuptools import setup, find_packages
import os
import sys

if sys.version_info < (3, 3):
    raise RuntimeError("BlackGecko requires Python 3.3+")


# Find __version__ without import that requires dependencies to be installed:
exec(open(os.path.join(
    os.path.dirname(__file__), 'BlackGecko/version.py'
)).read())

deps = ['hangups==0.3.6', 'BlackGecko']

setup(
    name='BlackGecko',
    version=__version__,
    url='https://github.com/jorgehortelano/BlackGecko',
    author='Jorge Hortelano',
    author_email='softwaremagico@gmail.com',
    license='GNU GPL v3',
    tests_require=[],
    #scripts = ['blackgecko-cli'],
    install_requires = deps,
    dependency_links = [
        'https://github.com/tdryer/hangups',
    ],
    packages= find_packages(),
    include_package_data=True,
    platforms='any',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],
)
