#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import neovim

from .utils import common
from .utils.log import logger

common.log_sys_path(logger)


class Base(object):
    def __init__(self, nvim: neovim.Nvim):
        self.nvim = nvim

    @property
    def window(self):
        return self.nvim.current.window

    @property
    def buffer(self):
        return self.nvim.current.buffer

    @property
    def line(self):
        return self.nvim.current.line

    @property
    def cursor(self):
        return self.window.cursor

    @property
    def row(self):
        # startswith 1
        return self.cursor[0]

    @property
    def col(self):
        # startswith 0
        return self.cursor[1]

    def get_char_before_cursor(self):
        row, col = self.window.cursor
        logger.deplus(f"{row}, {col}")
        return self.buffer[row - 1][col - 1]


@neovim.plugin
class Main(Base):
    @neovim.command('ShowSysPath')
    def show_sys_path(self):
        for p in sys.path:
            logger.info(p)
            self.nvim.out_write(f"{p}\n")

    @neovim.command('ShowCurrentLineLength')
    def show_current_line_length(self):
        length = len(self.line.strip())
        self.nvim.out_write(f"{length}\n")

    @neovim.command('RangeTrimTrailingSpaces', range=True)
    def trim_trailing_spaces_with_range(self, range, *args, **kwargs):
        start, end = range
        lines = self.buffer[start - 1: end]
        lines = [line.rstrip() for line in lines]
        self.buffer[start - 1: end] = lines

    @neovim.command('TrimTrailingSpaces')
    def trim_trailing_spaces(self):
        lines = [line.rstrip() for line in self.buffer]
        self.buffer[:] = lines

    @neovim.command('SplitLine')
    def split_line(self):
        spaces, content = common.get_spaces_and_content(self.line)
        lines = common.split(content)
        lines = [f"{spaces}{one}," for one in lines]
        before = self.buffer[:self.row - 1]
        after = self.buffer[self.row:]
        self.buffer[:] = before + lines + after

    @neovim.command('DuplicateInLine', range=True)
    def duplicate_in_line(self, range):
        start, end = range
        lines = self.buffer[start - 1: end]
        lines = [f"{line} {line}" for line in lines]
        self.buffer[start - 1: end] = lines


if __name__ == '__main__':
    __import__('ipdb').set_trace()
