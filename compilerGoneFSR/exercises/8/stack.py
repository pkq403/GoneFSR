# File to learn how the python stack works
import sys

def printstack():
    frame = sys._getframe()
    while frame:
        print("[%s]" % frame.f_code.co_name)
        print(" Locals: %s "% list(frame.f_locals))
        frame = frame.f_back

def foo():
    a = 10
    b = 20
    printstack()

def recursive(n):
    if n > 0:
        recursive(n - 1)
    else:
        printstack()

recursive(5)