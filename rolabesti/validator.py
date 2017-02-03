# -*- coding: utf-8 -*-
"""
rolabesti.validator
~~~~~~~~~~~~~~~~~~~

This module contains validation related functionality.
"""

from os.path import exists
import sys

from .conf import settings
from .sorter import SORTINGS
from .player import MAXIMUM_OVERLAP_LENGTH, MINIMUM_OVERLAP_LENGTH, PLAYERS


def get_value(variable):
    """Return its value if variable is defined in settings. Otherwise, exit with error."""
    try:
        return getattr(settings, variable)
    except AttributeError:
        error = '[rolabesti] error : missing settings : {} should be defined'.format(variable)
        sys.exit(error)


def validate_settings():
    """Exit with error if there are invalid settings."""
    max_tracklist_length = get_value('MAX_TRACKLIST_LENGTH')
    max_track_length = get_value('MAX_TRACK_LENGTH')
    min_track_length = get_value('MIN_TRACK_LENGTH')

    if not('int' in str(type(max_tracklist_length)) and max_tracklist_length >= 0):
        error = '[rolabesti] error : invalid settings : '
        error += 'MAX_TRACKLIST_LENGTH should be a non negative integer'
        sys.exit(error)

    if not('int' in str(type(min_track_length)) and min_track_length >= 0):
        error = '[rolabesti] error : invalid settings : '
        error += 'MIN_TRACK_LENGTH should be a non-negative integer'
        sys.exit(error)

    if not('int' in str(type(max_track_length)) and max_track_length > 0):
        error = '[rolabesti] error : invalid settings : '
        error += 'MAX_TRACK_LENGTH should be a positive integer'
        sys.exit(error)

    if min_track_length > max_track_length:
        error = '[rolabesti] error : invalid settings : '
        error += 'MAX_TRACK_LENGTH should be greater than or equal to MIN_TRACK_LENGTH'
        sys.exit(error)

    if max_track_length > max_tracklist_length:
        error = '[rolabesti] error : invalid settings : '
        error += 'MAX_TRACKLIST_LENGTH should be greater than or equal to MAX_TRACK_LENGTH'
        sys.exit(error)

    player = get_value('PLAYER')

    if player not in PLAYERS:
        error = '[rolabesti] error : invalid settings : PLAYER should be a valid value : {}'.format(', '.join(PLAYERS))
        sys.exit(error)

    sorting = get_value('SORTING')

    if sorting not in SORTINGS:
        error = '[rolabesti] error : invalid settings : SORTING should have a valid value : {}'.format(', '.join(SORTINGS))
        sys.exit(error)

    overlap_length = get_value('OVERLAP_LENGTH')

    if not('int' in str(type(overlap_length)) and MINIMUM_OVERLAP_LENGTH <= overlap_length <= MAXIMUM_OVERLAP_LENGTH):
        error = '[rolabesti] error : invalid settings : OVERLAP_LENGTH should be an integer between {} and {}'.format(MINIMUM_OVERLAP_LENGTH, MAXIMUM_OVERLAP_LENGTH)
        sys.exit(error)

    directory = get_value('MUSIC_DIR')

    if not exists(directory):
        error = '[rolabesti] error : invalid settings : MUSIC_DIR should be an existing directory'
        sys.exit(error)
