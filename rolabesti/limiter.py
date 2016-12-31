#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils import format_length


def limit(tracks, total_length):
    """Return (tracklist, length) tuple, where tracklist length is less than
    or equal to total_length and length is the formatted tracklist length."""
    tracklist = []
    length = 0.0

    print('[rolabesti] creating tracklist')

    for track in tracks:
        if track['length'] <= total_length - length:
            length += track['length']
            tracklist.append(track)
        else:
            break

    return tracklist, format_length(length)
