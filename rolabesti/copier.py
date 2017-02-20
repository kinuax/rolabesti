# -*- coding: utf-8 -*-

from .utils import execute


def copy(tracks, directory):
    print('[copier] copying {} track{} to {}'.format(len(tracks), 's'[len(tracks) == 1:], directory))

    command = ['cp'] + [track['path'] for track in tracks] + [directory]
    execute(command, background=False)

    print('[copier] {} track{} copied'.format(len(tracks), 's'[len(tracks) == 1:]))
