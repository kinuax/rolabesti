# -*- coding: utf-8 -*-
"""
rolabesti.utils
~~~~~~~~~~~~~~~

This module contains some utility functions.
"""

from logging import getLogger
import subprocess
import sys

from mutagen.easyid3 import EasyID3
from mutagen.id3._util import ID3NoHeaderError
from mutagen.mp3 import MP3

from .constants import ID3_TAGS, TRACK_FIELDS


def get_length(trackpath):
    """Return the length of the track located at trackpath in integer seconds.

    If there is an error retrieving the length, log the error and return None.
    """
    try:
        return int(MP3(trackpath).info.length)
    except:
        error = sys.exc_info()
        error = 'getting length | {} - {} | {}'.format(str(error[0]), str(error[1]), trackpath)
        getLogger(__name__).error(error)


def get_id3_obj(trackpath):
    """Return an instance of mutagen.easyid3.EasyID3 (dictionary-like object)
    defined by the track located at trackpath.

    If there is an error while instantiating, log the error and return an empty dictionary.
    """
    try:
        return EasyID3(trackpath)
    except ID3NoHeaderError:
        EasyID3().save(trackpath)
        return EasyID3(trackpath)
    except:
        error = sys.exc_info()
        error = 'getting EasyID3 | {} - {} | {}'.format(str(error[0]), str(error[1]), trackpath)
        getLogger(__name__).error(error)
        return {}


def get_id3_tags(trackpath):
    """Return a dictionary with the ID3 tags of the track located at trackpath.

    The tags are limited to ID3_TAGS.

    If there is no tag to retrieve, return an empty dictionary.
    """
    tags = {}
    id3 = get_id3_obj(trackpath)

    for tag in set.intersection(set(id3), set(ID3_TAGS)):
        if id3[tag] and id3[tag][0].strip():
            tags[tag] = id3[tag][0].strip()

    return tags


def add_prefix_to_dict(dictionary, prefix):
    """Return a modified dictionary with keys prefixed by prefix."""
    return {'{}_{}'.format(prefix, key): value for key, value in dictionary.items()}


def format_length(length):
    """Return length in the format MM:SS or HH:MM:SS."""
    length = int(length)

    if length < 3600:
        minutes = length // 60
        seconds = length % 60

        return '{}:{}'.format(format(minutes, '02'), format(seconds, '02'))
    else:
        hours = length // 3600
        minutes = (length % 3600) // 60
        seconds = (length % 3600) % 60

        return '{}:{}:{}'.format(hours, format(minutes, '02'), format(seconds, '02'))


def track_to_string(track):
    """Convert track into a string."""
    string = []

    for field_id, fields in TRACK_FIELDS.items():
        for field in fields:
            if field in track:
                string.append('{} = {}'.format(field_id.capitalize(), track[field]))

                break

    string.append('Length = ' + format_length(track['length']))

    return ' | '.join(string)


def execute(command, shell=False, background=True):
    """Execute command.

    Return an (output, error) tuple if background is False. Otherwise, return None.

    If shell is True, command should be a string.
    If shell is False, command should be a list of strings.
    """
    process = subprocess.Popen(command,
                               shell=shell,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    if not background:
        return process.communicate()


def is_running(process):
    """Return True if process is running. Otherwise, return False."""
    command = 'ps -A | grep {}'.format(process)
    output, error = execute(command, shell=True, background=False)

    return bool(output)
