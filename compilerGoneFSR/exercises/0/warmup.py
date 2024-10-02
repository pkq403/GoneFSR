# Ejercicio resuelto por Pedro Castro
# Exercise 0 - warmup.py
#
# A warmup exercise to illustrate some of the basic concepts of
# compilers.  It defines a very minimal virtual machine.  You are
# to write three programs based on this machine.   Follow instructions
# near the bottom of this file.
# ----------------------------------------------------------------------

# TinyVM. 
# 
# A tiny virtual machine.  The machine has 8 registers (R0,R1,...,R7)
# and understands the following 8 instructions--which are encoded as
# tuples.
#
#   ('ADD', 'Ra', 'Rb', 'Rd')     -> Rc = Ra + Rb
#   ('SUB', 'Ra', 'Rb', 'Rd')     -> Rc = Ra - Rb
#   ('MOV', value, 'Rd')          -> Rd = value
#   ('LD', 'Rs', 'Rd', offset)    -> Rd = MEMORY[Rs + offset]
#   ('ST', 'Rs', 'Rd', offset)    -> MEMORY[Rd + offset] = Rs
#   ('JMP', 'Rd', offset)         -> PC = Rd + offset
#   ('BZ', 'Rt', offset)          -> if Rt == 0: PC = PC + offset
#   ('HALT,)                      -> Halts machine
#
# In the the above instructions 'Rx' means some register number such 
# as R0, R1, etc.  Initially the machine initialzes R0,...,R6 to 0.
# R7 is initialized to last valid memory address.

class Halt(Exception):
    pass

class TinyVM(object):
    def run(self, memory):
        '''
        Run a program. memory is a Python list containing the program
        instructions and other data.  Upon startup, all registers
        are initialized to 0.  R7 is initialized with the highest valid
        memory address.
        '''
        self.pc = 0
        self.registers = { f'R{d}':0 for d in range(8) }
        self.memory = memory
        self.registers['R7'] = len(memory) - 1
        try:
            while True:
                op, *args = self.memory[self.pc]
                self.pc += 1
                getattr(self, op)(*args)
        except Halt:
            self.registers = { key: 0 for key in self.registers }
        return

    def ADD(self, ra, rb, rd):
        self.registers[rd] = self.registers[ra] + self.registers[rb]

    def SUB(self, ra, rb, rd):
        self.registers[rd] = self.registers[ra] - self.registers[rb]

    def MOV(self, value, rd):
        self.registers[rd] = value

    def LD(self, rs, rd, offset):
        self.registers[rd] = self.memory[self.registers[rs]+offset]

    def ST(self, rs, rd, offset):
        self.memory[self.registers[rd]+offset] = self.registers[rs]

    def JMP(self, rd, offset):
        self.pc = self.registers[rd] + offset

    def BRZ(self, rt, offset):
        if not self.registers[rt]:
            self.pc += offset

    def HALT(self):
        raise Halt()
            

machine = TinyVM()

# ----------------------------------------------------------------------
# Problem 1:  Computers
#
# The CPU of a computer executes low-level instructions.  Using the
# TinyVM instruction set above, show how you would compute 2 + 3 - 4.

prog1 = [ # Instructions here
          ('MOV', 2, 'R1'),
          ('MOV', 3, 'R2'),
          ('MOV', 4, 'R3'),
          ('ADD', 'R1', 'R2', 'R5'),
          ('SUB', 'R5', 'R3', 'R6'),
          ('ST', 'R6', 'R7', 0),    # Save result. Replace 'RESULT' with a register
          ('HALT',),
          0            # Store the result here (note: R7 holds this address)
          ]

machine.run(prog1)
print('Program 1 Result:', prog1[-1], '(should be 1)')

# ----------------------------------------------------------------------
# Problem 2: Computation
#
# Write a TinyVM program that computes 23 * 37.  Note: The machine
# doesn't implement multiplication.  So, you need to figure out how
# to do it.

prog2 = [ # Instructions here
          ('MOV', 23, 'R1'),
          ('MOV', 37, 'R2'),
          ('MOV', 1, 'R4'),
          ('BRZ', 'R1', 3), # SALTA A LA INSTRUCCION DE ST
          ('ADD', 'R3', 'R2', 'R3'),
          ('SUB', 'R1', 'R4', 'R1'),
          ('JMP', 'R6', 3), # SALTA A LA INSTRUCCION BRZ
          ('ST', 'R3', 'R7', 0),
          ('HALT',),
          0           # Store result here
        ]

machine.run(prog2)
print('Program 2 Result:', prog2[-1], f'(Should be {23*37})')

# ----------------------------------------------------------------------
# Problem 3: Abstraction
#
# Write a Python function mul(x, y) that computes x * y on TinyVM. 
# This function, should abstract details away--you're not supposed to
# worry about how it works.  Just call mul(x, y).

def mul(x, y):
    prog = [ # Instructions here
             ('LD', 'R7', 'R1', -1),
             ('LD', 'R7', 'R2', -2),
             ('MOV', 1, 'R4'),
             ('BRZ', 'R1', 3), # SALTA A LA INSTRUCCION DE ST
             ('ADD', 'R3', 'R2', 'R3'),
             ('SUB', 'R1', 'R4', 'R1'),
             ('JMP', 'R6', 3), # SALTA A LA INSTRUCCION BRZ
             ('ST', 'R3', 'R7', 0),
             ('HALT',),
             x,      # Input value
             y,      # Input value
             0       # Result
    ]
    machine.run(prog)
    return prog[-1] 

print(f'Problem 3: 51 * 53 = {mul(51, 53)}. Should be {51*53}')

# ----------------------------------------------------------------------
# Problem 4: Challenge
#
# Rewrite this recursive Python function as a single set of TinyVM
# instructions that recursively calculate the same result.
print("Problem 4 Fibonacci")
def fib(n):
    if n <= 2:
        return 1
    else:
        return fib(n-1) + fib(n-2)
print(f"Fibonacci(10) should be {fib(12)}")
# Your rewritten version should look like this:
def fib(n):
    prog = [ # Instructions here
             ('LD', 'R7', 'R1', -1), # En R1 Input value
             ('MOV', 1, 'R6'),
             ('BRZ', 'R1', 15), # Si R1 == 0, salta al final, devuelve 1
             ('SUB', 'R1', 'R6', 'R2'),
             ('BRZ', 'R1', 13), # Si R1 == 1, salta al final, devuelve 1
             ('MOV', 1, 'R2'), # Si R1 (el input value) es diferente != 0 y != 1
             ('MOV', 1, 'R3'),
             ('MOV', 2, 'R4'),
             ('SUB', 'R1','R4', 'R1'), # n = n - 2
             ('MOV', 0, 'R4'),
             ('BRZ', 'R1', 6), # Saltas a despues del bucle
             ('ADD', 'R3', 'R4', 'R5'),
             ('ADD', 'R2', 'R3', 'R3'),
             ('ADD', 'R5', 'R4', 'R2'),
             ('MOV', 1, 'R5'),
             ('SUB', 'R1', 'R5','R1'),
             ('JMP', 'R4', 10),
             ('ADD', 'R4', 'R3', 'R6'),
             ('ST', 'R6', 'R7', 0),
             ('HALT',),
             n,      # Input value
             0       # Result
    ]
    machine.run(prog)
    return prog[-1] 
        
print(f'Assembly Fibonacci = {fib(12)}')