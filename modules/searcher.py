#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import basename, exists, splitext

from modules.database import get_tracks
from modules.logger import get_logger

LOG_NAME = splitext(basename(__file__))[0]
SEARCH_FIELDS = ('place', 'genre', 'artist', 'album')


def filtered_by_fields(track, fields):
    for field, value in fields.items():
        if field not in track or value.lower() not in track[field].lower():
            return False

    return True


def track_exists(trackpath):
    if exists(trackpath):
        return True
    else:
        logger = get_logger(LOG_NAME)
        warning = u'indexed track does not exist in file system | %s' % trackpath
        logger.info(warning)

        return False


def search(arguments):
    tracks = []
    fields = {field: value for field, value in arguments.iteritems()
              if field in SEARCH_FIELDS}

    print '[searcher] searching tracks'

    if fields:
        for track in get_tracks():
            if arguments['min'] <= track['length'] <= arguments['max']:
                if filtered_by_fields(track, fields):
                    if track_exists(track['path']):
                        tracks.append(track)
    else:
        for track in get_tracks():
            if arguments['min'] <= track['length'] <= arguments['max']:
                if track_exists(track['path']):
                    tracks.append(track)

    if not tracks:
        print '[searcher] no track found'

    return tracks
