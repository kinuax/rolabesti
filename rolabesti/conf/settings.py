# -*- coding: utf-8 -*-
"""
rolabesti.conf.settings
~~~~~~~~~~~~~~~~~~~~~~~

This module contains the default rolabesti settings. These settings can be overriden
by the user at the ~/.config/rolabesti/rolabesti.conf file.
"""

import configparser
import getpass
from os.path import exists
import sys

# mongo module
MAX_TRACK_LENGTH = 10
MIN_TRACK_LENGTH = 0
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DBNAME = 'rolabesti'
MONGO_COLNAME = 'tracks'
MUSIC_DIR = '/home/{}/Music'.format(getpass.getuser())

# player module
PLAYER = 'vlc'
OVERLAP_LENGTH = 3

# slicer module
MAX_TRACKLIST_LENGTH = 60

# sorter module
SORTING = 'random'

# Override settings
conf_file = '/home/{}/.config/rolabesti/rolabesti.conf'.format(getpass.getuser())

if exists(conf_file):
    SETTINGS = ('MAX_TRACK_LENGTH', 'MIN_TRACK_LENGTH', 'MONGO_HOST', 'MONGO_PORT', 'MONGO_DBNAME', 'MONGO_COLNAME', 'MUSIC_DIR',
                'PLAYER', 'OVERLAP_LENGTH', 'MAX_TRACKLIST_LENGTH', 'SORTING')
    config = configparser.ConfigParser()
    config.read(conf_file)

    for setting, value in config.items('rolabesti'):
        if setting.upper() in SETTINGS:
            try:
                setattr(sys.modules[__name__], setting.upper(), int(value))
            except ValueError:
                setattr(sys.modules[__name__], setting.upper(), value)
