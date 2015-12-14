#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import modf
from os import remove, walk
from os.path import join


def clean_repo(directory):
    """
    Remove *.pyc files in directory
    """
    filepaths = []

    for dirpath, dirnames, filenames in walk(directory):
        filepaths.extend([join(dirpath, filename).decode('utf-8') for filename
                         in filenames if filename.endswith('.pyc')])

    map(remove, filepaths)

    print 'repository cleaned'


def format_length(length):
    """
    Return formatted length.
    """
    length = int(modf(length)[1])

    if length < 3600:
        minutes = length / 60
        seconds = length % 60

        return '%s:%s' % (format(minutes, '02'), format(seconds, '02'))
    else:
        hours = length / 3600
        minutes = (length % 3600) / 60
        seconds = (length % 3600) % 60

        return '%d:%s:%s' % (hours, format(minutes, '02'), format(seconds, '02'))
