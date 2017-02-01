# -*- coding: utf-8 -*-

from os.path import exists
import sys

from .sorter import SORTINGS

DIRECTORIES = ['BASE_DIR', 'LOG_DIR', 'MUSIC_DIR']
MINIMUM_OVERLAP_LENGTH = 0
MAXIMUM_OVERLAP_LENGTH = 30


def get_value(variable):
    """Return its value if variable is defined in settings. Otherwise, exit with error."""
    code = 'from settings import %s' % variable

    try:
        exec(code)
    except ImportError:
        error = '[rolabesti] error | missing settings | '
        error += '%s must be defined' % variable
        sys.exit(error)

    return locals()[variable]


def check_settings():
    """Check if the settings are valid."""
    for directory in DIRECTORIES:
        directory = get_value(directory)

        if not exists(directory):
            error = '[rolabesti] error | invalid settings | '
            error += '%s must be an existing directory' % directory
            sys.exit(error)

    sorting = get_value('SORTING')

    if sorting not in SORTINGS:
        error = '[rolabesti] error | invalid settings | '
        error += 'SORTING must have a valid value : %s' % ', '.join(SORTINGS)
        sys.exit(error)

    min_track_length = get_value('MIN_TRACK_LENGTH')
    max_track_length = get_value('MAX_TRACK_LENGTH')
    max_tracklist_length = get_value('MAX_TRACKLIST_LENGTH')

    if not('int' in str(type(max_tracklist_length)) and max_tracklist_length >= 0):
        error = '[rolabesti] error | invalid settings | '
        error += 'MAX_TRACKLIST_LENGTH must be a non negative integer'
        sys.exit(error)

    if not('int' in str(type(min_track_length)) and min_track_length >= 0):
        error = '[rolabesti] error | invalid settings | '
        error += 'MIN_TRACK_LENGTH must be a non-negative integer'
        sys.exit(error)

    if not('int' in str(type(max_track_length)) and max_track_length > 0):
        error = '[rolabesti] error | invalid settings | '
        error += 'MAX_TRACK_LENGTH must be a positive integer'
        sys.exit(error)

    if min_track_length > max_track_length:
        error = '[rolabesti] error | invalid settings | '
        error += 'MAX_TRACK_LENGTH must be greater than or equal to MIN_TRACK_LENGTH'
        sys.exit(error)

    if max_track_length > max_tracklist_length:
        error = '[rolabesti] error | invalid settings | '
        error += 'MAX_TRACKLIST_LENGTH must be greater than or equal to MAX_TRACK_LENGTH'
        sys.exit(error)

    overlap_length = get_value('OVERLAP_LENGTH')

    if not('int' in str(type(overlap_length)) and MINIMUM_OVERLAP_LENGTH <= overlap_length <= MAXIMUM_OVERLAP_LENGTH):
        error = '[rolabesti] error | invalid settings | '
        error += 'OVERLAP_LENGTH must have a valid value : integer in the range '
        error += '[%s, %s]' % (MINIMUM_OVERLAP_LENGTH, MAXIMUM_OVERLAP_LENGTH)
        sys.exit(error)
