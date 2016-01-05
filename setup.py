#!/usr/bin/env python

from setuptools import setup
from goear_dl import __version__

setup(
    name='goear_dl',
    version=__version__,
    description='download songs from goear',
    author='Joan Font',
    license='GPLv2',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Environment :: Console',
        'Topic :: Multimedia :: Sound/Audio',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Topic :: Terminals',
        'Topic :: System :: Shells',
        'Topic :: Utilities'
    ],
    keywords='goear download music',
    author_email='joanfont@gmail.com',
    url='https://github.com/joanfont/goear-dl',
    download_url='https://github.com/joanfont/goear-dl',

    packages=['goear_dl'],
    install_requires=[
        'requests==2.9.1',
        'beautifulsoup4==4.4.1',
        'six==1.10.0',
    ],
    entry_points={
        'console_scripts': [
            'goear-dl = goear_dl.main:main'
        ],
    }
)
