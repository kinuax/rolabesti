# -*- coding: utf-8 -*-


def limit(tracks, max_tracklist_length):
    """Return a (tracks, length) tuple, where tracks is the list of tracks with length
    less than or equal to max_tracklist_length and length is the tracks length.
    """
    length = 0.0

    for i, track in enumerate(tracks):
        if length + track['length'] <= max_tracklist_length:
            length += track['length']
        else:
            break

    return tracks[:i], length
