# -*- coding: utf-8 -*-

import getpass
import os

# directories
BASE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)))
LOG_DIR = os.path.join(BASE_DIR, 'log')
MUSIC_DIR = '/home/{}/Music'.format(getpass.getuser())

# default arguments
MAX_TRACKLIST_LENGTH = 60
MAX_TRACK_LENGTH = 10
MIN_TRACK_LENGTH = 0
PLAYER = 'vlc'
SORTING = 'random'

# player settings
OVERLAP_LENGTH = 3

# mongo settings
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DBNAME = 'rolabesti'
MONGO_COLNAME = 'tracks'
