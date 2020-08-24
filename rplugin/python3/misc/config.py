#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

base_path = '~/.local/share/nvim/plugged/misc.nvim'
#base_path = '~/workspace/github/sources/misc.nvim'  # or your local path


try:
    from .local_config import *  # noqa
except ImportError:
    pass


base_path = os.path.expanduser(base_path)
log_path = os.path.join(base_path, 'debug.log')
module_path = os.path.join(base_path, 'rplugin/python3/misc')
