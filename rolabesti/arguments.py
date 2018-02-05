# -*- coding: utf-8 -*-
"""
rolabesti.arguments
~~~~~~~~~~~~~~~~~~~

This module contains the functionality related to the user arguments.
"""

import argparse
import os
from os.path import isdir
import sys

from . import __description__, __version__
from .conf.settings import MAX_TRACKLIST_LENGTH, MAX_TRACK_LENGTH, MIN_TRACK_LENGTH, MUSIC_DIR, OVERLAP_LENGTH, PLAYER, SORTING
from .constants import ID3_TAGS
from .player import MAXIMUM_OVERLAP_LENGTH, MINIMUM_OVERLAP_LENGTH, PLAYERS
from .sorter import SORTINGS


def parse_arguments():
    """Parse command-line arguments and return them in a dictionary.

    If no argument is given, show help message and exit. If there is an invalid argument, show error message and exit.
    """
    root_parser = argparse.ArgumentParser(description=__description__)
    root_parser.add_argument('-v', '--version', action='version', version='%(prog)s {}'.format(__version__))
    subparsers = root_parser.add_subparsers(title='subcommands', dest='subcommand')
    subparsers.required = True
    play_parser = subparsers.add_parser('play', help='play and enqueue tracks')
    search_parser = subparsers.add_parser('search', help='search and display tracks')
    load_parser = subparsers.add_parser('load', help='parse and load tracks from a directory to the database')
    copy_parser = subparsers.add_parser('copy', help='copy tracks to a directory')
    tag_parser = subparsers.add_parser('tag', help='update ID3 tags with parsed values')

    if len(sys.argv) == 1:
        root_parser.print_help()
        sys.exit(1)

    for parser in [play_parser, search_parser, load_parser, copy_parser, tag_parser]:
        parser.add_argument('--log', action='store_true', help='enable logging')

    for parser in [play_parser, search_parser, copy_parser, tag_parser]:
        parser.add_argument('-ar', '--artist', type=str, help='track artist')
        parser.add_argument('-t', '--title', type=str, help='track title')
        parser.add_argument('-al', '--album', type=str, help='track album')
        parser.add_argument('-g', '--genre', type=str, help='track genre')
        parser.add_argument('-p', '--place', type=str, help='track place')
        parser.add_argument('--max', type=non_negative_integer, default=MAX_TRACK_LENGTH, help='maximum track length in minutes, 0 denotes no maximum track length, default is {}'.format(MAX_TRACK_LENGTH))
        parser.add_argument('--min', type=non_negative_integer, default=MIN_TRACK_LENGTH, help='minimum track length in minutes, 0 denotes no minimum track length, default is {}'.format(MIN_TRACK_LENGTH))

    for parser in [play_parser, copy_parser]:
        parser.add_argument('-l', '--max_tracklist_length', type=non_negative_integer, default=MAX_TRACKLIST_LENGTH,
                            help='maximum tracklist length in minutes, 0 denotes no maximum tracklist length, default is {}'.format(MAX_TRACKLIST_LENGTH))
        parser.add_argument('-s', '--sorting', choices=SORTINGS, default=SORTING, help='tracklist sorting, default is {}'.format(SORTING))

    play_parser.add_argument('--player', choices=PLAYERS, default=PLAYER, help='player to play and enqueue tracks, default is {}'.format(PLAYER))
    play_parser.add_argument('-o', '--overlap_length', type=overlap_length, default=OVERLAP_LENGTH,
                             help='with shell player, overlap length in seconds between two consecutive tracks, minimum is {}, maximum is {}, default is {}'.format(MINIMUM_OVERLAP_LENGTH, MAXIMUM_OVERLAP_LENGTH, OVERLAP_LENGTH))
    load_parser.add_argument('-d', '--music_dir', type=readable_directory, default=MUSIC_DIR, help='path where the mp3 files are located, default is {}'.format(MUSIC_DIR))
    copy_parser.add_argument('-d', '--directory', type=writable_directory, default=os.getcwd(), help='path where the tracks will be copied, default is current directory {}'.format(os.getcwd()))
    tag_parser.add_argument('--id3_tag', choices=ID3_TAGS, required=True, help='ID3 tag to be updated with corresponding parsed value, required')

    parsed_args = root_parser.parse_args()

    return {key: value for key, value in vars(parsed_args).items() if value is not None}


def integer(arg, error='should be an integer'):
    try:
        return int(arg)
    except ValueError:
        raise argparse.ArgumentTypeError(error)


def non_negative_integer(arg):
    error = 'should be a non negative integer'
    arg = integer(arg, error)

    if arg < 0:
        raise argparse.ArgumentTypeError(error)

    return arg


def positive_integer(arg):
    error = 'should be a positive integer'
    arg = integer(arg, error)

    if arg <= 0:
        raise argparse.ArgumentTypeError(error)

    return arg


def overlap_length(arg):
    error = 'should be an integer between {} and {}'.format(MINIMUM_OVERLAP_LENGTH, MAXIMUM_OVERLAP_LENGTH)
    arg = integer(arg, error)

    if not(MINIMUM_OVERLAP_LENGTH <= arg <= MAXIMUM_OVERLAP_LENGTH):
        raise argparse.ArgumentTypeError(error)

    return arg


def existing_directory(arg):
    if not isdir(arg):
        raise argparse.ArgumentTypeError('should be an existing directory')

    return arg


def readable_directory(arg):
    existing_directory(arg)

    if not os.access(arg, os.R_OK):
        raise argparse.ArgumentTypeError('should be readable for the current user')

    return arg


def writable_directory(arg):
    existing_directory(arg)

    if not os.access(arg, os.R_OK):
        raise argparse.ArgumentTypeError('should be writable for the current user')

    return arg


def validate_arguments(arguments):
    """Exit with error if there are invalid arguments."""
    if 0 < arguments['max'] < arguments['min']:
        error = '[rolabesti] error : invalid arguments : '
        error += 'max must be greater than or equal to min'
        sys.exit(error)


def prepare_arguments(arguments):
    """Set proper maximum track length. Convert length arguments to seconds."""
    if 'max_tracklist_length' in arguments:
        if 0 < arguments['max_tracklist_length'] < arguments['max']:
            arguments['max'] = arguments['max_tracklist_length']

        arguments['max_tracklist_length'] *= 60

    arguments['max'] *= 60
    arguments['min'] *= 60
