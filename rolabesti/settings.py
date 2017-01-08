#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getpass
import os

BASE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)))

# directories
LOG_DIR = os.path.join(BASE_DIR, 'log')
MUSIC_DIR = '/home/{}/Music'.format(getpass.getuser())

# default arguments
MIN_TRACK_LENGTH = 0
MAX_TRACK_LENGTH = 10
MAX_TRACKLIST_LENGTH = 60
SORTING = 'random'

# playing settings
PLAYING_MODE = 'vlc'
OVERLAP_LENGTH = 3

# MongoDB settings
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DBNAME = 'rolabesti'
MONGO_COLNAME = 'tracks'
