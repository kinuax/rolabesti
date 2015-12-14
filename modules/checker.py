#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import exists
import sys
from sorter import SORTINGS


def check_definition(variable):
    """
    Return its value if variable is defined in settings,
    exit with error otherwise.
    """
    code = 'from settings import %s' % variable

    try:
        exec code
    except ImportError:
        error = '[checker] error | invalid settings | '
        error += '%s must be defined' % variable
        sys.exit(error)

    return locals()[variable]


def check_existence(directory):
    """
    Exit with error if directory does not exist.
    """
    if not exists(directory):
        error = '[checker] error | invalid settings | '
        error += '%s must be an existing directory' % directory
        sys.exit(error)


def check_settings():
    """
    Check if the settings are valid
    """
    directories = ['BASE_DIR', 'DB_DIR', 'LOG_DIR', 'MUSIC_DIR']

    for directory in directories:
        directory = check_definition(directory)

        check_existence(directory)

    sorting = check_definition('SORTING')

    if sorting not in SORTINGS:
        error = '[checker] error | invalid settings | '
        error += 'SORTING must have a valid value'
        sys.exit(error)

    total_length = check_definition('TOTAL_LENGTH')
    min_track_length = check_definition('MIN_TRACK_LENGTH')
    max_track_length = check_definition('MAX_TRACK_LENGTH')

    if not('int' in str(type(total_length)) and total_length > 0):
        error = '[checker] error | invalid settings | '
        error += 'TOTAL_LENGTH must be a positive integer'
        sys.exit(error)

    if not('int' in str(type(min_track_length)) and min_track_length >= 0):
        error = '[checker] error | invalid settings | '
        error += 'MIN_TRACK_LENGTH must be a non-negative integer'
        sys.exit(error)

    if not('int' in str(type(max_track_length)) and max_track_length > 0):
        error = '[checker] error | invalid settings | '
        error += 'MAX_TRACK_LENGTH must be a positive integer'
        sys.exit(error)

    if min_track_length > max_track_length:
        error = '[checker] error | invalid settings | '
        error += 'MAX_TRACK_LENGTH must be greater than or equal to MIN_TRACK_LENGTH'
        sys.exit(error)

    if max_track_length > total_length:
        error = '[checker] error | invalid settings | '
        error += 'TOTAL_LENGTH must be greater than or equal to MAX_TRACK_LENGTH'
        sys.exit(error)


def check_arguments(arguments):
    """
    Check if the arguments are valid
    """
    if arguments.total_length <= 0:
        error = '[checker] error | invalid argument | '
        error += 'total_length must be a positive integer'
        sys.exit(error)

    if arguments.min < 0:
        error = '[checker] error | invalid argument | '
        error += 'min must be a non-negative integer'
        sys.exit(error)

    if arguments.max <= 0:
        error = '[checker] error | invalid argument | '
        error += 'max must be a positive integer'
        sys.exit(error)

    if arguments.min > arguments.max:
        error = '[checker] error | invalid arguments | '
        error += 'max must be greater than or equal to min'
        sys.exit(error)

    if arguments.max > arguments.total_length:
        error = '[checker] error | invalid arguments | '
        error += 'total_length must be greater than or equal to max'
        sys.exit(error)

    if arguments.method == 'copy':
        if not arguments.destiny:
            error = '[checker] error | missing argument | '
            error += 'destiny is required with copy method'
            sys.exit(error)

        if not exists(arguments.destiny.decode('utf-8')):
            error = '[checker] error | invalid argument | '
            error += 'destiny must be an existing directory'
            sys.exit(error)
