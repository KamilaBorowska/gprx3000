# Copyright (c) 2016 Konrad Borowski
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from sys import argv, stdin, stdout

class UnderflowError(ArithmeticError):
    pass

class GoToError(IndexError):
    pass

def plus(machine):
    machine.a += machine.b

def minus(machine):
    machine.a -= machine.b
    # Negative numbers don't exist. Only natural are the truth!
    if machine.a < 0:
        raise UnderflowError()

def multiply(machine):
    machine.a *= machine.b

def divide(machine):
    machine.a //= machine.b

def modulo(machine):
    machine.a %= machine.b

def goto(machine):
    # Every step in machine implicitly does a step, so move a bit backwards.
    position = machine.a
    if position > len(machine.program):
        raise GoToError()
    machine.position = position - 1

def print_char(machine):
    stdout.write(chr(machine.a))

def read_char(machine):
    result = stdin.read(1)
    machine.a = ord(result) + 1 if result else 0

def exchange(machine):
    machine.a, machine.b, machine.c = machine.c, machine.a, machine.b

operations = {
    '+': plus,
    '-': minus,
    '*': multiply,
    '/': divide,
    '%': modulo,
    'g': goto,
    'p': print_char,
    'r': read_char,
    'x': exchange,
}

class GPRX3000:
    position = 0
    a = 0
    b = 0
    c = 0

    def __init__(self, program):
        self.program = program

    def step(self):
        number = []
        while self.program[self.position].isdigit():
            number.append(self.program[self.position])
            self.position += 1
        if number:
            self.a = int("".join(number))
        operations[self.program[self.position]](self)
        self.position += 1

    def run(self):
        while self.position < len(self.program):
            self.step()

is_stdin = len(argv) == 1 or argv[1] == '-'

handle = stdin if is_stdin else open(argv[1])
try:
    program = handle.read()
    GPRX3000(program).run()
finally:
    if not is_stdin:
        handle.close()
