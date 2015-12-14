#!/usr/bin/env python
# -*- coding: utf-8 -*-

from searcher import SEARCH_FIELDS
from tools.misc import format_length


def list_tracks(tracks):
    length = 0.0
    summary = {}

    for field in SEARCH_FIELDS:
        summary[field] = []

    print '[lister] listing tracks'

    for track in tracks:
        length += track['length']
        string = []

        for field in SEARCH_FIELDS:
            if field in track:
                value = track[field].encode('utf-8')

                if value not in summary[field]:
                    summary[field].append(value)

                string.append(field.capitalize() + ' = ' + value)

        string.append('Length = ' + format_length(track['length']))
        string.append('Filename = ' + track['filename'].encode('utf-8'))
        string = ' | '.join(string)

        print(string)

    print '[lister] listing summary'
    print 'Number of tracks: %d' % len(tracks)
    print 'Length: ' + format_length(length)

    for field in SEARCH_FIELDS:
        if summary[field]:
            count = len(summary[field])
            values = ' | '.join(sorted(summary[field]))

            print '%ss (%d): %s' % (field.capitalize(), count, values)
