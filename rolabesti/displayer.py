# -*- coding: utf-8 -*-
"""
rolabesti.displayer
~~~~~~~~~~~~~~~~~~~

This module is in charge of printing tracks data to the standard output.
"""

from .constants import TRACK_FIELDS
from .utils import format_length, track_to_string

SUMMARY_FIELDS = ('artist', 'album', 'genre', 'place')


def display(tracks, length):
    """Print tracklist and summary of tracks."""
    summary = {field: set() for field in SUMMARY_FIELDS}

    print('[rolabesti] ------------ TRACKLIST ------------')

    for track in tracks:
        for sum_field in SUMMARY_FIELDS:
            for field in TRACK_FIELDS[sum_field]:
                if field in track:
                    summary[sum_field].add(track[field])

                break

        print(track_to_string(track))

    print('[rolabesti] ------------ SUMMARY --------------')
    print('Number of tracks: {}'.format(len(tracks)))
    print('Length: {}'.format(format_length(length)))

    for field in SUMMARY_FIELDS:
        if summary[field]:
            values = ' | '.join(sorted(summary[field]))

            print('{}s ({}): {}'.format(field.capitalize(), len(summary[field]), values))
