#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import neovim
from xml.dom import minidom

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
    def tabpage(self):
        return self.nvim.current.tabpage

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

    def get_global_variable(self, name):
        return self.nvim.vars.get(name, None)
        """
        try:
            return self.nvim.eval(f"g:{name}")
        except Exception:
            return
        """

    def get_char_before_cursor(self):
        row, col = self.window.cursor
        logger.deplus(f"{row}, {col}")
        return self.buffer[row - 1][col - 1]

    def get_lines_of_range(self, range):
        start, end = range
        lines = self.buffer[start - 1: end]
        return lines

    def replace_lines_by_range(self, new_lines, range):
        start, end = range
        self.buffer[start - 1: end] = new_lines

    def replace_line_by_cursor(self, new_lines):
        before = self.buffer[:self.row - 1]
        after = self.buffer[self.row:]
        self.buffer[:] = before + new_lines + after

    def replace_line_one_by_one(self, new_line):
        self.replace_line_by_cursor([new_line])

    def move_tabpage_right(self):
        total_number = self.nvim.call('tabpagenr', '$')
        if self.tabpage.number == total_number:
            cmd = 'tabmove 0'
        else:
            cmd = 'tabmove +1'
        self.nvim.command(cmd)

    def move_tabpage_left(self):
        if self.tabpage.number == 1:
            cmd = 'tabmove $'
        else:
            cmd = 'tabmove -1'
        self.nvim.command(cmd)


@neovim.plugin
class Main(Base):
    @neovim.command('DeleteEmptyLines')
    def delete_empty_lines(self):
        lines = [line for line in self.buffer if line]
        self.buffer[:] = lines

    @neovim.command('RangeReverseLines', range=True)
    def range_reverse_lines(self, range):
        lines = self.get_lines_of_range(range)
        lines = [common.reverse_line(line) for line in lines]
        self.replace_lines_by_range(lines, range)

    @neovim.command('ShowSysPath')
    def show_sys_path(self):
        cmd = '/usr/local/bin/python'
        virtual_env = os.environ.get('VIRTUAL_ENV', '')
        if virtual_env:
            cmd = os.path.join(virtual_env, 'bin/python')
        output = self.nvim.command_output(f'!{cmd} -c "import sys;print(sys.path)"')
        logger.info(output)
        paths = eval(output.split('\n')[-2])
        for p in paths:
            logger.info(p)
            self.nvim.out_write(f"{p}\n")

    @neovim.command('ShowCurrentLineLength')
    def show_current_line_length(self):
        length = len(self.line.strip())
        self.nvim.out_write(f"{length}\n")

    @neovim.command('RangeTrimTrailingSpaces', range=True)
    def trim_trailing_spaces_with_range(self, range, *args, **kwargs):
        lines = self.get_lines_of_range(range)
        lines = [line.rstrip() for line in lines]
        self.replace_lines_by_range(lines, range)

    @neovim.command('TrimTrailingSpaces')
    def trim_trailing_spaces(self):
        lines = [line.rstrip() for line in self.buffer]
        self.buffer[:] = lines

    @neovim.command('ReverseLine')
    def reverse_line(self):
        spaces, content = common.get_spaces_and_content(self.line)
        if not content:
            return
        new_line = common.reverse_line(self.line)
        self.replace_line_one_by_one(new_line)

    @neovim.command('SplitLine')
    def split_line(self):
        spaces, content = common.get_spaces_and_content(self.line)
        if not content:
            return
        lines = common.split(content)
        lines = [f"{spaces}{one}," for one in lines]
        self.replace_line_by_cursor(lines)

    @neovim.command('RangeDuplicateInLine', range=True)
    def range_duplicate_in_line(self, range):
        lines = self.get_lines_of_range(range)
        lines = [f"{line} {line}" for line in lines]
        self.replace_lines_by_range(lines, range)

    @neovim.command('FormatXML')
    def pretty_print_xml(self):
        # todo, some special content may be changed
        lines = [line.strip() for line in self.buffer]
        starter = []
        first_line = lines[0]
        if '<?xml' in first_line.lower():
            starter.append(first_line)
            lines = lines[1:]
        first_line = lines[0]
        if '<!DOCTYPE' in first_line.upper():
            starter.append(first_line)
            lines = lines[1:]
        xml_string = ''.join(lines)
        xml_string = minidom.parseString(xml_string).toprettyxml(indent='  ')
        lines = xml_string.split('\n')[1:]
        while not lines[-1]:
            lines.pop(-1)
        lines = [common.keep_space_in_xml_node_end_if_has_props(line) for line in lines]
        self.buffer[:] = starter + lines

    @neovim.command('MoveTabpage', nargs=1)
    def move_tabpage(self, args):
        assert type(args) is list
        assert len(args) == 1
        direction = args[0]
        if direction == '+1':
            self.move_tabpage_right()
        elif direction == '-1':
            self.move_tabpage_left()
        else:
            self.nvim.err_write('need to be +1 or -1\n')

    @neovim.function('FuncMoveTabpage')
    def func_move_tabpage(self, args):
        direction = args[0]
        if direction == 1:
            self.move_tabpage_right()
        elif direction == -1:
            self.move_tabpage_left()


if __name__ == '__main__':
    __import__('ipdb').set_trace()
