#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from checker import check_settings
check_settings()

from arguments import parse_arguments, prepare_arguments, validate_arguments
from copier import copy
from displayer import display
from mongo import load, search
from player import play
from slicer import slice_tracks
from sorter import sort
from tagger import tag


if __name__ == '__main__':
    arguments = parse_arguments()
    subcommand = arguments['subcommand']

    if subcommand == 'load':
        load()
    else:
        validate_arguments(arguments)
        prepare_arguments(arguments)
        tracks, length = search(arguments)

        if tracks:
            if subcommand == 'search':
                display(tracks, length)
            elif subcommand == 'tag':
                tag(tracks)
            else:  # subcommand is play or copy
                tracks = sort(tracks, arguments['sorting'])

                if arguments['max_tracklist_length'] > 0:
                    tracks, length = slice_tracks(tracks, arguments['max_tracklist_length'])

                display(tracks, length)

                if subcommand == 'play':
                    play(tracks, arguments['player'])
                else:
                    copy(tracks, arguments['destiny'])
