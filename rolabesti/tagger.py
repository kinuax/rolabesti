# -*- coding: utf-8 -*-
"""
rolabesti.tagger
~~~~~~~~~~~~~~~~

This module contains the functionality to manage the ID3 tags of loaded tracks.
"""

from logging import getLogger

from .constants import COUNTS
from .mongo import update
from .utils import get_id3_obj


def tag(tracks, id3_tag):
    """Update tracks with new ID3 tag value given by corresponding parsed field,
    both in system file and database.
    """
    logger = getLogger(__name__)
    parsed_field = 'parsed_{}'.format(id3_tag)
    id3_field = 'id3_{}'.format(id3_tag)
    count = 0

    for track in tracks:
        if parsed_field in track and id3_field in track and track[id3_field] != track[parsed_field]:
            id3 = get_id3_obj(track['path'])

            if not id3:
                continue

            id3[id3_tag] = track[parsed_field]
            id3.save()

            update(track['_id'], id3_field, track[parsed_field])

            info = 'track updated with new {} ID3 tag | {}'.format(id3_tag, track['path'])
            logger.info(info)

            count += 1

            if count in COUNTS:
                print('[rolabesti] tagging {} tracks'.format(count))

    print('[rolabesti] %d track%s tagged' % (count, 's'[count == 1:]))
