# Experiento para crear un AST con el modulo de python ast
text = "a = 2 + 3 * (4 + 5)"
import ast
c = ast.parse(text)
print(ast.dump(c))