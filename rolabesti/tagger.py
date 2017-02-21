# -*- coding: utf-8 -*-

from .constants import COUNTS
from .utils import get_id3_obj

VALUES = ('', 'unknown', 'other', 'default', 'no artist', 'no title', 'genre', 'title')


def tag(tracks):
    count = 0

    for track in tracks:
        id3 = get_id3_obj(track['path'])

        if not id3:
            continue

        save = False

        if 'genre' in track and ('genre' not in id3 or (id3['genre'] or [''])[0].strip().lower() in VALUES):
            id3['genre'] = track['genre']
            save = True

        if 'artist' in track and ('artist' not in id3 or
                    (id3['artist'] or [''])[0].strip().lower() in VALUES or
                    ((id3['artist'] or [''])[0] != track['artist'] and
                    (id3['artist'] or [''])[0].strip().lower() == track['artist'].lower())):
            id3['artist'] = track['artist']
            save = True

        if 'album' in track and ('album' not in id3 or (id3['album'] or [''])[0].strip().lower() in VALUES):
            id3['album'] = track['album']
            save = True

        if 'title' in track and ('title' not in id3 or (id3['title'] or [''])[0].strip().lower() in VALUES):
            id3['title'] = track['title']
            save = True

        if save:
            id3.save()

            count += 1

            if count in COUNTS:
                print('[mutagen] tagging %d tracks' % count)

    print('[mutagen] %d track%s tagged' % (count, 's'[count == 1:]))
