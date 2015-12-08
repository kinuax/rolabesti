#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import json
from os import walk
from os.path import basename, join, splitext
import re
import sys

from mutagen.mp3 import MP3

from modules.logger import get_logger
from settings import DB_DIR, MUSIC_DIR

LOG_NAME = splitext(basename(__file__))[0]
PARSINGS = (
    (r'/Places/(.+?)/Genres/(.+?)/Albums/(.+?)/(.+/)*(.+)\.mp3$', ('place', 'genre', 'album', 'other', 'filename')),
    (r'/Places/(.+?)/Genres/(.+?)/(.+?)/(.+?)/(.+/)*(.+)\.mp3$', ('place', 'genre', 'artist', 'album', 'other', 'filename')),
    (r'/Places/(.+?)/Genres/(.+?)/(.+?)/(.+)\.mp3$', ('place', 'genre', 'artist', 'filename')),
    (r'/Places/(.+?)/Albums/(.+?)/(.+/)*(.+)\.mp3$', ('place', 'album', 'other', 'filename')),
    (r'/Places/(.+?)/(.+?)/(.+?)/(.+/)*(.+)\.mp3$', ('place', 'artist', 'album', 'other', 'filename')),
    (r'/Places/(.+?)/(.+?)/(.+)\.mp3$', ('place', 'artist', 'filename')),
    (r'/Genres/(.+?)/Albums/(.+?)/(.+/)*(.+)\.mp3$', ('genre', 'album', 'other', 'filename')),
    (r'/Genres/(.+?)/(.+?)/(.+?)/(.+/)*(.+)\.mp3$', ('genre', 'artist', 'album', 'other', 'filename')),
    (r'/Genres/(.+?)/(.+?)/(.+)\.mp3$', ('genre', 'artist', 'filename')),
)
COUNTS = (50, 100, 500, 1000, 2000, 5000, 10000, 15000, 20000, 25000, 30000, 40000, 50000)


def build_index():
    """
    Build the database index
    """
    places = []
    genres = []
    artists = []
    albums = []
    tracks = []
    count = 0

    logger = get_logger(LOG_NAME)
    info = 'building new database index'
    logger.info(info)

    print info

    for dirpath, dirnames, filenames in walk(MUSIC_DIR):
        if 'Places' in dirpath or 'Genres' in dirpath:
            trackpaths = [join(dirpath, filename).decode('utf-8')
                          for filename in filenames if filename.endswith('.mp3')]

            for trackpath in trackpaths:
                track = build_track(trackpath)

                if track:
                    tracks.append(track)
                    count += 1

                    if 'genre' in track and track['genre'] not in genres:
                        genres.append(track['genre'])

                    if 'place' in track and track['place'] not in places:
                        places.append(track['place'])

                    if 'artist' in track and track['artist'] not in artists:
                        artists.append(track['artist'])

                    if 'album' in track and track['album'] not in albums:
                        albums.append(track['album'])

                    info = u'track indexed : %s' % track['path']
                    logger.info(info)

                    if count in COUNTS:
                        print '%d tracks indexed' % count

    dump_to_json(sorted(places), join(DB_DIR, 'places.json'))
    dump_to_json(sorted(genres), join(DB_DIR, 'genres.json'))
    dump_to_json(sorted(artists), join(DB_DIR, 'artists.json'))
    dump_to_json(sorted(albums), join(DB_DIR, 'albums.json'))
    dump_to_json(tracks, join(DB_DIR, 'tracks.json'))

    info = 'database index built : %d tracks indexed' % count
    logger.info(info)

    print info


def build_track(trackpath):
    """
    Build the track index
    """
    logger = get_logger(LOG_NAME)

    # get track parsing
    for parsing in PARSINGS:
        match = re.search(parsing[0], trackpath)

        if match:
            track = {'path': trackpath}
            values = match.groups()

            for i, field in enumerate(parsing[1]):
                if field != 'other':
                    track[field] = values[i]

            break

    if not match:
        warning = u'track parsing not found : %s' % trackpath
        logger.warning(warning)

        return {}

    # get track length
    try:
        audio = MP3(trackpath)
        track['length'] = audio.info.length
    except:
        error = sys.exc_info()
        error = u'getting track length : %s - %s : %s' % \
            (str(error[0]), str(error[1]), trackpath)
        logger.error(error)

        return {}

    return track


def get_tracks():
    """
    Return a list with the indexed tracks
    """
    return load_from_json(join(DB_DIR, 'tracks.json'))


def dump_to_json(obj, filepath):
    with codecs.open(filepath, 'w', 'utf-8') as file:
        json.dump(obj, file, ensure_ascii=False, indent=4, sort_keys=True)


def load_from_json(filepath):
    with open(filepath) as file:
        obj = json.load(file)

    return obj
