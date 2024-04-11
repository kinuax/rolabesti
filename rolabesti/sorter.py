# -*- coding: utf-8 -*-
"""
rolabesti.sorter
~~~~~~~~~~~~~~~~

This module contains all the supported sortings and the sort function.
"""

from operator import itemgetter
import random

SORTINGS = ('asc', 'desc', 'random')


def sort(tracks, sorting: str):
    """Return tracks sorted by sorting type."""
    if sorting == 'asc':
        return sorted(tracks, key=itemgetter('path'))
    elif sorting == 'desc':
        return sorted(tracks, key=itemgetter('path'), reverse=True)
    else:
        return random.sample(tracks, len(tracks))
