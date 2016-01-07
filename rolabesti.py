#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modules.checker import check_settings
check_settings()

from modules.arguments import get_arguments
from modules.copier import copy
from modules.database import build_index, search, check_empty_database
from modules.limiter import limit
from modules.lister import list_tracks
from modules.player import play
from modules.sorter import sort
from modules.tagger import tag


if __name__ == '__main__':
    arguments = get_arguments()
    method = arguments['method']

    if method == 'build':
        build_index()
    else:
        check_empty_database()

        tracks = search(arguments)

        if tracks:
            if method == 'list':
                list_tracks(tracks)
            elif method == 'tag':
                tag(tracks)
            else:
                tracks = sort(tracks, arguments['sorting'])
                tracks, length = limit(tracks, arguments['total_length'])

                if method == 'play':
                    play(tracks, length)
                else:
                    copy(tracks, length, arguments['destiny'])
