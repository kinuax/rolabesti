#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys

from checker import check_arguments
from settings import SORTING, TOTAL_LENGTH, MIN_TRACK_LENGTH, MAX_TRACK_LENGTH
from sorter import SORTINGS

METHODS = ('build', 'play', 'copy', 'list')


def get_arguments():
    parser = argparse.ArgumentParser(description='command-line program to manage a music library')

    parser.add_argument('-m', '--method', help='method to run, default is play', choices=METHODS, default='play')
    parser.add_argument('-s', '--sorting', help='track sorting, default is %s' % SORTING, choices=SORTINGS, default=SORTING)
    parser.add_argument('-t', '--total_length', help='maximum track list length in minutes, default is %s' % TOTAL_LENGTH, type=int, default=TOTAL_LENGTH)
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
    arguments['method'] = parsed_args.method.decode('utf-8')
    arguments['sorting'] = parsed_args.sorting.decode('utf-8')
    arguments['total_length'] = parsed_args.total_length * 60
    arguments['min'] = parsed_args.min * 60
    arguments['max'] = parsed_args.max * 60

    if parsed_args.place:
        arguments['place'] = parsed_args.place.decode('utf-8')

    if parsed_args.genre:
        arguments['genre'] = parsed_args.genre.decode('utf-8')

    if parsed_args.artist:
        arguments['artist'] = parsed_args.artist.decode('utf-8')

    if parsed_args.album:
        arguments['album'] = parsed_args.album.decode('utf-8')

    if parsed_args.destiny:
        arguments['destiny'] = parsed_args.destiny.decode('utf-8')

    return arguments
