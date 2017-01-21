# -*- coding: utf-8 -*-

import codecs
import json
import logging
from os import remove, walk
from os.path import basename, join, splitext
import subprocess
import sys

from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.id3._util import ID3NoHeaderError

from settings import LOG_DIR


def dump_to_json(obj, filepath):
    with codecs.open(filepath, 'w', 'utf-8') as file:
        json.dump(obj, file, ensure_ascii=False)


def load_from_json(filepath):
    with open(filepath) as file:
        for obj in json.load(file):
            yield obj


def get_length(trackpath):
    logger = get_logger(__file__)

    try:
        return MP3(trackpath).info.length
    except:
        error = sys.exc_info()
        error = 'getting length | %s - %s | %s' % (str(error[0]), str(error[1]), trackpath)
        logger.error(error)


def get_tags(trackpath):
    logger = get_logger(__file__)

    try:
        return EasyID3(trackpath)
    except ID3NoHeaderError:
        EasyID3().save(trackpath)
        return EasyID3(trackpath)
    except:
        error = sys.exc_info()
        error = 'getting tags | %s - %s | %s' % (str(error[0]), str(error[1]), trackpath)
        logger.error(error)


def get_tag(trackpath, tagname):
    tags = get_tags(trackpath)

    if not tags:
        return None
    elif tagname in tags and len(tags[tagname]) and tags[tagname][0]:
        return tags[tagname][0]
    else:
        return ''


def get_logger(file):
    name = splitext(basename(file))[0]
    logger = logging.getLogger(name)

    if not len(logger.handlers):
        logger.setLevel(logging.INFO)
        logpath = join(LOG_DIR, '{}.log'.format(name))
        handler = logging.FileHandler(logpath, encoding='utf-8')
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def clean_repo(directory):
    """Remove *.pyc files from directory."""
    filepaths = []

    for dirpath, dirnames, filenames in walk(directory):
        filepaths.extend([join(dirpath, filename).decode('utf-8') for filename
                         in filenames if filename.endswith('.pyc')])

    map(remove, filepaths)

    print('repository cleaned')


def format_length(length):
    """Return formatted length."""
    length = int(length)

    if length < 3600:
        minutes = length // 60
        seconds = length % 60

        return '%s:%s' % (format(minutes, '02'), format(seconds, '02'))
    else:
        hours = length // 3600
        minutes = (length % 3600) // 60
        seconds = (length % 3600) % 60

        return '%d:%s:%s' % (hours, format(minutes, '02'), format(seconds, '02'))


def execute(command, shell=False, background=True):
    """Execute command.

    Return (output, error) tuple if background is False. Otherwise, return None.
    """
    process = subprocess.Popen(command,
                               shell=shell,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    if not background:
        return process.communicate()


def is_running(process):
    """Return True if process is running. Otherwise, return False."""
    command = 'ps -A | grep %s' % process
    (output, error) = execute(command, shell=True, background=False)

    return True if output else False
