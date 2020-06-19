"""CPU functionality."""

import sys
# [X] Implement Stack Push
# [X] Implement Stack Pop
# [X] Format RAM Partition
# [X] Initialize Stack Pointer @ reg[-1]

# Day 4:
# [X] Implement the CALL and RET instructions
# [X] Implement Subroutine Calls and be able to run the call.ls8 program

# Sprint:




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
        self.reg = [0] * 8 # REG to store values from RAM
        self.fl = 0b00000000
        # self.sp = 0XF4 # stack pointer
        self.running = False # Boolean to toggle Machine ON/OFF
        self.MUL = 0b10100010
        self.ADD = 0b10100000
        self.SUB = 0b10100001
        self.OR =  0b10101010
        self.AND = 0b10101000
       
        self.PRN = 0b01000111
        self.LDI = 0b10000010
        self.HLT = 0b00000001

        self.PUSH = 0b01000101
        self.POP = 0b01000110

        self.CALL = 0b01010000
        self.RET = 0b00010001

        self.CMP = 0b10100111
        self.JEQ = 0b01010101
        self.JNE = 0b01010110
        self.JMP = 0b01010100

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
                self.reg[i] = 0XF4
        
        # Marks Reserved Partition of RAM
        self.ram[self.reg[-1]:] = f'RRR01234567'
        
        
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
        stack = f'Head ->{self.ram[self.reg[-1]:0xf4]}<- Tail'

        print(f'\n---------------------')
        print(f'Machine State Report')    
        print(f'---------------------\n')
        print(f'State of RAM:\n{(self.ram)}\n')
        print(f'State of REG:\n{self.reg}\n')
        print(f'State of PC:\n{self.pc}\n')
        print(f'State of Stack:\n{stack}\n')
        print(f'State of Stack Pointer:\n{self.ram[self.reg[-1]]}\n')
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
            self.CALL: self.call,
            self.RET: self.ret,
            self.ADD : self.add,
            self.CMP : self.comp,
            self.JEQ: self.jeq,
            self.JNE: self.jne,
            self.JMP: self.jmp,
            self.AND: self.andOperation,
            self.OR: self.orOperation,
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
        x = self.reg[reg_a]
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            # subtract reg_b from reg_a 
            result = self.reg[reg_b] - self.reg[reg_a]
            # store in register A
            self.reg[reg_a] = result
        elif op == "AND":
            # grab bitwise operation value
            result = self.reg[reg_a] & self.reg[reb_b]
            # store in register A
            self.reg[reg_a] = result
        elif op == "OR":
            # grab bitwise operation value
            result = self.reg[reg_a] | self.reg[reg_a]
            # store in register A
            self.reg[reg_a] = result
        elif op == "MUL":
            # multiply reg_a by reg_b
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            # reg_a < reg_b
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 0b00000100
            # reg_a > reg_b
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b00000010
            # reg_a == reg_b
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 0b00000001
            else:
                self.fl = 0b00000000
        else:
            raise Exception(f'Unsupported ALU operation:', op)

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

    def push(self):
        # Decrement the 'SP'
        
        # Decrement the REG SP
        self.reg[-1] -= 1
        # Copy the value in given register
        address = self.ram[self.pc + 1]
        value = self.reg[address]
        #put value at the top of stack
        self.ram[self.reg[-1]] = value
        # Print Action
        print(f'Pushed [{self.ram[self.reg[-1]]}] To Top of Stack!')
        # Increment Program/Command Counter
        self.pc +=2
    

    def pop(self):
        cur = self.reg[-1]
        # Grab value
        value = self.ram[cur]
        # Value Address
        address = self.ram[self.pc + 1]
        # Value from Reg
        self.reg[address] = value
        # Increment the Stack Pointer
        self.reg[-1] += 1
        # Print The Popped Value
        print(f'Popped [{value}] From Top of Stack!')
        self.pc += 2

   
    def call(self):
        # Calls a subroutine at the address stored in the register
        # 1. The address of the instruction directly after CALL is pushed onto the stack. This allows us to return to where we left off when the subroutine finishes executing.
        return_pc = self.pc + 2

        # Set value in the stack to the PC value we want to return to after we call the function
        # Pushes the return pc address to the allocated Stack portion of the RAM
        self.reg[-1] -= 1
        self.ram[self.reg[-1]] = return_pc

        # 2. The PC is set to the address stored in the given register. We jump to that location in RAM and execute the first instruction in the subroutine. The PC can move forward or backward from its current location.
        subroutine = self.ram[self.pc + 1]
        self.pc = self.reg[subroutine]

    
    def ret(self):
        # Return from subroutine
        # Pop the value from the top of the stack and store it in the PC
    
        ts = self.reg[-1]
        return_pc = self.ram[ts]
        self.pc = return_pc
    
    def mult(self):
        self.alu("MUL", 0,1)
        self.pc +=3
    
    def add(self):
        self.alu("ADD", 0,0)
        self.pc +=3

    # L G E
    def comp(self):
        self.alu("CMP", 0,1)
        self.pc +=3
    
    def jeq(self):
        flag = str(self.fl)[-1]
        address = self.ram[self.pc + 1]
        if int(flag) is 1:
            self.pc = self.reg[address]
        else:
            self.pc += 2

    # sprint requirements
    def jmp(self):
        address = self.ram[self.pc + 1]
        self.pc = self.reg[address]

    def jne(self):
        flag = str(self.fl)[-1]
        address = self.ram[self.pc + 1]
        if int(flag) is not 1:
            self.pc = self.reg[address]
        else:
            self.pc += 2

    # Sprint Stretch
    def andOperation(self):
        self.alu("AND", 0,0)
        self.pc +=3

    def orOperation(self):
        self.alu("OR",0,0)
        self.pc +=3

    def sub(self):
        self.alu("SUB", 0,0)
        self.pc +=3
        
    def jlt(self):
        pass
    def jle(self):
        pass
    def jgt(self):
        pass



#print('---------------')
#print(myPC.ram_read(2))




