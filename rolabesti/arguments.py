#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from os.path import exists
import sys

from settings import SORTING, TOTAL_LENGTH, MIN_TRACK_LENGTH, MAX_TRACK_LENGTH
from sorter import SORTINGS


def get_arguments():
    root_parser = argparse.ArgumentParser(description='Application to manage a music library.')
    subparsers = root_parser.add_subparsers(title='subcommands', dest='subcommand')
    subparsers.required = True
    play_parser = subparsers.add_parser('play', help='play and enqueue tracks')
    search_parser = subparsers.add_parser('search', help='search and output tracks')
    subparsers.add_parser('load', help='parse and load tracks to the database')
    copy_parser = subparsers.add_parser('copy', help='copy tracks to destiny')
    tag_parser = subparsers.add_parser('tag', help='tag tracks')

    for parser in [play_parser, search_parser, copy_parser, tag_parser]:
        parser.add_argument('-ar', '--artist', help='track artist')
        parser.add_argument('-al', '--album', help='track album')
        parser.add_argument('-g', '--genre', help='track genre')
        parser.add_argument('-p', '--place', help='track place')
        parser.add_argument('-t', '--total_length', type=int, default=TOTAL_LENGTH, help='maximum tracklist length in minutes, default is %s' % TOTAL_LENGTH)
        parser.add_argument('--min', type=int, default=MIN_TRACK_LENGTH, help='minimum track length in minutes, default is %s' % MIN_TRACK_LENGTH)
        parser.add_argument('--max', type=int, default=MAX_TRACK_LENGTH, help='maximum track length in minutes, default is %s' % MAX_TRACK_LENGTH)
        parser.add_argument('-s', '--sorting', choices=SORTINGS, default=SORTING, help='tracklist sorting, default is %s' % SORTING)

    copy_parser.add_argument('-d', '--destiny', required=True, help='directory to copy tracks, required')
    parsed_args = root_parser.parse_args()

    check_arguments(parsed_args)

    if parsed_args.max > parsed_args.total_length:
        parsed_args.max = parsed_args.total_length

    arguments = {}
    arguments['subcommand'] = parsed_args.subcommand
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

    if parsed_args.subcommand == 'copy':
        arguments['destiny'] = parsed_args.destiny

    return arguments


def check_arguments(arguments):
    """Exit with error if there are invalid arguments. Otherwise, return None."""
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

    if arguments.subcommand == 'copy':
        if not arguments.destiny:
            error = '[arguments] error | missing argument | '
            error += 'destiny is required with copy method'
            sys.exit(error)

        if not exists(arguments.destiny):
            error = '[arguments] error | invalid argument | '
            error += 'destiny must be an existing directory'
            sys.exit(error)
