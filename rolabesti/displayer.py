# -*- coding: utf-8 -*-
"""
rolabesti.displayer
~~~~~~~~~~~~~~~~~~~

This module is in charge of printing tracks data to the standard output.
"""
from .constants import TRACK_FIELDS
from .utils import format_length

SUMMARY_FIELDS = ('artist', 'album', 'genre', 'place')


def display(tracks, length):
    """Print tracklist and summary of tracks."""
    summary = {}

    for key_field in TRACK_FIELDS:
        summary[key_field] = []

    print('[rolabesti] ------------ TRACKLIST ------------')

    for track in tracks:
        string = []

        for key_field, fields in TRACK_FIELDS.items():
            for field in fields:
                if field in track:
                    string.append('{} = {}'.format(key_field.capitalize(), track[field]))

                    if key_field in SUMMARY_FIELDS and track[field] not in summary[key_field]:
                        summary[key_field].append(track[field])

                    break

        string.append('Length = {}'.format(format_length(track['length'])))

        print(' | '.join(string))

    print('[rolabesti] ------------ SUMMARY --------------')
    print('Number of tracks: {}'.format(len(tracks)))
    print('Length: {}'.format(format_length(length)))

    for key_field in TRACK_FIELDS:
        if summary[key_field]:
            values = ' | '.join(sorted(summary[key_field]))

            print('{}s ({}): {}'.format(key_field.capitalize(), len(summary[key_field]), values))
