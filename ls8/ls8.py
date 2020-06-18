#!usr/bin/env python3

"""Main."""

import sys
from cpu import *


Instructions = {
0b10100010: "Multiply",
0b01000111: "Print",
0b10000010: "LDI",
0b00000001: "Halt",
0b01000101: "Push",
0b01000110: "Pop",
}


# initialiaze empty array
program = []
# read from file and store program from file specified in terminal
file_name = sys.argv[1]
print(f'-----------------')
print(f'Program Loading: {file_name}')
print(f'-----------------\n')
with open(file_name) as f:
    for line in f:
        if line[0]!= '#':
            num = int(line[0:8], 2)
            program.append(num)
    #Displays The Program and the instructions passed
    print(f'-----------------')
    print(f'{file_name} Instructions:')
    print(f'-----------------\n')
    for indx, inst in enumerate(program):
        value = ''
        if inst in Instructions:
            value = Instructions[inst]
            print(f'{indx +1}: Instruction:({bin(inst)}) = {value}')
        else:
            print(f'{indx +1}: Number = {inst}')
        # Print The Instructio
        

print(f'\n-----------------')
print(f'Program Starting')
print(f'-----------------\n')
cpu = CPU()
cpu.load(program)
cpu.run()
#cpu.mult()
