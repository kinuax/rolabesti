# -*- coding: utf-8 -*-

from utils import execute


def copy(tracks, destiny):
    print('[copier] copying {} track{} to {}'.format(len(tracks), 's'[len(tracks) == 1:], destiny))

    command = ['cp'] + [track['path'] for track in tracks] + [destiny]
    execute(command, background=False)

    print('[copier] {} track{} copied'.format(len(tracks), 's'[len(tracks) == 1:]))
