# -*- coding: utf-8 -*-
"""
rolabesti.conf.settings
~~~~~~~~~~~~~~~~~~~~~~~

This module contains the default rolabesti settings.
"""

import getpass

# arguments
MAX_TRACKLIST_LENGTH = 60
MAX_TRACK_LENGTH = 10
MIN_TRACK_LENGTH = 0
PLAYER = 'vlc'
SORTING = 'random'

# mongo module
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DBNAME = 'rolabesti'
MONGO_COLNAME = 'tracks'
MUSIC_DIR = '/home/{}/Music'.format(getpass.getuser())

# player module
OVERLAP_LENGTH = 3
