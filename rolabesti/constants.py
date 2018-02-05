# -*- coding: utf-8 -*-
"""
rolabesti.constants
~~~~~~~~~~~~~~~~~~~

This module contains some readonly variables.
"""

from collections import OrderedDict

TRACK_FIELDS = OrderedDict()
TRACK_FIELDS['artist'] = ('parsed_artist', 'id3_artist')
TRACK_FIELDS['title'] = ('id3_title', 'parsed_title')
TRACK_FIELDS['album'] = ('parsed_album', 'id3_album')
TRACK_FIELDS['genre'] = ('parsed_genre', 'id3_genre')
TRACK_FIELDS['place'] = ('parsed_place',)

ID3_TAGS = ('album', 'artist', 'genre', 'title')

COUNTS = (5, 10, 50, 100, 500, 1000, 2000, 5000, 10000, 15000, 20000, 25000, 30000, 40000, 50000)
