#!usr/bin/env python3

"""Main."""

import sys
from cpu import *

# initialiaze empty array
program = []
# read from file and store program from file specified in terminal
file_name = sys.argv[1]
print(file_name)
with open(file_name) as f:
    for line in f:
        if line[0]!= '#':
            num = int(line[0:8], 2)
            program.append(num)
    print(program)

cpu = CPU()
cpu.load(program)
cpu.run()
#cpu.mult()
