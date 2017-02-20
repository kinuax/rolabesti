# -*- coding: utf-8 -*-

import logging
import sys

from .arguments import parse_arguments, prepare_arguments, validate_arguments
from .copier import copy
from .displayer import display
from .mongo import load, search
from .player import play
from .slicer import slice_tracks
from .sorter import sort
from .tagger import tag
from .validator import validate_settings


def main(args=sys.argv[1:]):
    """Entrypoint to the rolabesti command."""
    validate_settings()
    arguments = parse_arguments()
    logger = logging.getLogger()

    if arguments['log']:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    else:
        logger.addHandler(logging.NullHandler())

    subcommand = arguments['subcommand']

    if subcommand == 'load':
        load(arguments['music_dir'])
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
                    copy(tracks, arguments['directory'])


if __name__ == '__main__':
    main()
