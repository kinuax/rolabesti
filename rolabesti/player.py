# -*- coding: utf-8 -*-
"""
rolabesti.player
~~~~~~~~~~~~~~~~

This module is in charge of playing and enqueueing tracks in the supported players.
"""

import sys
from time import sleep

import vlc

from .conf.settings import OVERLAP_LENGTH
from .utils import execute, is_running, track_to_string

MAXIMUM_OVERLAP_LENGTH = 30
MINIMUM_OVERLAP_LENGTH = 0
PLAYERS = ('shell', 'vlc')


def play(tracks, player):
    count = len(tracks)

    if player == 'shell':
        instance = vlc.Instance()
        players = {0: instance.media_player_new(), 1: instance.media_player_new()}

        for i, track in enumerate(tracks):
            print('[rolabesti] now playing : {}'.format(track_to_string(track)))

            media = instance.media_new(track['path'])
            player = i % 2
            players[player].set_media(media)
            players[player].play()

            sleep(int(track['length']) - OVERLAP_LENGTH)  # Stop running until the next track begins
    else:
        if sys.platform.startswith('linux'):
            command = ['vlc']
        elif sys.platform.startswith('darwin'):
            command = ['/Applications/VLC.app/Contents/MacOS/VLC']
        else:
            error = '[system] platform not supported'
            sys.exit(error)

        if not is_running('vlc'):
            count -= 1

            print('[system] vlc closed')
            print('[system] opening vlc')
            print('[vlc] now playing : {}'.format(track_to_string(tracks[0])))

        if count:
            print('[vlc] {} track{} enqueued'.format(count, 's'[count == 1:]))

        for track in tracks:
            command.append(track['path'])

        execute(command)
