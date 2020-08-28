#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from contextlib import contextmanager

from dataclasses import dataclass

import enum
from enum import Enum

import string

from typing import *


@enum.unique
class Direction(Enum):
    RIGHT = 0
    UP = enum.auto()
    LEFT = enum.auto()
    DOWN = enum.auto()

    def ccw(self):
        return Direction((self.value + 1) % 4)

    def cw(self):
        return Direction((self.value - 1) % 4)

    def __str__(self):
        if self == self.RIGHT:
            return '>'
        elif self == self.UP:
            return '^'
        elif self == self.LEFT:
            return '<'
        elif self == self.DOWN:
            return 'v'

@enum.unique
class Instruction(Enum):
    PUSH_LEFT = '{'
    PUSH_RIGHT = '}'
    POP_LEFT = '['
    POP_RIGHT = ']'
    SET_DIR_RIGHT = '>'
    SET_DIR_UP = '^'
    SET_DIR_LEFT = '<'
    SET_DIR_DOWN = 'v'
    SET_REG_0 = '0'
    SET_REG_1 = '1'
    SET_REG_2 = '2'
    SET_REG_3 = '3'
    SET_REG_4 = '4'
    SET_REG_5 = '5'
    SET_REG_6 = '6'
    SET_REG_7 = '7'
    SET_REG_8 = '8'
    SET_REG_9 = '9'
    INPUT_CHAR = '?'
    OUTPUT_CHAR = '!'
    CONDITIONAL_TURN = '@'
    RETURN = '#'
    BIN_ADD = 'a'
    BIN_SUB = 's'
    BIN_MULT = 'm'
    BIN_DIV = 'd'
    BIN_REM = 'r'

    @classmethod
    def from_char(cls, c):
        try:
            return cls(c)
        except ValueError:
            pass
        return CallOrSkippedInstruction(c)

class CallOrSkippedInstruction:
    def __init__(self, block_name):
        assert block_name not in Parser.RESERVED_NAMES
        self.block_name = block_name

@dataclass
class Block:
    name: str
    instrs: Sequence[Sequence[Instruction]]
    left_entry: Optional[Tuple[int, int]]
    bottom_entry: Optional[Tuple[int, int]]
    right_entry: Optional[Tuple[int, int]]
    top_entry: Optional[Tuple[int, int]]

    def get_entry_from_dir(block, direction):
        if direction == Direction.RIGHT:
            return block.left_entry
        if direction == Direction.UP:
            return block.bottom_entry
        if direction == Direction.LEFT:
            return block.right_entry
        if direction == Direction.DOWN:
            return block.top_entry

