#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os.path import exists, join
import sys

from .arguments import METHODS, SORTINGS

PLAYING_MODES = ('shell', 'vlc')
MINIMUM_OVERLAP_LENGTH = 0
MAXIMUM_OVERLAP_LENGTH = 30


def check_existence(directory):
    """
    Exit with error if directory does not exist.
    """
    if not exists(directory):
        error = '[rolabesti] error | invalid settings | '
        error += '%s must be an existing directory' % directory
        sys.exit(error)


def check_definition(variable):
    """
    Return its value if variable is defined in settings,
    exit with error otherwise.
    """
    code = 'from settings import %s' % variable

    try:
        exec(code)
    except ImportError:
        error = '[rolabesti] error | missing settings | '
        error += '%s must be defined' % variable
        sys.exit(error)

    return locals()[variable]


def check_settings():
    """
    Check if the settings are valid
    """
    directories = ['BASE_DIR', 'LOG_DIR', 'MUSIC_DIR']

    for directory in directories:
        directory = check_definition(directory)

        check_existence(directory)

    method = check_definition('METHOD')

    if method not in METHODS:
        error = '[rolabesti] error | invalid settings | '
        error += 'METHOD must have a valid value : %s' % ', '.join(METHODS)
        sys.exit(error)

    sorting = check_definition('SORTING')

    if sorting not in SORTINGS:
        error = '[rolabesti] error | invalid settings | '
        error += 'SORTING must have a valid value : %s' % ', '.join(SORTINGS)
        sys.exit(error)

    total_length = check_definition('TOTAL_LENGTH')
    min_track_length = check_definition('MIN_TRACK_LENGTH')
    max_track_length = check_definition('MAX_TRACK_LENGTH')

    if not('int' in str(type(total_length)) and total_length > 0):
        error = '[rolabesti] error | invalid settings | '
        error += 'TOTAL_LENGTH must be a positive integer'
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

    if max_track_length > total_length:
        error = '[rolabesti] error | invalid settings | '
        error += 'TOTAL_LENGTH must be greater than or equal to MAX_TRACK_LENGTH'
        sys.exit(error)

    playing_mode = check_definition('PLAYING_MODE')

    if playing_mode not in PLAYING_MODES:
        error = '[rolabesti] error | invalid settings | '
        error += 'PLAYING_MODE must have a valid value : %s' % ', '.join(PLAYING_MODES)
        sys.exit(error)

    overlap_length = check_definition('OVERLAP_LENGTH')

    if not('int' in str(type(overlap_length)) and MINIMUM_OVERLAP_LENGTH <= overlap_length <= MAXIMUM_OVERLAP_LENGTH):
        error = '[rolabesti] error | invalid settings | '
        error += 'OVERLAP_LENGTH must have a valid value : integer in the range '
        error += '[%s, %s]' % (MINIMUM_OVERLAP_LENGTH, MAXIMUM_OVERLAP_LENGTH)
        sys.exit(error)
