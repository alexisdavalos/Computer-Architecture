#!usr/bin/env python3
"""Main."""

import sys
from cpu import *


Instructions = {
0b10100010: "Multiply #Multiplies Two Numbers",
0b01000111: "Print #Prints Num From REG[Num]",
0b10000010: "LDI #Stores Second Number in REG[Num1]",
0b00000001: "Halt #Stops The Program - Buggy Command Print Out",
0b01000101: "Push #Pushes Number To Stack",
0b01000110: "Pop #Pops from Top of Stack",
}

# initialiaze empty array
program = []
# read from file and store program from file specified in terminal
file_name = sys.argv[1]
print(f'----------------------------------')
print(f'Program Loading: {file_name}')
print(f'----------------------------------\n')

with open(file_name) as f:
    for line in f:
        if line[0]!= '#':
            num = int(line[0:8], 2)
            program.append(num)
    #Displays The Program and the instructions passed
    
    print(f'----------------------------------')
    print(f'{file_name} Instructions:')
    print(f'----------------------------------\n')
    
    for indx, inst in enumerate(program):
        value = ''
        if inst in Instructions:
            value = Instructions[inst]
            if int(bin(inst),2) != 0b00000001:
                print(f'inst: {bin(inst)}')
                print(f'value: {inst}')
                print(f'Line {indx +1} Instruction:({bin(inst)} or {inst}) = {value} \n ------------------------------------------------')
        else:
            print(f'    - Number = {inst} \n    - Binary = ({bin(inst)})\n')
        # Print The Instructios
        
cpu = CPU()
cpu.load(program)
cpu.run()
#cpu.mult()
