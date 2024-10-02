import dis

def add(x, y):
    return x + y

def sub(x, y):
    a = x - y
    return a

def main():
    a = add (1,2)
    b = sub(a, 1)

dis.dis(main)
dis.dis(add)