#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from os.path import join

from settings import LOG_DIR


def get_logger(name):
    logger = logging.getLogger(name)

    if not len(logger.handlers):
        logger.setLevel(logging.INFO)
        logpath = join(LOG_DIR, '%s.log ' % name)
        handler = logging.FileHandler(logpath, encoding='utf-8')
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
