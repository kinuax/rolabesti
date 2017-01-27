# -*- coding: utf-8 -*-

from os import walk
from os.path import exists, join
import re
import sys

from pymongo import MongoClient

from parser import parse
from settings import MUSIC_DIR, MONGO_HOST, MONGO_PORT, MONGO_DBNAME, MONGO_COLNAME
from utils import get_length, get_logger, get_tag

COUNTS = (5, 10, 50, 100, 500, 1000, 2000, 5000, 10000, 15000, 20000, 25000, 30000, 40000, 50000)
SEARCH_FIELDS = ('artist', 'album', 'genre', 'place')


def get_collection():
    client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)

    return client[MONGO_DBNAME][MONGO_COLNAME]


def load():
    """Load the collection with parsed mp3 files."""
    collection = get_collection()
    collection.remove({})
    count = 0

    logger = get_logger(__file__)
    info = 'loading new database from scratch'
    logger.info(info)
    print('[mongo]', info)

    for dirpath, dirnames, filenames in walk(MUSIC_DIR):
        for filename in filenames:
            if filename.lower().endswith('.mp3'):
                trackpath = join(dirpath, filename)
                track = parse(trackpath)

                if track:
                    try:
                        track['length'] = get_length(trackpath)
                    except:
                        error = sys.exc_info()
                        error = 'getting track length | %s - %s | %s' % (str(error[0]), str(error[1]), trackpath)
                        logger.error(error)

                        continue

                    track['title'] = get_tag(trackpath, 'title')
                    collection.insert_one(track)
                    count += 1

                    if count in COUNTS:
                        print('[mongo] loading %d tracks' % count)

    info = 'new database loaded : %d tracks loaded' % count
    logger.info(info)
    print('[mongo]', info)


def filtered_by_fields(track, fields):
    for field, value in fields.items():
        if field not in track or value.lower() not in track[field].lower():
            return False

    return True


def search(arguments):
    tracks = []
    logger = get_logger(__file__)
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


def is_database_empty():
    """Return True is there is at least one track in the collection. Otherwise, return False."""
    return not get_collection().find().count()
