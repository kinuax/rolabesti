#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils import format_length


def limit(tracks, max_tracklist_length):
    """Return (tracklist, length) tuple, where tracklist is the list of tracks with length
    less than or equal to max_tracklist_length and length is the formatted tracklist length.
    """
    tracklist = []
    length = 0.0

    print('[rolabesti] creating tracklist')

    for track in tracks:
        if length + track['length'] <= max_tracklist_length:
            tracklist.append(track)
            length += track['length']
        else:
            break

    return tracklist, format_length(length)
