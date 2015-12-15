#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import walk
from os.path import basename, exists, join, splitext
import re
import sys

from mutagen.mp3 import MP3

from modules.logger import get_logger
from settings import DB_DIR, MUSIC_DIR
from tools.json_tools import dump_to_json, load_from_json

LOG_NAME = splitext(basename(__file__))[0]
PARSINGS = (
    (r'/Places/(.+?)/Genres/(.+?)/Albums/(.+?)/(.+/)*(.+)\.[mM][pP]3$', ('place', 'genre', 'album', 'other', 'filename')),
    (r'/Places/(.+?)/Genres/(.+?)/(.+?)/(.+?)/(.+/)*(.+)\.[mM][pP]3$', ('place', 'genre', 'artist', 'album', 'other', 'filename')),
    (r'/Places/(.+?)/Genres/(.+?)/(.+?)/(.+)\.[mM][pP]3$', ('place', 'genre', 'artist', 'filename')),
    (r'/Places/(.+?)/Albums/(.+?)/(.+/)*(.+)\.[mM][pP]3$', ('place', 'album', 'other', 'filename')),
    (r'/Places/(.+?)/(.+?)/(.+?)/(.+/)*(.+)\.[mM][pP]3$', ('place', 'artist', 'album', 'other', 'filename')),
    (r'/Places/(.+?)/(.+?)/(.+)\.[mM][pP]3$', ('place', 'artist', 'filename')),
    (r'/Genres/(.+?)/Albums/(.+?)/(.+/)*(.+)\.[mM][pP]3$', ('genre', 'album', 'other', 'filename')),
    (r'/Genres/(.+?)/(.+?)/(.+?)/(.+/)*(.+)\.[mM][pP]3$', ('genre', 'artist', 'album', 'other', 'filename')),
    (r'/Genres/(.+?)/(.+?)/(.+)\.[mM][pP]3$', ('genre', 'artist', 'filename')),
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
    info = 'building new index'
    logger.info(info)
    print '[database] ' + info

    for dirpath, dirnames, filenames in walk(MUSIC_DIR):
        if re.search(r'/Places/|/Genres/', dirpath):
            trackpaths = [join(dirpath, filename).decode('utf-8')
                          for filename in filenames if re.search(r'\.[mM][pP]3$', filename)]

            for trackpath in trackpaths:
                track = parse(trackpath)

                if track:
                    try:
                        track['length'] = get_length(trackpath)
                    except:
                        error = sys.exc_info()
                        error = u'getting track length | %s - %s | %s' % \
                            (str(error[0]), str(error[1]), trackpath)
                        logger.error(error)

                        continue

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

                    info = u'track indexed | %s' % track['path']
                    logger.info(info)

                    if count in COUNTS:
                        print '[database] indexing %d tracks' % count

                else:
                    warning = u'track parsing not found | %s' % trackpath
                    logger.warning(warning)

    dump_to_json(sorted(places), join(DB_DIR, 'places.json'))
    dump_to_json(sorted(genres), join(DB_DIR, 'genres.json'))
    dump_to_json(sorted(artists), join(DB_DIR, 'artists.json'))
    dump_to_json(sorted(albums), join(DB_DIR, 'albums.json'))
    dump_to_json(tracks, join(DB_DIR, 'tracks.json'))

    info = 'new index built'
    logger.info(info)
    print '[database] ' + info

    info = '%d tracks indexed' % count
    logger.info(info)
    print '[database] ' + info


def parse(trackpath):
    for parsing in PARSINGS:
        match = re.search(parsing[0], trackpath)

        if match:
            track = {'path': trackpath}
            values = match.groups()

            for i, field in enumerate(parsing[1]):
                if field != 'other':
                    track[field] = values[i]

            return track


def get_length(trackpath):
    audio = MP3(trackpath)

    return audio.info.length


def get_tracks():
    """
    Return a list with existing indexed tracks.
    """
    logger = get_logger(LOG_NAME)
    indexed_tracks = load_from_json(join(DB_DIR, 'tracks.json'))
    tracks = []

    for track in indexed_tracks:
        if exists(track['path']):
            tracks.append(track)
        else:
            warning = u'indexed track does not exist in file system | %s' % track['path']
            logger.warning(warning)

    return tracks
