#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

BASE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)))

# directories
LOG_DIR = os.path.join(BASE_DIR, 'log')
MUSIC_DIR = '/path/to/music/directory'

# default method option
METHOD = 'play'

# default tracklist options
SORTING = 'random'
TOTAL_LENGTH = 60

# default track options
MIN_TRACK_LENGTH = 0
MAX_TRACK_LENGTH = TOTAL_LENGTH

# playing settings
PLAYING_MODE = 'shell'
OVERLAP_LENGTH = 5

# MongoDB settings
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DBNAME = 'rolabesti'
MONGO_COLNAME = 'tracks'
