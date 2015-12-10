#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import modf


def format_length(length):
    length = int(modf(length)[1])

    if length < 60:
        return '%d seconds' % length
    elif length < 3600:
        minutes = length / 60
        seconds = length % 60

        return '%s:%s minutes' % (format(minutes, '02'), format(seconds, '02'))
    else:
        hours = length / 3600
        minutes = (length % 3600) / 60
        seconds = (length % 3600) % 60

        return '%d:%s:%s hours' % (hours,
                                   format(minutes, '02'),
                                   format(seconds, '02'))


def limit(tracks, total_length):
    """
    Return (tracklist, length) tuple, where tracklist length is less than
    or equal to total_length and length is the formatted tracklist length
    """
    tracklist = []
    length = 0.0

    for track in tracks:
        if track['length'] <= total_length - length:
            length += track['length']
            tracklist.append(track)
        else:
            break

    return tracklist, format_length(length)
