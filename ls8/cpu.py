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
        self.MUL = 0b10100010
        self.PRN = 0b01000111
        self.LDI = 0b10000010
        self.HLT = 0b00000001
    
    def load(self, program):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

       #  program = [
            # From print8.ls8
       #     0b10000010, # LDI R0,8
       #     0b00000000,
       #     0b00001000,
       #     0b01000111, # PRN R0
       #     0b00000000,
       #     0b00000001, # HLT
       # ]

        for instruction in program:
            self.ram[address] = instruction
            #print(f'I AM AN INSTRUCTION: {self.ram[address]}')
            address += 1
        
       # print(f'Ram:{self.ram}')

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        if op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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
        #TODO Build Dictionary for storing instructions
        while running:
            ir = self.ram[self.pc]
            if ir == self.LDI:
                self.ldi()
            elif ir == self.MUL:
               #TODO
               # define multiply method
               self.mult()
            elif ir == self.PRN:
                self.prn() 
            elif ir == self.HLT:
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

    def mult(self):
       # a = self.ram[self.pc+1]
       # b = self.ram[self.pc+2]
       #  print(f'a: {a}, b: {b}')
        self.alu("MUL", 0, 1)
        print(f'Ram: {self.ram[:15]}')
        print(f'Reg: {self.reg}')
        self.pc +=3

#print('---------------')
#print(myPC.ram_read(2))




