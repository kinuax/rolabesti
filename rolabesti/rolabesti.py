#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from checker import check_settings
check_settings()

from arguments import parse_arguments, validate_arguments
from copier import copy
from database import load, search
from limiter import limit
from displayer import display
from player import play
from sorter import sort
from tagger import tag


if __name__ == '__main__':
    arguments = parse_arguments()
    subcommand = arguments['subcommand']

    if subcommand == 'load':
        load()
    else:
        validate_arguments(arguments)
        tracks, length = search(arguments)

        if tracks:
            if subcommand == 'search':
                display(tracks, length)
            elif subcommand == 'tag':
                tag(tracks)
            else:  # subcommand is play or copy
                tracks = sort(tracks, arguments['sorting'])
                tracks, length = limit(tracks, arguments['max_tracklist_length'])
                display(tracks, length)

                if subcommand == 'play':
                    play(tracks, length)
                else:
                    copy(tracks, length, arguments['destiny'])
