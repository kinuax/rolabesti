#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from tools.process import execute, running_process


def play(tracks, length):
    count = len(tracks)

    if not running_process('vlc'):
        count -= 1

        print '[system] vlc closed'
        print '[system] opening vlc'
        print u'[vlc] playing ' + tracks[0]['path']

    if count:
        print '[vlc] enqueuing %d track%s' % (count, 's'[count == 1:])

    if sys.platform == 'linux2':
        command = ['vlc']
    elif sys.platform == 'darwin':
        command = ['/Applications/VLC.app/Contents/MacOS/VLC']
    else:
        error = '[system] platform not supported'
        sys.exit(error)

    for track in tracks:
        command.append(track['path'])

    execute(command)

    print '[vlc] tracklist length is ' + length
