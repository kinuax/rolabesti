# -*- coding: utf-8 -*-

from utils import execute


def copy(tracks, length, destiny):
    count = len(tracks)

    print('[copier] copying %d track%s to %s' % (count, 's'[count == 1:], destiny))

    command = ['cp']

    for track in tracks:
        command.append(track['path'])

    command.append(destiny)
    execute(command, background=False)

    print('[copier] length is', length)
