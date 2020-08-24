#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys

common_delimiter = re.compile(r'\s*[,;，；]\s*')


def split(string):
    ones = common_delimiter.split(string)
    ones = [one for one in ones if one != '']
    return ones


def get_spaces_and_content(string):
    for index, char in enumerate(string):
        if char != ' ':
            break
    return string[:index], string[index:].strip()


def log_sys_path(logger):
    for pth in sys.path:
        logger.info(pth)
