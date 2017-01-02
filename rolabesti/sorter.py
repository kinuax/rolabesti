#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

SORTINGS = ('asc', 'desc', 'random')


def sort(tracks, sorting):
    if sorting == 'asc':
        return tracks
    elif sorting == 'desc':
        return reversed(tracks)
    else:
        return random.sample(tracks, len(tracks))
