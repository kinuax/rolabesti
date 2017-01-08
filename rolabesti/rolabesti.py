#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from checker import check_settings
check_settings()

from arguments import parse_arguments, validate_arguments
from copier import copy
from database import load, search, is_database_empty
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

        tracks = search(arguments)

        if tracks:
            if subcommand == 'search':
                print_tracks(tracks)
            elif subcommand == 'tag':
                tag(tracks)
            else:  # subcommand is play or copy
                tracks = sort(tracks, arguments['sorting'])
                tracks, length = limit(tracks, arguments['max_tracklist_length'])

                if subcommand == 'play':
                    play(tracks, length)
                else:
                    copy(tracks, length, arguments['destiny'])
        elif is_database_empty():
            print('[rolabesti] there is no track in the database, load subcommand should be run first')
