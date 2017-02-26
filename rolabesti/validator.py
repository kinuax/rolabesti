# -*- coding: utf-8 -*-
"""
rolabesti.validator
~~~~~~~~~~~~~~~~~~~

This module contains validation related functionality.
"""

import os
from os.path import isdir
import sys

from .conf import settings
from .player import MAXIMUM_OVERLAP_LENGTH, MINIMUM_OVERLAP_LENGTH, PLAYERS
from .sorter import SORTINGS


def get_value(variable):
    """Return its value if variable is defined in settings. Otherwise, show error message and exit."""
    try:
        return getattr(settings, variable)
    except AttributeError:
        error = '[rolabesti] error : missing setting : {} should be defined'.format(variable)
        sys.exit(error)


def validate_settings():
    """If there is an invalid setting, show error message and exit."""
    error = '[rolabesti] error : invalid setting : '
    max_tracklist_length = get_value('MAX_TRACKLIST_LENGTH')
    max_track_length = get_value('MAX_TRACK_LENGTH')
    min_track_length = get_value('MIN_TRACK_LENGTH')

    if not(type(max_tracklist_length) is int and max_tracklist_length >= 0):
        error += 'MAX_TRACKLIST_LENGTH should be a non negative integer'
        sys.exit(error)

    if not(type(max_track_length) is int and max_track_length >= 0):
        error += 'MAX_TRACK_LENGTH should be a non negative integer'
        sys.exit(error)

    if not(type(min_track_length) is int and min_track_length >= 0):
        error += 'MIN_TRACK_LENGTH should be a non negative integer'
        sys.exit(error)

    if 0 < max_track_length < min_track_length:
        error += 'MAX_TRACK_LENGTH should be greater than or equal to MIN_TRACK_LENGTH'
        sys.exit(error)

    if max_track_length > max_tracklist_length:
        error += 'MAX_TRACKLIST_LENGTH should be greater than or equal to MAX_TRACK_LENGTH'
        sys.exit(error)

    player = get_value('PLAYER')

    if player not in PLAYERS:
        error += 'PLAYER should be a valid value : {}'.format(', '.join(PLAYERS))
        sys.exit(error)

    sorting = get_value('SORTING')

    if sorting not in SORTINGS:
        error += 'SORTING should have a valid value : {}'.format(', '.join(SORTINGS))
        sys.exit(error)

    overlap_length = get_value('OVERLAP_LENGTH')

    if not(type(overlap_length) is int and MINIMUM_OVERLAP_LENGTH <= overlap_length <= MAXIMUM_OVERLAP_LENGTH):
        error += 'OVERLAP_LENGTH should be an integer between {} and {}'.format(MINIMUM_OVERLAP_LENGTH, MAXIMUM_OVERLAP_LENGTH)
        sys.exit(error)

    directory = get_value('MUSIC_DIR')

    if not isdir(directory):
        error += 'MUSIC_DIR should be an existing directory'
        sys.exit(error)
    elif not os.access(directory, os.R_OK):
        error += 'MUSIC_DIR should be readable for the current user'
        sys.exit(error)
