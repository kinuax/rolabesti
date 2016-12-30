#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random


def sort(tracks, sorting):
    if sorting == 'asc':
        return tracks
    elif sorting == 'desc':
        tracks.reverse()

        return tracks
    else:
        return random.sample(tracks, len(tracks))
