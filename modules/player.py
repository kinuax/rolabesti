#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tools.process import execute, running_process


def play(tracks):
    if running_process('vlc'):
        command = ['vlc']
    else:
        print 'vlc not running'
        print 'opening vlc'
        print 'playing %s' % tracks[0]['path']

        command = ['vlc', tracks[0]['path']]
        tracks.pop(0)

    for track in tracks:
        command.append(track['path'])

    execute(command)

    print '%d tracks enqueued' % len(tracks)
