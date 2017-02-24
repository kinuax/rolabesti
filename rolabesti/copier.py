# -*- coding: utf-8 -*-
"""
rolabesti.copier
~~~~~~~~~~~~~~~~

This module contains the functionality to copy found tracks to some directory.
"""

from .utils import execute


def copy(tracks, directory):
    print('[rolabesti] copying {} track{} to {}'.format(len(tracks), 's'[len(tracks) == 1:], directory))

    command = ['cp'] + [track['path'] for track in tracks] + [directory]
    execute(command, background=False)

    print('[rolabesti] {} track{} copied'.format(len(tracks), 's'[len(tracks) == 1:]))
