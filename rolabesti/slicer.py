# -*- coding: utf-8 -*-
"""
rolabesti.slicer
~~~~~~~~~~~~~~~~

This module contains the functionality to slice a list of tracks based on maximum tracklist length.
"""


def slice_tracks(tracks, max_tracklist_length):
    """Return a (tracks, length) tuple, where tracks is the list of tracks with length
    less than or equal to max_tracklist_length and length is the length of tracks.
    """
    length = 0.0

    for i, track in enumerate(tracks):
        if length + track['length'] <= max_tracklist_length:
            length += track['length']
        else:
            break

    return tracks[:i + 1], length
