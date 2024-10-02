# Creating Basic Blocks and Control Flow Graphs
import ast

class CodeGenerator(ast.NodeVisitor):
    def __init__(self):
        self.code = []
        self._label = 0
    
    def new_block(self):
        self._label += 1
        return 'b%d' % self._label
    
    def visit_While(self, node):
        whileblock = self.new_block()
        self.code.append(('BLOCK', whileblock))
        self.visit(node.test)

        mergeblock = self.new_block()

        self.code.append(('JUMP_IF_FALSE', mergeblock))

        for bnode in node.body:
            self.visit(bnode)
        self.code.append(('JUMP', whileblock))
        
        # mergeblock
        self.code.append(('BLOCK', mergeblock))

    def visit_If(self, node):
        self.visit(node.test)

        ifblock = self.new_block()
        elseblock = self.new_block()
        mergeblock = self.new_block()

        self.code.append(('JUMP_IF_FALSE', elseblock))

        self.code.append(('BLOCK', ifblock))
        for bnode in  node.body:
            self.visit(bnode)
        self.code.append(('JUMP', mergeblock))

        if node.orelse:
            self.code.append(('BLOCK', elseblock))
            # visit the body of the else-clause
            for bnode in node.orelse:
                self.visit(bnode)
        
        # Mergeblock
        self.code.append(('BLOCK', mergeblock))

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)
        opname = node.op.__class__.__name__
        inst = ("BINARY_"+opname.upper(),)
        self.code.append(inst)
    
    # def visit_Assign(self, node):
    #     for t in node.targets: self.visit_Name(t)
    #     self.visit_BinOp(node.value)
    #     inst = (("ASSIGN " ,str(node.targets[0].id)))
    #     self.code.append(inst)

    def visit_Compare(self, node):
        self.visit(node.left)
        opname = node.ops[0].__class__.__name__
        self.visit(node.comparators[0])
        inst = ("BINARY_" + opname.upper(),)
        self.code.append(inst)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            inst = ('LOAD_GLOBAL', node.id)
        elif isinstance(node.ctx, ast.Store):
            inst = ('STORE_GLOBAL', node.id)
        else:
            inst = ('UNIMPLEMENTED',)
        self.code.append(inst)

    def visit_Num(self, node):
        inst = ('LOAD_CONST', node.n)
        self.code.append(inst)

code1 = """\
start
if a < 0:
   a + b
else:
   a - b
done
"""
code2 = """\
start
while n < 0:
    n = n - 1
done
"""

top = ast.parse(code2)
gen = CodeGenerator()
gen.visit(top)
for instr in gen.code: print(instr)