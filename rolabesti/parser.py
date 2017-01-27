# -*- coding: utf-8 -*-

from collections import OrderedDict
import re

from utils import get_logger

PARSINGS = OrderedDict({
    r'/Places/(.+?)/Genres/(.+?)/Albums/(.+?)/(.+/)*(.+)\.[mM][pP]3$': ('place', 'genre', 'album', 'side', 'filename'),
    r'/Places/(.+?)/Genres/(.+?)/(.+?)/(.+?)/(.+/)*(.+)\.[mM][pP]3$': ('place', 'genre', 'artist', 'album', 'side', 'filename'),
    r'/Places/(.+?)/Genres/(.+?)/(.+?)/(.+)\.[mM][pP]3$': ('place', 'genre', 'artist', 'filename'),
    r'/Places/(.+?)/Albums/(.+?)/(.+/)*(.+)\.[mM][pP]3$': ('place', 'album', 'side', 'filename'),
    r'/Places/(.+?)/(.+?)/(.+?)/(.+/)*(.+)\.[mM][pP]3$': ('place', 'artist', 'album', 'side', 'filename'),
    r'/Places/(.+?)/(.+?)/(.+)\.[mM][pP]3$': ('place', 'artist', 'filename'),
    r'/Genres/(.+?)/Albums/(.+?)/(.+/)*(.+)\.[mM][pP]3$': ('genre', 'album', 'side', 'filename'),
    r'/Genres/(.+?)/(.+?)/(.+?)/(.+/)*(.+)\.[mM][pP]3$': ('genre', 'artist', 'album', 'side', 'filename'),
    r'/Genres/(.+?)/(.+?)/(.+)\.[mM][pP]3$': ('genre', 'artist', 'filename'),
})
logger = get_logger(__file__)


def parse(trackpath):
    """Match and parse trackpath against PARSINGS.

    If there is a parsing to match, return a dictionary with parsed fields.
    If there is no parsing to match, return an empty dictionary.
    """
    for regex, fields in PARSINGS.items():
        match = re.search(regex, trackpath)

        if match:
            return {field: value for field, value in zip(fields, match.groups())}

    info = 'parsing not found | {}'.format(trackpath)
    logger.info(info)

    return {}
