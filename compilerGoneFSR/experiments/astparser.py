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
while n < 1:
    a + b
    b - c
a - b
"""
import ast

top = ast.parse(code_while)
print(ast.dump(top))
