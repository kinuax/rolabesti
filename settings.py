#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

BASE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)))

# directories
DB_DIR = os.path.join(BASE_DIR, 'database')
LOG_DIR = os.path.join(BASE_DIR, 'log')
MODULES_DIR = os.path.join(BASE_DIR, 'modules')
MUSIC_DIR = '/path/to/music/directory'

# default search
SORTING = 'random'
TOTAL_LENGTH = 60
MIN_TRACK_LENGTH = 0
MAX_TRACK_LENGTH = TOTAL_LENGTH
