#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import basename, splitext
import sys

from mutagen.easyid3 import EasyID3
from mutagen.id3._util import ID3NoHeaderError

from logger import get_logger
from database import COUNTS

LOG_NAME = splitext(basename(__file__))[0]
VALUES = ('', 'unknown', 'other', 'default', 'no artist', 'no title', 'genre', 'title')


def tag(tracks):
    logger = get_logger(LOG_NAME)
    count = 0

    for track in tracks:
        try:
            tags = get_tags(track['path'].encode('utf-8'))
        except:
            error = sys.exc_info()
            error = u'tagging track | %s - %s | %s' % \
                (str(error[0]), str(error[1]), track['path'])
            logger.error(error)

            continue

        save = False

        if 'genre' in track and ('genre' not in tags or
                    (tags['genre'] or [''])[0].strip().lower() in VALUES):
            tags['genre'] = track['genre']
            save = True

        if 'artist' in track and ('artist' not in tags or
                    (tags['artist'] or [''])[0].strip().lower() in VALUES or
                    ((tags['artist'] or [''])[0] != track['artist'] and
                    (tags['artist'] or [''])[0].strip().lower() == track['artist'].lower())):
            tags['artist'] = track['artist']
            save = True

        if 'album' in track and ('album' not in tags or
                    (tags['album'] or [''])[0].strip().lower() in VALUES):
            tags['album'] = track['album']
            save = True

        if 'filename' in track and ('title' not in tags or
                    (tags['title'] or [''])[0].strip().lower() in VALUES):
            tags['title'] = track['filename']
            save = True

        if save:
            tags.save()

            count += 1

            if count in COUNTS:
                print '[mutagen] tagging %d tracks' % count

    print '[mutagen] %d track%s tagged' % (count, 's'[count == 1:])


def get_tags(trackpath):
    try:
        return EasyID3(trackpath)
    except ID3NoHeaderError:
        EasyID3().save(trackpath)

        return EasyID3(trackpath)
