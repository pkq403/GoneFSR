# Testing dissasemble python module
import dis
def adios(x):
    return x
def hola(a,b):
    c = a + b
    return adios(c)

if __name__=="__main__":
    dis.dis(hola)
