# -*- coding: utf-8 -*-
"""
rolabesti.mongo
~~~~~~~~~~~~~~~

This module contains all the MongoDB related functionality.
"""

from contextlib import contextmanager
from logging import getLogger
from os import walk
from os.path import exists, join
import re

from pymongo import MongoClient

from .conf.settings import MONGO_HOST, MONGO_PORT, MONGO_DBNAME, MONGO_COLNAME
from .constants import TRACK_FIELDS, COUNTS
from .parser import parse
from .utils import add_prefix_to_dict, get_length, get_id3_tags


def load(music_dir):
    """Load the collection with mp3 files from music_dir."""
    count = 0
    info = 'loading new database from scratch : MUSIC_DIR = {}'.format(music_dir)
    logger = getLogger(__name__)
    logger.info(info)
    print('[mongo]', info)

    with get_collection() as collection:
        collection.remove({})

        for dirpath, dirnames, filenames in walk(music_dir):
            for filename in filenames:
                if filename.lower().endswith('.mp3'):
                    trackpath = join(dirpath, filename)
                    length = get_length(trackpath)

                    if length:
                        parsed = parse(trackpath)

                        if parsed:
                            track = {'path': trackpath, 'length': length}
                            track.update(add_prefix_to_dict(parsed, 'parsed'))
                            track.update(add_prefix_to_dict(get_id3_tags(trackpath), 'id3'))

                            collection.insert_one(track)
                            count += 1

                            if count in COUNTS:
                                print('[mongo] loading {} tracks'.format(count))

    info = 'new database loaded : {} track{} loaded'.format(count, 's'[count == 1:])
    logger.info(info)
    print('[mongo]', info)


def search(arguments):
    """Return a (tracks, length) tuple, where tracks is the list of found tracks
    based on arguments and length is the length of tracks.
    """
    tracks = []
    length = 0
    length_filters = {}
    filters = []
    logger = getLogger(__name__)

    with get_collection() as collection:
        if not collection.count():
            print('[mongo] there is no track loaded to the database, load subcommand should be run first')
            return tracks, length

    print('[mongo] searching tracks')

    if arguments['max'] > 0:
        length_filters['$lte'] = arguments['max']

    if arguments['min'] > 0:
        length_filters['$gte'] = arguments['min']

    if length_filters:
        filters.append({'length': length_filters})

    for arg in set.intersection(set(arguments), set(TRACK_FIELDS)):
        value = re.compile(arguments[arg], re.IGNORECASE)
        fields = TRACK_FIELDS[arg]

        if len(fields) == 1:
            filter_ = {fields[0]: value}
        else:  # len(fields) = 2
            filter_ = {'$or': [{fields[0]: value}, {'$and': [{fields[0]: {'$exists': False}}, {fields[1]: value}]}]}

        filters.append(filter_)

    with get_collection() as collection:
        for track in collection.find({'$and': filters}):
            if exists(track['path']):
                tracks.append(track)
                length += track['length']
            else:
                warning = 'loaded track does not exist in file system | {}'.format(track['path'])
                logger.warning(warning)

    if tracks:
        print('[mongo] {} track{} found'.format(len(tracks), 's'[len(tracks) == 1:]))
    else:
        print('[mongo] no track found')

    return tracks, length


def update(id_, field, value):
    """Update track with a new field."""
    with get_collection() as collection:
        collection.update({"_id": id_}, {"$set": {field: value}})


@contextmanager
def get_collection():
    client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)

    yield client[MONGO_DBNAME][MONGO_COLNAME]

    client.close()
