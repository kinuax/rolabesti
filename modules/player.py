#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tools.process import execute, running_process


def play(tracks, length):
    command = ['vlc']
    count = len(tracks)

    for track in tracks:
        command.append(track['path'])

    if not running_process('vlc'):
        count -= 1

        print '[system] vlc closed'
        print '[system] opening vlc'
        print u'[vlc] playing ' + tracks[0]['path']

    execute(command)

    if count:
        print '[vlc] %d track%s enqueued' % (count, 's'[count == 1:])

    print '[vlc] tracklist length is ' + length
