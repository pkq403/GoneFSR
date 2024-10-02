code = """\
start
if a < 0:
    a + b
else:
    a - b
done
"""

code2 = """\
start
a + b
a - b
"""

code_while ="""\
start
def hola(a,b,c):
    a + b
    b - c
t = 4
hola(t,2,3)
done
"""
import ast

top = ast.parse(code_while)
print(ast.dump(top))
