#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from checker import check_settings
check_settings()

from arguments import parse_arguments, validate_arguments
from copier import copy
from database import load, search, check_existing_tracks
from limiter import limit
from player import play
from printer import print_tracks
from sorter import sort
from tagger import tag


if __name__ == '__main__':
    arguments = parse_arguments()
    subcommand = arguments['subcommand']

    if subcommand == 'load':
        load()
    else:
        validate_arguments(arguments)

        check_existing_tracks()

        tracks = search(arguments)

        if tracks:
            if subcommand == 'search':
                print_tracks(tracks)
            elif subcommand == 'tag':
                tag(tracks)
            else:  # subcommand is play or copy
                tracks = sort(tracks, arguments['sorting'])
                tracks, length = limit(tracks, arguments['total_length'])

                if subcommand == 'play':
                    play(tracks, length)
                else:
                    copy(tracks, length, arguments['destiny'])