class Parser:
    class Error(Exception):
        def __init__(self, msg, line_n, col_n):
            if msg[-1] == '.':
                msg = msg[:-1]
            msg += f' at ({line_n}, {col_n}).'
            super().__init__(msg)

    def make_error(parser, msg, col_n):
        line_n = parser.get_line_n()
        return parser.Error(msg, line_n, col_n)


    WHITESPACE = frozenset(string.whitespace)
    RESERVED_NAMES = frozenset(instr.value for instr in Instruction)

    def parse(self, code):
        self.cur_block = None
        self.blocks = {}
        lines = code.split('\n')
        for line in lines:
            self.parse_line(line)
        self.parse_line('')

    def parse_line(self, line):
        if self.cur_block is None:
            if len(line) == 0 or line[0] in self.WHITESPACE:
                return
            line = line.strip()

            self.parse_top_line(line)

        else:  # self.cur_block is not None
            if len(line) == 0 or line[0] in self.WHITESPACE:
                self.blocks[self.cur_block.name] = self.cur_block
                self.cur_block = None
                return
            line = line.strip()

            if line[0] == self.cur_block.name:
                self.parse_bottom_line(line)
            else:
                self.parse_middle_line(line)

    def parse_top_line(self, line):
        name = line[0]
        if name in self.blocks:
            raise self.make_error(f"Block '{name}' already exists.", 0)
        if name in self.RESERVED_NAMES:
            raise self.make_error(f"'{name}' is reserved name.", 0)

        self.cur_block = Block(
            name=name,
            instrs=[],
            left_entry=None,
            bottom_entry=None,
            right_entry=None,
            top_entry=None,
        )

        def instrs_gen():
            for col_n, char in enumerate(line):
                if col_n == 0:
                    yield None
                    continue
                self.parse_boundary(char, 'v', col_n)
                yield Instruction.from_char(char)
        self.add_instrs_line(list(instrs_gen()))

    def parse_bottom_line(self, line):
        assert line[0] == self.cur_block.name

        def instrs_gen():
            for col_n, char in enumerate(line):
                if col_n == 0:
                    yield None
                    continue
                self.parse_boundary(char, '^', col_n)
                yield Instruction.from_char(char)
        self.add_instrs_line(list(instrs_gen()))

    def parse_middle_line(self, line):
        def instrs_gen():
            for col_n, char in enumerate(line):
                if col_n == 0:
                    self.parse_boundary(char, '>', col_n)
                elif col_n == len(line) - 1:
                    self.parse_boundary(char, '<', col_n)
                yield Instruction.from_char(char)
        self.add_instrs_line(list(instrs_gen()))

    def parse_boundary(self, char, entry_char, col_n):
        if char == entry_char:
            self.set_entry(char, col_n)
        elif char != '#':
            msg = f"Invalid block boundary instruction '{char}'."
            raise self.make_error(msg, col_n)

    def set_entry(self, entry_char, col_n):
        line_n = self.get_line_n()
        pos = (line_n, col_n)
        if entry_char == '>':
            self.cur_block.left_entry = pos
        elif entry_char == '^':
            self.cur_block.bottom_entry = pos
        elif entry_char == '<':
            self.cur_block.right_entry = pos
        elif entry_char == 'v':
            self.cur_block.top_entry = pos
        else:
            assert False

    def get_line_n(self):
        return len(self.cur_block.instrs)

    def add_instrs_line(self, instrs_line):
        self.cur_block.instrs.append(instrs_line)

    cur_block: Optional[Block]

    blocks: Mapping[str, Block]

