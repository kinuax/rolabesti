# -*- coding: utf-8 -*-
"""
rolabesti.conf.settings
~~~~~~~~~~~~~~~~~~~~~~~

This module contains the default rolabesti settings. These settings can be overriden
by the user in the ~/.config/rolabesti/rolabesti.conf file.
"""

import configparser
import os
import sys

from platformdirs import user_config_path, user_data_path, user_documents_dir, user_music_dir

from rolabesti import __app_name__


# Defaults.
MAX_TRACK_LENGTH = 10
MIN_TRACK_LENGTH = 0
MAX_TRACKLIST_LENGTH = 60
SORTING = "random"
OVERLAP_LENGTH = 3
MUSIC_DIR = user_music_dir()
COPY_DIR = user_documents_dir()
DB = "tiny"

# MongoDB.
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DBNAME = "rolabesti"
MONGO_COLNAME = "tracks"

# TinyDB.
TINY_DIR = user_data_path(__app_name__)
TINY_FILE = TINY_DIR / "tracks.json"

if DB == "tiny" and not TINY_DIR.exists():
    os.mkdir(TINY_DIR)

# Override settings
conf_file = user_config_path(__app_name__) / f"{__app_name__}.conf"


if conf_file.exists():
    SETTINGS = ("MAX_TRACK_LENGTH", "MIN_TRACK_LENGTH", "MAX_TRACKLIST_LENGTH", "SORTING", "OVERLAP_LENGTH",
                "MUSIC_DIR", "COPY_DIR", "DB", "MONGO_HOST", "MONGO_PORT", "MONGO_DBNAME", "MONGO_COLNAME")
    config = configparser.ConfigParser()
    config.read(conf_file)

    for setting, value in config.items("rolabesti"):
        if setting.upper() in SETTINGS:
            try:
                value = int(value)
            except ValueError:
                pass

            setattr(sys.modules[__name__], setting.upper(), value)
