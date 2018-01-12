# -*- coding: utf-8 -*-
"""
rolabesti.mongo
~~~~~~~~~~~~~~~

This module contains all the MongoDB related functionality.
"""

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
    collection = get_collection()
    collection.remove({})
    count = 0

    info = 'loading new database from scratch : MUSIC_DIR = {}'.format(music_dir)
    logger = getLogger(__name__)
    logger.info(info)
    print('[mongo]', info)

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
    length = 0.0
    collection = get_collection()
    and_list = [{}]
    length_filters = {}
    logger = getLogger(__name__)

    if arguments['max'] > 0:
        length_filters['$lte'] = arguments['max']

    if arguments['min'] > 0:
        length_filters['$gte'] = arguments['min']

    if length_filters:
        and_list[0] = {'length': length_filters}

    print('[mongo] searching tracks')

    for key_field, fields in TRACK_FIELDS.items():
        if key_field in arguments:
            value = re.compile(arguments[key_field], re.IGNORECASE)
            or_list = [{field: value} for field in fields]
            and_list.append({'$or': or_list})

    for track in collection.find({'$and': and_list}):
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

        if not get_collection().find().count():
            print('[mongo] there is no track loaded to the database, load subcommand should be run first')

    return tracks, length


def update(_id, field, value):
    """Update track with a new field."""
    get_collection().update({"_id": _id}, {"$set": {field: value}})


def get_collection():
    client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)

    return client[MONGO_DBNAME][MONGO_COLNAME]
