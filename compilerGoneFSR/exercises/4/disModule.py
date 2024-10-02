'''
In Python functions get compiled down to a low leel interpreter machine code.
You can see that with the dis module

Example:
'''
a = 3
b = 5
c = 6
def foo():
    return a + 2*b - 3*c

import dis
dis.dis(foo)

'''
Python's machine code is based on a simple stack machine.
To carry out operantions, operands are first pushed onto a stack.
Different operations then consume entries on the stack and replace 
the top entry with the result.

Example:
'''

# Evaluate a = 1 + 2*3 - 4*5

stack = []

stack.append(1)
stack.append(2)
stack.append(3)
# stack [1,2,3]

stack[-2:] = [stack[-2] * stack[-1]]
# stack [1,6]

stack[-2:] = [stack[-2] + stack[-1]]
# stack [7]

stack.append(4)
stack.append(5)
# stack [7, 4, 5]

stack[-2:] = [stack[-2] * stack[-1]]
# stack [7,20]

stack[-2:] = [stack[-2] - stack[-1]]
# stack [13]

a = stack.pop()
print(a) # resultado final de la funcion