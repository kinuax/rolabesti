#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import codecs
import json


def dump_to_json(obj, filepath):
    with codecs.open(filepath, 'w', 'utf-8') as file:
        json.dump(obj, file, ensure_ascii=False)


def load_from_json(filepath):
    with open(filepath) as file:
        for obj in json.load(file):
            yield obj
