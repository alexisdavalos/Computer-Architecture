"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""
    
    """
    Already implemented:
    - load method, alu method, trace method
    Needs to be implemented:
    - cpu constructor
        - Ram
        - Program Counter
        - General Purpose Register

    """


    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        self.reg = [0] * 8

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b100000101010101010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            #print(f'I AM AN INSTRUCTION: {self.ram[address]}')
            address += 1
        
       # print(f'Ram:{self.ram}')

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU.""" 
        running = True
        while running:
            ir = self.ram[self.pc]
            if ir == 130:
                self.ldi()
            elif ir == 71:
                self.prn()
        
            elif ir == 1:
                running = self.hlt()

            else:
                print(f'Unknown instruction {ir} at address {self.pc}')
                sys.exit(1)

    def ram_read(self, address):
        # accept address
        # return it's value
        return f'Read from Ram: {self.ram[address]}'
    def ram_write(self, value, address):
        # take a value
        # write to address
        # no return 
        self.ram[address] = value 
    
    def ldi(self):
        address = self.ram[self.pc + 1]
        value = self.ram[self.pc + 2] 
        self.reg[address] = value
        self.pc +=3
    
    def prn(self):
        address = self.ram[self.pc+1]
        print(self.reg[address])
        self.pc +=2

    def hlt(self):
        self.pc +=1
        return False
myPC = CPU()

myPC.load()
myPC.run()
#print('---------------')
#print(myPC.ram_read(2))




