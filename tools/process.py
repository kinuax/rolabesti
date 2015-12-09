#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess


def execute(command, shell=False, background=True):
    """
    Execute command.

    Return (output, error) tuple if background=False, None otherwise
    """
    process = subprocess.Popen(command,
                               shell=shell,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    if not background:
        return process.communicate()


def running_process(process):
    """
    Return True if process is running, False otherwise
    """
    command = 'ps -A | grep %s' % process
    (output, error) = execute(command, shell=True, background=False)

    if output:
        return True
    else:
        return False
