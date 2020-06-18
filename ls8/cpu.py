"""CPU functionality."""

import sys
#TODO
# [] Implement Stack Push
# [] Implement Stack Pop
# [] Format RAM Partition
# [] Initialize Stack Pointer @ reg[-1]

#Plan of Attack
# SP = 7



class CPU:
    """Main CPU class."""
    
    """
    Already implemented:
    - load method, alu method, trace method
    - cpu constructor
        - Ram
        - Program Counter
        - General Purpose Register
    - hash table for accessing program function O(1) lookup
    """


    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 # Array map of empty memory
        self.pc = 0 # program/command counter
        self.sp = 0xF4 # stack pointer
        self.reg = [0] * 8 # REG to store values from RAM
        self.name = ''
        self.running = False # Boolean to toggle Machine ON/OFF
        self.MUL = 0b10100010
        self.PRN = 0b01000111
        self.LDI = 0b10000010
        self.HLT = 0b00000001
        self.PUSH = 0b01000101
        self.POP = 0b01000110

    def TurnOn(self):
     
        print(f'\n-----------------')
        print(f'LS8 is initializing...')
        print(f'-----------------')

        for i in range(len(self.reg)):
            # `R0`-`R6` are cleared to `0`.
            if i < len(self.reg) - 1:
                self.reg[i] = 0
            # `R7` is set to `0xF4`.
            else:
                self.reg[i] = self.sp
        
        # Formats Stack Pointer 
        self.ram[self.sp] = f'SP:{hex(self.sp)}'
        # Marks Reserved Partition of RAM
        self.ram[self.sp+1:] = f'Reserved!'
        
        
        print(f'\n-----------------')
        print(f'LS8 ON')
        print(f'-----------------')
         # Starts Running Commands
        self.running = True
        print(f'-----------------------')
        print(f'LS8 is executing.....')
        print(f'-----------------------\n')

    def report(self):
        # Define Stack
        stack = f'Head ->{self.ram[self.sp:0xf4]}<- Tail'

        print(f'\n---------------------')
        print(f'Machine State Report')    
        print(f'---------------------\n')
        print(f'State of RAM:\n{(self.ram)}\n')
        print(f'State of REG:\n{self.reg}\n')
        print(f'State of PC:\n{self.pc}\n')
        print(f'State of Stack:\n{stack}\n')
        print(f'State of SP:\n{self.ram[self.sp]}\n')
        print(f'-----------------\n')
        print(f'\n-----------------')
        print(f'LS8 is OFF')
        print(f'-----------------\n')

    def load(self, program):
        """Load a program into memory."""
        # Represents index pointer in program arr passed in
        address = 0
        for instruction in program:
            self.ram[address] = instruction
            address += 1
        
       # print(f'Ram:{self.ram}')

    def run(self, branch_table = None):
        """Run the CPU.""" 

        # Initialize Branch Table
        branch_table = {
            self.LDI : self.ldi,
            self.PRN : self.prn,
            self.MUL : self.mult,
            self.HLT : self.hlt,
            self.PUSH : self.push,
            self.POP: self.pop,
            }

        #Turns LS8 On
        self.TurnOn()
        # Toggle cpu running boolean to turn CPU on
        while self.running:
            # ir is the binary value in ram at the index of pc
            ir = self.ram[self.pc]
            # check if value is a key in our hash table
            if ir in branch_table:
                # run the function stored as the value of the key
                branch_table[ir]()
            # throw error
            elif ir not in branch_table:
                print(f"Unknown instruction {bin(ir)} at address {self.pc}")
                sys.exit(1)
            # print the state of ram and reg
        
        # Prints report after program execution
        self.report()       
 
    
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
        # print(self.reg[address])
         # Print Action
        print(f'Read From Register: [{self.reg[address]}]')
        self.pc +=2

    def hlt(self):
        self.pc +=1
        self.running = False
        print(f'\n------------------')
        print(f'Program Completed!')
        print(f'------------------')

    def mult(self):
       # a = self.ram[self.pc+1]
       # b = self.ram[self.pc+2]
       #  print(f'a: {a}, b: {b}')
        self.alu("MUL", 0, 1)
        self.pc +=3
    
    def push(self):
        # Decrement the 'SP'
        self.sp -= 1
        # Copy the value in given register
        address = self.ram[self.pc + 1]
        value = self.reg[address]
        #put value at the top of stack
        self.ram[self.sp] = value
        # Print Action
      
        # print(f'Pushed [{self.ram[self.sp]}] To Top of Stack!')
        # Increment Program/Command Counter
        self.pc +=2

    def pop(self):
        # # Grab address
        # address = self.ram[self.pc + 1]
        # # Grab value
        # value = self.reg[address]
        # # clear current
        # self.sp +=1
        # print(f'popped: {value} ')
        self.pc += 2
        pass

#print('---------------')
#print(myPC.ram_read(2))




