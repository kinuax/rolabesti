# -*- coding: utf-8 -*-

import re

from utils import get_logger

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
    logger = get_logger(__file__)

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
