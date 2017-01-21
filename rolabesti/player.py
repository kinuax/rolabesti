# -*- coding: utf-8 -*-

import sys
from time import sleep

import vlc

from database import SEARCH_FIELDS
from settings import PLAYING_MODE, OVERLAP_LENGTH
from utils import execute, format_length, is_running


def track_to_string(track):
    string = []

    for field in SEARCH_FIELDS:
        if field in track:
            value = track[field]
            string.append(field.capitalize() + ' = ' + value)

    string.append('Filename = ' + track['filename'])
    string.append('Length = ' + format_length(track['length']))

    return ' | '.join(string)


def play(tracks, length):
    count = len(tracks)

    if PLAYING_MODE == 'vlc':
        if not is_running('vlc'):
            count -= 1

            print('[system] vlc closed')
            print('[system] opening vlc')
            print('[vlc] playing:', track_to_string(tracks[0]))

        if count:
            print('[vlc] enqueuing %d track%s' % (count, 's'[count == 1:]))

        if sys.platform.startswith('linux'):
            command = ['vlc']
        elif sys.platform.startswith('darwin'):
            command = ['/Applications/VLC.app/Contents/MacOS/VLC']
        else:
            error = '[system] platform not supported'
            sys.exit(error)

        for track in tracks:
            command.append(track['path'])

        execute(command)

        print('[vlc] tracklist length is', length)
    else:  # PLAYING_MODE = 'shell'
        instance = vlc.Instance()
        players = {
            0: instance.media_player_new(),
            1: instance.media_player_new(),
        }

        print('[rolabesti] tracklist length is', length)

        for i, track in enumerate(tracks):
            if i == 0 and count > 1:
                print('[rolabesti] enqueuing %d track%s' % (count - 1, 's'[count - 1 == 1:]))
                print('[rolabesti] ----- ENQUEUED TRACKS -----')

                for track in tracks[1:]:
                    print('           ', track_to_string(track))

                print('[rolabesti] ---------------------------')

            print('[rolabesti] playing :', track_to_string(track))

            media = instance.media_new(track['path'])
            players[i % 2].set_media(media)
            players[i % 2].play()

            sleep(int(track['length']) - OVERLAP_LENGTH)  # Stop running until the next track begins
