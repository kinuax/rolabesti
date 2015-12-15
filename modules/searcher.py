#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import basename, splitext

from modules.database import get_tracks

LOG_NAME = splitext(basename(__file__))[0]
SEARCH_FIELDS = ('place', 'genre', 'artist', 'album')


def filtered_by_fields(track, fields):
    for field, value in fields.items():
        if field not in track or value.lower() not in track[field].lower():
            return False

    return True


def search(arguments):
    tracks = []
    fields = {field: value for field, value in arguments.iteritems()
              if field in SEARCH_FIELDS}

    print '[searcher] searching tracks'

    if fields:
        for track in get_tracks():
            if arguments['min'] <= track['length'] <= arguments['max']:
                if filtered_by_fields(track, fields):
                    tracks.append(track)
    else:
        for track in get_tracks():
            if arguments['min'] <= track['length'] <= arguments['max']:
                tracks.append(track)

    if not tracks:
        print '[searcher] no track found'

    return tracks
