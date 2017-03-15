# -*- coding: utf-8 -*-
"""
rolabesti.conf.settings
~~~~~~~~~~~~~~~~~~~~~~~

This module contains the default rolabesti settings. These settings can be overriden
by the user in the ~/.config/rolabesti/rolabesti.conf file.
"""

import configparser
from os.path import exists, expanduser
import sys

# mongo module
MAX_TRACK_LENGTH = 10
MIN_TRACK_LENGTH = 0
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DBNAME = 'rolabesti'
MONGO_COLNAME = 'tracks'
MUSIC_DIR = '{}/Music'.format(expanduser('~'))

# player module
OVERLAP_LENGTH = 3
PLAYER = 'vlc'

# slicer module
MAX_TRACKLIST_LENGTH = 60

# sorter module
SORTING = 'random'

# Override settings
conf_file = '{}/.config/rolabesti/rolabesti.conf'.format(expanduser('~'))

if exists(conf_file):
    SETTINGS = ('MAX_TRACK_LENGTH', 'MIN_TRACK_LENGTH', 'MONGO_HOST', 'MONGO_PORT', 'MONGO_DBNAME', 'MONGO_COLNAME', 'MUSIC_DIR',
                'OVERLAP_LENGTH', 'PLAYER', 'MAX_TRACKLIST_LENGTH', 'SORTING')
    config = configparser.ConfigParser()
    config.read(conf_file)

    for setting, value in config.items('rolabesti'):
        if setting.upper() in SETTINGS:
            try:
                value = int(value)
            except ValueError:
                pass

            setattr(sys.modules[__name__], setting.upper(), value)
