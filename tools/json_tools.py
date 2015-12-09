#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import json


def dump_to_json(obj, filepath):
    with codecs.open(filepath, 'w', 'utf-8') as file:
        json.dump(obj, file, ensure_ascii=False, indent=4, sort_keys=True)


def load_from_json(filepath):
    with open(filepath) as file:
        obj = json.load(file)

    return obj
