#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils import format_length

SUMMARY_FIELDS = ('artist', 'album', 'genre', 'place')


def print_tracks(tracks):
    length = 0.0
    summary = {}

    for field in SUMMARY_FIELDS:
        summary[field] = []

    print('[rolabesti] printing tracks')

    for track in tracks:
        length += track['length']
        output = []

        if 'artist' in track:
            output.append('Artist = {}'.format(track['artist']))

        if 'title' in track:
            output.append('Title = {}'.format(track['title']))

        for field in SUMMARY_FIELDS:
            if field in track:
                value = track[field]

                if value not in summary[field]:
                    summary[field].append(value)

                if field != 'artist':
                    output.append(field.capitalize() + ' = ' + value)

        output.append('Length = ' + format_length(track['length']))
        output.append('Filename = ' + track['filename'])

        print(' | '.join(output))

    print('[rolabesti] printing summary')
    print('Number of tracks:', len(tracks))
    print('Length:', format_length(length))

    for field in SUMMARY_FIELDS:
        if summary[field]:
            count = len(summary[field])
            values = ' | '.join(sorted(summary[field]))

            print('%ss (%d): %s' % (field.capitalize(), count, values))