class Interpreter:
    class RuntimeError(Exception):
        pass

    def __init__(self, *, stdin=None, stdout=None):
        self.parser = Parser()
        self.stdin = stdin
        self.stdout = stdout

    @dataclass
    class Frame:
        block: Block
        ip: Tuple[int, int]

    def step(self, frame):
        line_n, col_n = frame.ip
        instr = frame.block.instrs[line_n][col_n]

        if False:
            pass

        elif instr == Instruction.PUSH_LEFT:
            self.step_push(0)
        elif instr == Instruction.PUSH_RIGHT:
            self.step_push(1)

        elif instr == Instruction.POP_LEFT:
            self.step_pop(0)
        elif instr == Instruction.POP_RIGHT:
            self.step_pop(1)

        elif instr == Instruction.SET_DIR_RIGHT:
            self.direction = Direction.RIGHT
        elif instr == Instruction.SET_DIR_UP:
            self.direction = Direction.UP
        elif instr == Instruction.SET_DIR_LEFT:
            self.direction = Direction.LEFT
        elif instr == Instruction.SET_DIR_DOWN:
            self.direction = Direction.DOWN

        elif instr == Instruction.SET_REG_0:
            self.reg = 0
        elif instr == Instruction.SET_REG_1:
            self.reg = 1
        elif instr == Instruction.SET_REG_2:
            self.reg = 2
        elif instr == Instruction.SET_REG_3:
            self.reg = 3
        elif instr == Instruction.SET_REG_4:
            self.reg = 4
        elif instr == Instruction.SET_REG_5:
            self.reg = 5
        elif instr == Instruction.SET_REG_6:
            self.reg = 6
        elif instr == Instruction.SET_REG_7:
            self.reg = 7
        elif instr == Instruction.SET_REG_8:
            self.reg = 8
        elif instr == Instruction.SET_REG_9:
            self.reg = 9

        elif instr == Instruction.INPUT_CHAR:
            self.reg = ord(self.stdin.read(1))
        elif instr == Instruction.OUTPUT_CHAR:
            c = chr(self.reg)
            self.stdout.write(c)

        elif instr == Instruction.CONDITIONAL_TURN:
            if self.reg > 0:
                self.direction = self.direction.ccw()
            elif self.reg < 0:
                self.direction = self.direction.cw()

        elif instr == Instruction.RETURN:
            return False

        elif instr == Instruction.BIN_ADD:
            self.reg = self.pop(0) + self.pop(1)
        elif instr == Instruction.BIN_SUB:
            self.reg = self.pop(0) - self.pop(1)
        elif instr == Instruction.BIN_MULT:
            self.reg = self.pop(0) * self.pop(1)
        elif instr == Instruction.BIN_DIV:
            self.reg = self.pop(0) // self.pop(1)
        elif instr == Instruction.BIN_REM:
            self.reg = self.pop(0) % self.pop(1)

        elif isinstance(instr, CallOrSkippedInstruction):
            self.execute_block_if_exists(instr.block_name)

        else:
            assert False

        if self.direction == Direction.RIGHT:
            frame.ip = line_n, col_n + 1
        if self.direction == Direction.UP:
            frame.ip = line_n - 1, col_n
        if self.direction == Direction.LEFT:
            frame.ip = line_n, col_n - 1
        if self.direction == Direction.DOWN:
            frame.ip = line_n + 1, col_n
        return True

    def step_push(self, stack_n):
        self.stacks[stack_n].append(self.reg)

    def step_pop(self, stack_n):
        self.reg = self.pop(stack_n)

    def pop(self, stack_n):
        stack = self.stacks[stack_n]
        if len(stack) == 0:
            stack_name = self.get_stack_name(stack_n)
            stack_name = stack_name[0].upper() + stack_name[1:]
            raise self.RuntimeError(f'{stack_name} stack is empty.')
        return stack.pop(-1)

    def execute_block_if_exists(self, block_name):
        if block_name in self.parser.blocks:
            self.execute_block(block_name)

    def execute_block(self, block_name):
        block = self.get_block(block_name)
        maybe_ip = block.get_entry_from_dir(self.direction)
        if maybe_ip is None:
            msg = f"Block '{block_name}' doesn't have entrypoint '{self.direction}'."
            raise self.RuntimeError(msg)
        frame = self.Frame(
            block=block,
            ip=maybe_ip,
        )

        while True:
            should_continue = self.step(frame)
            if not should_continue:
                break

    def execute(self, code=None):
        if code is not None:
            self.parser.parse(code)
        self.direction = Direction.RIGHT
        self.stacks = [], []
        self.reg = 42
        self.execute_block('$')

    def get_block(self, name):
        blocks = self.parser.blocks
        if name not in blocks:
            assert name not in Parser.WHITESPACE
            assert name not in Parser.RESERVED_NAMES
            raise self.RuntimeError(f"Missing block '{name}'.")
        return blocks[name]

    def get_stack_name(self, stack_n):
        if stack_n == 0:
            return 'left'
        elif stack_n == 1:
            return 'right'
        else:
            assert False

    parser: Parser
    direction: Direction
    stacks: Tuple[List[int], List[int]]
    reg: int

def execute(code, *, stdin=None, stdout=None):
    Interpreter(stdin=stdin, stdout=stdout).execute(code)

if __name__ == '__main__':
    from sys import argv, stdin, stdout
    if len(argv) > 2:
        from sys import stderr
        print('Too many args!', file=stderr)
        exit(1)
    elif len(argv) == 2:
        with open(argv[1], 'r') as f:
            data = f.read()
        f_in = stdin
        f_out = stdout
    else:
        data = stdin.read()
        f_in = None
        f_out = stdout
    execute(data, stdin=f_in, stdout=f_out)
