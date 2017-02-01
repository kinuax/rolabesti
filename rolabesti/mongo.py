# -*- coding: utf-8 -*-
"""
rolabesti.mongo
~~~~~~~~~~~~~~~

This module contains all the MongoDB related functionality.
"""
from os import walk
from os.path import exists, join
import re

from pymongo import MongoClient

from .constants import TRACK_FIELDS, COUNTS
from .parser import parse
from .settings import MUSIC_DIR, MONGO_HOST, MONGO_PORT, MONGO_DBNAME, MONGO_COLNAME
from .utils import add_prefix_to_dict, get_length, get_logger, get_id3_tags

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
                    track.update(add_prefix_to_dict(parse(trackpath), 'parsed'))
                    track.update(add_prefix_to_dict(get_id3_tags(trackpath), 'id3'))

                    collection.insert_one(track)
                    count += 1

                    if count in COUNTS:
                        print('[mongo] loading {} tracks'.format(count))

    info = 'new database loaded : {} track{} loaded'.format(count, 's'[count == 1:])
    logger.info(info)
    print('[mongo]', info)


def search(arguments):
    tracks = []
    length = 0.0
    collection = get_collection()
    and_list = [{'length': {'$gte': arguments['min'], '$lte': arguments['max']}}]

    print('[mongo] searching tracks')

    for key_field, fields in TRACK_FIELDS.items():
        if key_field in arguments:
            value = re.compile(arguments[key_field], re.IGNORECASE)
            or_list = [{field: value} for field in fields]
            and_list.append({"$or": or_list})

    for track in collection.find({"$and": and_list}):
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
