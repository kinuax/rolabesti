#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from database import COUNTS
from utils import get_tags

VALUES = ('', 'unknown', 'other', 'default', 'no artist', 'no title', 'genre', 'title')


def tag(tracks):
    count = 0

    for track in tracks:
        tags = get_tags(track['path'])

        if not tags:
            continue

        save = False

        if 'genre' in track and ('genre' not in tags or (tags['genre'] or [''])[0].strip().lower() in VALUES):
            tags['genre'] = track['genre']
            save = True

        if 'artist' in track and ('artist' not in tags or
                    (tags['artist'] or [''])[0].strip().lower() in VALUES or
                    ((tags['artist'] or [''])[0] != track['artist'] and
                    (tags['artist'] or [''])[0].strip().lower() == track['artist'].lower())):
            tags['artist'] = track['artist']
            save = True

        if 'album' in track and ('album' not in tags or (tags['album'] or [''])[0].strip().lower() in VALUES):
            tags['album'] = track['album']
            save = True

        if 'filename' in track and ('title' not in tags or (tags['title'] or [''])[0].strip().lower() in VALUES):
            tags['title'] = track['filename']
            save = True

        if save:
            tags.save()

            count += 1

            if count in COUNTS:
                print('[mutagen] tagging %d tracks' % count)

    print('[mutagen] %d track%s tagged' % (count, 's'[count == 1:]))
