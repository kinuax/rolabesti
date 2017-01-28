# -*- coding: utf-8 -*-

from collections import OrderedDict
import re

from utils import get_logger

PARSINGS = OrderedDict()
PARSINGS[r'/Places/(.+?)/Genres/(.+?)/Albums/(.+?)/(.+/)*(.+)\.[mM][pP]3$'] = ('place', 'genre', 'album', 'side', 'filename')
PARSINGS[r'/Places/(.+?)/Genres/(.+?)/(.+?)/(.+?)/(.+/)*(.+)\.[mM][pP]3$'] = ('place', 'genre', 'artist', 'album', 'side', 'filename')
PARSINGS[r'/Places/(.+?)/Genres/(.+?)/(.+?)/(.+)\.[mM][pP]3$'] = ('place', 'genre', 'artist', 'filename')
PARSINGS[r'/Places/(.+?)/Albums/(.+?)/(.+/)*(.+)\.[mM][pP]3$'] = ('place', 'album', 'side', 'filename')
PARSINGS[r'/Places/(.+?)/(.+?)/(.+?)/(.+/)*(.+)\.[mM][pP]3$'] = ('place', 'artist', 'album', 'side', 'filename')
PARSINGS[r'/Places/(.+?)/(.+?)/(.+)\.[mM][pP]3$'] = ('place', 'artist', 'filename')
PARSINGS[r'/Genres/(.+?)/Albums/(.+?)/(.+/)*(.+)\.[mM][pP]3$'] = ('genre', 'album', 'side', 'filename')
PARSINGS[r'/Genres/(.+?)/(.+?)/(.+?)/(.+/)*(.+)\.[mM][pP]3$'] = ('genre', 'artist', 'album', 'side', 'filename')
PARSINGS[r'/Genres/(.+?)/(.+?)/(.+)\.[mM][pP]3$'] = ('genre', 'artist', 'filename')
logger = get_logger(__file__)


def parse(trackpath):
    """Match and parse trackpath against PARSINGS.

    Return a dictionary with parsed fields if there is a parsing to match.
    Otherwise, log the trackpath and return an empty dictionary.
    """
    for regex, fields in PARSINGS.items():
        match = re.search(regex, trackpath)

        if match:
            return {field: value for field, value in zip(fields, match.groups())}

    info = 'parsing not found | {}'.format(trackpath)
    logger.info(info)

    return {}
