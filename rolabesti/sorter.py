# -*- coding: utf-8 -*-
"""
rolabesti.sorter
~~~~~~~~~~~~~~~~

This module contains all the supported sortings and the sort function.
"""

import random

SORTINGS = ('asc', 'desc', 'random')


def sort(tracks, sorting):
    """Return tracks sorted by sorting type."""
    if sorting == 'asc':
        return tracks
    elif sorting == 'desc':
        return reversed(tracks)
    else:
        return random.sample(tracks, len(tracks))
