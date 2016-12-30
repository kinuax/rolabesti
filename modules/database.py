#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import walk
from os.path import basename, exists, join, splitext
import re
import sys

from mutagen.mp3 import MP3
from pymongo import MongoClient

from .logger import get_logger
from settings import MUSIC_DIR, MONGO_HOST, MONGO_PORT, MONGO_DBNAME, MONGO_COLNAME

LOG_NAME = splitext(basename(__file__))[0]
PARSINGS = (
    (r'/Places/(.+?)/Genres/(.+?)/Albums/(.+?)/(.+/)*(.+)\.[mM][pP]3$', ('place', 'genre', 'album', 'side', 'filename')),
    (r'/Places/(.+?)/Genres/(.+?)/(.+?)/(.+?)/(.+/)*(.+)\.[mM][pP]3$', ('place', 'genre', 'artist', 'album', 'side', 'filename')),
    (r'/Places/(.+?)/Genres/(.+?)/(.+?)/(.+)\.[mM][pP]3$', ('place', 'genre', 'artist', 'filename')),
    (r'/Places/(.+?)/Albums/(.+?)/(.+/)*(.+)\.[mM][pP]3$', ('place', 'album', 'side', 'filename')),
    (r'/Places/(.+?)/(.+?)/(.+?)/(.+/)*(.+)\.[mM][pP]3$', ('place', 'artist', 'album', 'side', 'filename')),
    (r'/Places/(.+?)/(.+?)/(.+)\.[mM][pP]3$', ('place', 'artist', 'filename')),
    (r'/Genres/(.+?)/Albums/(.+?)/(.+/)*(.+)\.[mM][pP]3$', ('genre', 'album', 'side', 'filename')),
    (r'/Genres/(.+?)/(.+?)/(.+?)/(.+/)*(.+)\.[mM][pP]3$', ('genre', 'artist', 'album', 'side', 'filename')),
    (r'/Genres/(.+?)/(.+?)/(.+)\.[mM][pP]3$', ('genre', 'artist', 'filename')),
)
COUNTS = (5, 10, 50, 100, 500, 1000, 2000, 5000, 10000, 15000, 20000, 25000, 30000, 40000, 50000)
SEARCH_FIELDS = ('artist', 'album', 'genre', 'place')


def get_collection():
    client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)

    return client[MONGO_DBNAME][MONGO_COLNAME]


def build():
    """
    Parse mp3 files under MUSIC_DIR and build the collection
    """
    collection = get_collection()
    collection.remove({})
    count = 0

    logger = get_logger(LOG_NAME)
    info = 'building new database'
    logger.info(info)
    print('[mongo]', info)

    for dirpath, dirnames, filenames in walk(MUSIC_DIR):
        if re.search(r'/Places/|/Genres/', dirpath):
            trackpaths = [join(dirpath, filename) for filename in filenames if re.search(r'\.[mM][pP]3$', filename)]

            for trackpath in trackpaths:
                track = parse(trackpath)

                if track:
                    try:
                        track['length'] = get_length(trackpath)
                    except:
                        error = sys.exc_info()
                        error = 'getting track length | %s - %s | %s' % \
                            (str(error[0]), str(error[1]), trackpath)
                        logger.error(error)

                        continue

                    collection.insert_one(track)
                    count += 1

                    if count in COUNTS:
                        print('[mongo] loading %d tracks' % count)

                else:
                    warning = 'track parsing not found | %s' % trackpath
                    logger.warning(warning)

    info = 'new database built : %d tracks loaded' % count
    logger.info(info)
    print('[mongo]', info)


def parse(trackpath):
    for parsing in PARSINGS:
        match = re.search(parsing[0], trackpath)

        if match:
            track = {'path': trackpath}
            values = match.groups()

            for i, field in enumerate(parsing[1]):
                if field != 'side':
                    track[field] = values[i]

            return track


def get_length(trackpath):
    audio = MP3(trackpath)

    return audio.info.length


def filtered_by_fields(track, fields):
    for field, value in fields.items():
        if field not in track or value.lower() not in track[field].lower():
            return False

    return True


def search(arguments):
    tracks = []
    logger = get_logger(LOG_NAME)
    collection = get_collection()
    query = {'length': {'$gte': arguments['min'], '$lte': arguments['max']}}
    query.update({field: re.compile(value, re.IGNORECASE)
                 for field, value in arguments.items() if field in SEARCH_FIELDS})

    print('[mongo] searching tracks')

    for track in collection.find(query):
        if exists(track['path']):
            tracks.append(track)
        else:
            warning = 'loaded track does not exist in file system | %s' % track['path']
            logger.warning(warning)

    if tracks:
        print('[mongo] %s track%s found' % (len(tracks), 's'[len(tracks) == 1:]))
    else:
        print('[mongo] no track found')

    return tracks


def check_existing_tracks():
    """
    Exit with message if there is no track in the collection
    """
    collection = get_collection()

    if not collection.find().count():
        error = '[mongo] there is no track loaded in the database'
        error += ' | run build method to load tracks'
        sys.exit(error)
