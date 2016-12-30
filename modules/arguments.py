#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
from os.path import exists

from settings import METHOD, SORTING, TOTAL_LENGTH, MIN_TRACK_LENGTH, MAX_TRACK_LENGTH

METHODS = ('build', 'play', 'copy', 'list', 'tag')
SORTINGS = ('asc', 'desc', 'random')


def get_arguments():
    parser = argparse.ArgumentParser(description='command-line program to manage a music library')

    parser.add_argument('-m', '--method', help='method to run, default is %s' % METHOD, choices=METHODS, default=METHOD)
    parser.add_argument('-s', '--sorting', help='tracklist sorting, default is %s' % SORTING, choices=SORTINGS, default=SORTING)
    parser.add_argument('-t', '--total_length', help='maximum tracklist length in minutes, default is %s' % TOTAL_LENGTH, type=int, default=TOTAL_LENGTH)
    parser.add_argument('--min', help='minimum track length in minutes, default is %s' % MIN_TRACK_LENGTH, type=int, default=MIN_TRACK_LENGTH)
    parser.add_argument('--max', help='maximum track length in minutes, default is %s' % MAX_TRACK_LENGTH, type=int, default=MAX_TRACK_LENGTH)
    parser.add_argument('-p', '--place', help='track place')
    parser.add_argument('-g', '--genre', help='track genre')
    parser.add_argument('-ar', '--artist', help='track artist')
    parser.add_argument('-al', '--album', help='track album')
    parser.add_argument('-d', '--destiny', help='directory to copy tracks, required if method is copy')

    parsed_args = parser.parse_args()

    check_arguments(parsed_args)

    if parsed_args.max > parsed_args.total_length:
        parsed_args.max = parsed_args.total_length

    arguments = {}
    arguments['method'] = parsed_args.method
    arguments['sorting'] = parsed_args.sorting
    arguments['total_length'] = parsed_args.total_length * 60
    arguments['min'] = parsed_args.min * 60
    arguments['max'] = parsed_args.max * 60

    if parsed_args.place:
        arguments['place'] = parsed_args.place

    if parsed_args.genre:
        arguments['genre'] = parsed_args.genre

    if parsed_args.artist:
        arguments['artist'] = parsed_args.artist

    if parsed_args.album:
        arguments['album'] = parsed_args.album

    if parsed_args.destiny:
        arguments['destiny'] = parsed_args.destiny

    return arguments


def check_arguments(arguments):
    """
    Exit with error if invalid arguments.
    """
    if arguments.total_length <= 0:
        error = '[arguments] error | invalid argument | '
        error += 'total_length must be a positive integer'
        sys.exit(error)

    if arguments.min < 0:
        error = '[arguments] error | invalid argument | '
        error += 'min must be a non-negative integer'
        sys.exit(error)

    if arguments.max <= 0:
        error = '[arguments] error | invalid argument | '
        error += 'max must be a positive integer'
        sys.exit(error)

    if arguments.min > arguments.max:
        error = '[arguments] error | invalid arguments | '
        error += 'max must be greater than or equal to min'
        sys.exit(error)

    if arguments.method == 'copy':
        if not arguments.destiny:
            error = '[arguments] error | missing argument | '
            error += 'destiny is required with copy method'
            sys.exit(error)

        if not exists(arguments.destiny):
            error = '[arguments] error | invalid argument | '
            error += 'destiny must be an existing directory'
            sys.exit(error)
