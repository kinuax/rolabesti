# -*- coding: utf-8 -*-

from os.path import basename, splitext
import re

from logger import get_logger

LOG_NAME = splitext(basename(__file__))[0]
logger = get_logger(LOG_NAME)
PARSINGS = {
    r'/Places/(.+?)/Genres/(.+?)/Albums/(.+?)/(.+/)*(.+)\.[mM][pP]3$': ('place', 'genre', 'album', 'side', 'filename'),
    r'/Places/(.+?)/Genres/(.+?)/(.+?)/(.+?)/(.+/)*(.+)\.[mM][pP]3$': ('place', 'genre', 'artist', 'album', 'side', 'filename'),
    r'/Places/(.+?)/Genres/(.+?)/(.+?)/(.+)\.[mM][pP]3$': ('place', 'genre', 'artist', 'filename'),
    r'/Places/(.+?)/Albums/(.+?)/(.+/)*(.+)\.[mM][pP]3$': ('place', 'album', 'side', 'filename'),
    r'/Places/(.+?)/(.+?)/(.+?)/(.+/)*(.+)\.[mM][pP]3$': ('place', 'artist', 'album', 'side', 'filename'),
    r'/Places/(.+?)/(.+?)/(.+)\.[mM][pP]3$': ('place', 'artist', 'filename'),
    r'/Genres/(.+?)/Albums/(.+?)/(.+/)*(.+)\.[mM][pP]3$': ('genre', 'album', 'side', 'filename'),
    r'/Genres/(.+?)/(.+?)/(.+?)/(.+/)*(.+)\.[mM][pP]3$': ('genre', 'artist', 'album', 'side', 'filename'),
    r'/Genres/(.+?)/(.+?)/(.+)\.[mM][pP]3$': ('genre', 'artist', 'filename'),
}


def parse(filepath):
    """Return a dictionary with parsed fields. If no parsing is found, return None."""
    for regex, fields in PARSINGS.items():
        match = re.search(regex, filepath)

        if match:
            track = {'path': filepath}

            for field, value in zip(fields, match.groups()):
                track[field] = value

            return track

    info = 'parsing not found | {}'.format(filepath)
    logger.info(info)

    return None
