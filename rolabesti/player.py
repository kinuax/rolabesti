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


def play(tracks, player, overlap_length=OVERLAP_LENGTH):
    count = len(tracks)

    if player == 'shell':
        # Create two players to manage contiguous tracks.
        instance = vlc.Instance()
        players = {0: instance.media_player_new(), 1: instance.media_player_new()}

        for i, track in enumerate(tracks):
            print('[rolabesti] playing | {}'.format(track_to_string(track)))

            # Select player and play track.
            media = instance.media_new(track['path'])
            player = i % 2
            players[player].set_media(media)
            players[player].play()

            # Adjust waiting_length. Filter out last track and too short tracks.
            track_length = int(track['length'])
            if i < count - 1 and overlap_length < track_length:
                waiting_length = track_length - overlap_length
            else:
                waiting_length = track_length

            try:
                # Wait for the next track to play.
                sleep(waiting_length)
            except KeyboardInterrupt:
                print('\n[rolabesti] exiting')
                sys.exit(0)
    else:
        if sys.platform.startswith('linux'):
            command = ['vlc']
        elif sys.platform.startswith('darwin'):
            command = ['/Applications/VLC.app/Contents/MacOS/VLC']
        else:
            error = '[rolabesti] platform not supported'
            sys.exit(error)

        if not is_running('vlc'):
            count -= 1

            print('[rolabesti] vlc is down, running it')
            print('[vlc] playing | {}'.format(track_to_string(tracks[0])))

        if count:
            print('[vlc] {} track{} enqueued'.format(count, 's'[count == 1:]))

        for track in tracks:
            command.append(track['path'])

        execute(command)
