#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

import rolabesti


def long_description():
    with open('README.rst', encoding='utf-8') as f:
        return f.read()


setup(
    name='rolabesti',
    version=rolabesti.__version__,
    description=rolabesti.__description__,
    long_description=long_description(),
    author='Kinuax',
    author_email='kinuax@gmail.com',
    url='https://github.com/kinuax/rolabesti/',
    download_url='https://github.com/kinuax/rolabesti/',
    license='GPLv2',
    keywords='mp3 id3 vlc mongo',
    zip_safe=False,
    packages=['rolabesti', 'rolabesti.conf'],
    install_requires=['mutagen==1.31', 'pymongo==3.2.1', 'python-vlc==1.1.2'],
    entry_points={'console_scripts': ['rolabesti = rolabesti.__main__:main']},
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Multimedia',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Multimedia :: Sound/Audio :: Players',
        'Topic :: Multimedia :: Sound/Audio :: Players :: MP3',
    ],
)
