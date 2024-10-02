# Como genera python codigo de bajo nivel con condiciones
import dis
# Funcion Condicional
def foo(a, b):
    if a < b:
        print("yes")
    else:
        print("no")

# dis.dis(foo)

# While loop

def countdown(n):
    while n > 0:
        print("T-minux", n)
        n -= 1

dis.dis(countdown)