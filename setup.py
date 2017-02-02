#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

from setuptools import setup


def get_from_package(var):
    """Return the value of __var__ in __init__.py. If __var__ is not defined, raise RuntimeError."""
    with open('rolabesti/__init__.py') as f:
        match = re.search(r'^__{}__\s*=\s*[\'"]([^\'"]*)[\'"]'.format(var), f.read(), re.MULTILINE)

    if match:
        return match.group(1)
    else:
        raise RuntimeError('{} is missing'.format(var))


version = get_from_package('version')
description = get_from_package('description')

with open('README.rst') as f:
    readme = f.read()

setup(
    name='rolabesti',
    version=version,
    description=description,
    long_description=readme,
    author='Kinuax',
    author_email='kinuax@gmail.com',
    url='https://github.com/kinuax/rolabesti/',
    packages=['rolabesti'],
    install_requires=['mutagen==1.31', 'pymongo==3.2.1', 'python-vlc==1.1.2'],
    entry_points={'console_scripts': ['rolabesti = rolabesti.__main__:main']},
    zip_safe=False,
    license='GPLv2',
    keywords='mp3 mutagen vlc',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Multimedia',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Multimedia :: Sound/Audio :: Players',
        'Topic :: Multimedia :: Sound/Audio :: Players :: MP3',
    ],
)
