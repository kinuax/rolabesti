# -*- coding: utf-8 -*-

from os import walk
from os.path import exists, join
import re

from pymongo import MongoClient

from parser import parse
from settings import MUSIC_DIR, MONGO_HOST, MONGO_PORT, MONGO_DBNAME, MONGO_COLNAME
from utils import get_length, get_logger, get_tag

COUNTS = (5, 10, 50, 100, 500, 1000, 2000, 5000, 10000, 15000, 20000, 25000, 30000, 40000, 50000)
SEARCH_FIELDS = ('artist', 'album', 'genre', 'place')
logger = get_logger(__file__)


def get_collection():
    client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)

    return client[MONGO_DBNAME][MONGO_COLNAME]


def load():
    """Load the collection with parsed mp3 files."""
    collection = get_collection()
    collection.remove({})
    count = 0

    info = 'loading new database from scratch'
    logger.info(info)
    print('[mongo]', info)

    for dirpath, dirnames, filenames in walk(MUSIC_DIR):
        for filename in filenames:
            if filename.lower().endswith('.mp3'):
                trackpath = join(dirpath, filename)
                length = get_length(trackpath)

                if length:
                    track = {'path': trackpath, 'length': length}
                    track.update(parse(trackpath))
                    track['title'] = get_tag(trackpath, 'title')
                    collection.insert_one(track)
                    count += 1

                    if count in COUNTS:
                        print('[mongo] loading {} tracks'.format(count))

    info = 'new database loaded : {} tracks loaded'.format(count)
    logger.info(info)
    print('[mongo]', info)


def search(arguments):
    tracks = []
    collection = get_collection()
    query = {'length': {'$gte': arguments['min'], '$lte': arguments['max']}}
    query.update({field: re.compile(value, re.IGNORECASE)
                 for field, value in arguments.items() if field in SEARCH_FIELDS})

    print('[mongo] searching tracks')

    for track in collection.find(query):
        if exists(track['path']):
            tracks.append(track)
        else:
            warning = 'loaded track does not exist in file system | {}'.format(track['path'])
            logger.warning(warning)

    if tracks:
        print('[mongo] {} track{} found'.format(len(tracks), 's'[len(tracks) == 1:]))
    else:
        print('[mongo] no track found')

    return tracks


def is_database_empty():
    """Return True is there is at least one track in the collection. Otherwise, return False."""
    return not get_collection().find().count()
