#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
