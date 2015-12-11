#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

SORTINGS = ('asc', 'desc', 'random')


def sort(tracks, sorting):
    if sorting == 'asc':
        return tracks
    elif sorting == 'desc':
        tracks.reverse()

        return tracks
    else:
        return random.sample(tracks, len(tracks))
