import pdb
'''
IR Code generation
Author: Pedro Castro
'''
'''
Here is an instruction set specification for the IRCode:

    MOVI   value, target       ;  Load a literal integer
    VARI   name                ;  Declare an integer variable 
    ALLOCI name                ;  Allocate an integer variabe on the stack
    LOADI  name, target        ;  Load an integer from a variable
    STOREI target, name        ;  Store an integer into a variable
    LOADFASTI  name, target        ;  Load an integer from a local variable
    STOREFASTI target, name        ;  Store an integer into a local variable
    ADDI   r1, r2, target      ;  target = r1 + r2
    SUBI   r1, r2, target      ;  target = r1 - r2
    MULI   r1, r2, target      ;  target = r1 * r2
    DIVI   r1, r2, target      ;  target = r1 / r2
    PRINTI source              ;  print source  (debugging)
    CMPI   op, r1, r2, target  ;  Compare r1 op r2 -> target
    AND    r1, r2, target      :  target = r1 & r2
    OR     r1, r2, target      :  target = r1 | r2
    XOR    r1, r2, target      :  target = r1 ^ r2

    MOVF   value, target       ;  Load a literal float
    VARF   name                ;  Declare a float variable 
    ALLOCF name                ;  Allocate a float variable on the stack
    LOADF  name, target        ;  Load a float from a variable
    STOREF target, name        ;  Store a float into a variable
    LOADFASTF  name, target        ;  Load a float from a local variable
    STOREFASTF target, name        ;  Store a float into a local variable
    ADDF   r1, r2, target      ;  target = r1 + r2
    SUBF   r1, r2, target      ;  target = r1 - r2
    MULF   r1, r2, target      ;  target = r1 * r2
    DIVF   r1, r2, target      ;  target = r1 / r2
    PRINTF source              ;  print source (debugging)
    CMPF   op, r1, r2, target  ;  r1 op r2 -> target

    MOVB   value, target       ; Load a literal byte
    VARB   name                ; Declare a byte variable
    ALLOCB name                ; Allocate a byte variable
    LOADB  name, target        ; Load a byte from a variable
    STOREB target, name        ; Store a byte into a variable
    LOADFASTB  name, target        ;  Load a byte from a local variable
    STOREFASTB target, name        ;  Store a byte into a local variable
    PRINTB source              ; print source (debugging)
    CMPB   op, r1, r2, target  ; r1 op r2 -> target

    MOVS   value, target       ;  Load a literal string
    VARS   name                ;  Declare an string variable 
    ALLOCS name                ;  Allocate an string variabe on the stack
    LOADS  name, target        ;  Load an string from a global variable
    STORES target, name        ;  Store an string into a global variable
    LOADFASTS  name, target        ;  Load an string from a local variable
    STOREFASTS target, name        ;  Store an string into a local variable

control flow instructions

    LABEL  name                  ; Declare a block label
    BRANCH label                 ; Unconditionally branch to label
    CBRANCH test, label1, label2 ; Conditional branch to label1 or label2 depending on test being 0 or not
    CALL   name, arg0, arg1, ... argN, target    ; Call a function name(arg0, ... argn) -> target
    RET    r1                    ; Return a result from a function

codification instructions
    CODER source, output
    DECODER source, output
'''

from . import ast

class GenerateCode(ast.NodeVisitor):
    def __init__(self):
        # counter for registers
        self.register_count = 0
        self.branch_count = 0
        # The generated code (list of tuples) before Project 8, now list of lists of tuples
        self.program = {"premain": {'function_name': "premain", "params_types": [],  "code": [], "return_type": 'void', 'params_labels': []}}
        self.cur_function = 'premain'
        self.local_variables = []
        # Binary operations codes
        self.binopcodes = {'int': {'+': 'ADDI', '-': 'SUBI', '*': 'MULI', '/': 'DIVI'}, 'float': {'+': 'ADDF', '-': 'SUBF', '*': 'MULF', '/': 'DIVF'}}
        self.inst_declare_var_global = {'int': 'VARI', 'float': 'VARF', 'char': 'VARB', 'bool': 'VARI', 'string': 'VARS'} # for global variables
        self.inst_declare_var_local = {'int': 'ALLOCI', 'float': 'ALLOCF', 'char': 'ALLOCB', 'bool': 'ALLOCI', 'string': 'ALLOCS'} # for local variables
        self.inst_str = {'int': 'STOREI', 'float': 'STOREF', 'char': 'STOREB', 'bool': 'STOREI', 'string': 'STORES'} # for global variables
        self.inst_str_local = {'int': 'STOREFASTI', 'float': 'STOREFASTF', 'char': 'STOREFASTB', 'bool': 'STOREFASTI', 'string': 'STOREFASTS'} # for local variables
        self.inst_load = {'int': 'LOADI', 'float': 'LOADF', 'char': 'LOADB', 'bool': 'LOADI', 'string': 'LOADS'} # for global variables
        self.inst_load_local= {'int': 'LOADFASTI', 'float': 'LOADFASTF', 'char': 'LOADFASTB', 'bool': 'LOADFASTI', 'string': 'LOADFASTS'} # for local variables
        self.inst_cmp = {'int': 'CMPI', 'float': 'CMPF', 'char': 'CMPB'}
        self.cmp_op = ['==', '!=', '<', '<=', '>', '>=']
        self.get_bool_binopcodes = lambda x, args_type : {'int': 'CMPI', 'float': 'CMPF', 'char': 'CMPB'}.get(args_type, None) if x in self.cmp_op  else {'&&': 'AND', '||': 'OR'}.get(x, None)
        self.logical_op = ['&&' '||']
        # print types
        self.print_types = {'int': 'PRINTI', 'bool': 'PRINTI', 'char': 'PRINTB', 'float': 'PRINTF', 'string': 'PRINTS'}

    def new_register(self):
         '''
         Creates a new temporary register
         '''
         self.register_count += 1
         return f'R{self.register_count}'

    def new_block(self):
        self.branch_count += 1
        return f'B{self.branch_count}'
    
    def visit_IntegerLiteral(self, node):
        target = self.new_register()
        self.program[self.cur_function]['code'].append(('MOVI', node.value, target))
        node.register = target

    def visit_FloatLiteral(self, node):
        target = self.new_register()
        self.program[self.cur_function]['code'].append(('MOVF', node.value, target))
        node.register = target

    def visit_CharLiteral(self, node):
        target = self.new_register()
        self.program[self.cur_function]['code'].append(('MOVB', ord(node.value), target))
        node.register = target

    def visit_BoolLiteral(self, node):
        target = self.new_register()
        self.program[self.cur_function]['code'].append(('MOVI', int(node.value == True), target))
        node.register = target

    def visit_StringLiteral(self, node):
        target = self.new_register()
        self.program[self.cur_function]['code'].append(('MOVS', node.value, target))
        node.register = target
    
    def visit_ConstDeclaration(self, node):
        value_type = node.value.type.name
        self.visit(node.value)
        declare = self.inst_declare_var_global
        inst_str = self.inst_str
        if self.cur_function != 'premain':
            declare = self.inst_declare_var_local
            inst_str = self.inst_str_local
            self.local_variables.append(node.name)
        # const declaration
        self.program[self.cur_function]['code'].append((declare[value_type], node.name))
        # store register in the constant (although is the same as variable in SSA)
        self.program[self.cur_function]['code'].append((inst_str[value_type], node.value.register, node.name))

    def visit_VarDeclaration(self, node):
        value_type = node.datatype.name
        self.visit(node.value)
        declare = self.inst_declare_var_global
        if self.cur_function != 'premain':
            declare = self.inst_declare_var_local
            self.local_variables.append(node.name)
        # var declaration
        self.program[self.cur_function]['code'].append((declare[value_type], node.name))
        if node.value != None:
            inst_str = self.inst_str
            if self.cur_function != 'premain':
                inst_str = self.inst_str_local
            # store register in the variable (initialize the variables)
            self.program[self.cur_function]['code'].append((inst_str[value_type], node.value.register, node.name))
    
    def visit_SimpleType(self, node):
        pass

    def visit_SimpleLocation(self, node):
        location_is_local = False
        if node.name in self.local_variables: location_is_local = True
        if self.access_mode == 'read':
            load_inst = self.inst_load_local if location_is_local else self.inst_load
            target = self.new_register()
            self.program[self.cur_function]['code'].append((load_inst[node.type.name], node.name, target))
            node.register = target
        if self.access_mode == 'write':
            str_inst = self.inst_str_local if location_is_local else self.inst_str
            self.program[self.cur_function]['code'].append((str_inst[node.type.name], self.write_register, node.name))

    def visit_ReadValue(self, node):
        self.access_mode = 'read'
        self.visit(node.location)
        node.register = node.location.register
    
    def visit_Assignment(self, node):
        self.visit(node.value)
        self.access_mode = 'write'
        self.write_register = node.value.register
        self.visit(node.location)

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)
        op = node.op
        if node.type.name == 'bool':
            code = self.get_bool_binopcodes(node.op, node.left.type.name)
            if not code:
                raise RuntimeError(f'Unknown binop {op} in comparison')
            target = self.new_register()
            inst = (code, op, node.left.register, node.right.register, target)
            if code in ["AND", "OR"]:
                inst = (code, node.left.register, node.right.register, target)
            self.program[self.cur_function]['code'].append(inst)
            node.register = target
            return None
        code = self.binopcodes[node.type.name].get(op, None)
        if not code:
            raise RuntimeError(f'Unknown binop {op}')
        target = self.new_register()
        inst = (code, node.left.register, node.right.register, target)
        self.program[self.cur_function]['code'].append(inst)
        node.register = target
    
    def visit_UnaryOp(self, node):
        # We must convert -x to 0 - x
        # when +x we do not do anything
        # If type is integer should use the int instruction set
        self.visit(node.operand)
        datatype = node.type.name
        result_register = node.operand.register
        if node.op == '-':
            zero_register = self.new_register()
            result_register = self.new_register()
            if datatype == "int":
                self.program[self.cur_function]['code'].append(('MOVI', 0, zero_register))
                self.program[self.cur_function]['code'].append(('SUBI', zero_register, node.operand.register, result_register))
            if datatype == "float":
                self.program[self.cur_function]['code'].append(('MOVF', 0.0, zero_register))
                self.program[self.cur_function]['code'].append(('SUBF', zero_register, node.operand.register, result_register))
        if node.op == '!':
            # has to be boolean, so i just have to work with int(1) {0,1}
            one_register = self.new_register()
            result_register = self.new_register()
            self.program[self.cur_function]['code'].append(('MOVI', 1, one_register))
            self.program[self.cur_function]['code'].append(('XOR', one_register, node.operand.register, result_register)) # XOR 1 x if x == 1: 0 if x == 0: 1
        node.register = result_register
            
    def visit_PrintStatement(self, node):
        self.visit(node.value)
        code = self.print_types[node.value.type.name]
        inst = (code, node.value.register)
        self.program[self.cur_function]['code'].append(inst)

    def visit_CoderStatement(self, node):
        self.visit(node.inputp)
        self.visit(node.outputp)
        inst = ("CODER", node.inputp.register, node.outputp.register)
        self.program[self.cur_function]['code'].append(inst)
    
    def visit_DecoderStatement(self, node):
        self.visit(node.inputp)
        self.visit(node.outputp)
        inst = ("DECODER", node.inputp.register, node.outputp.register)
        self.program[self.cur_function]['code'].append(inst)
    
    def visit_IfStatement(self, node):
        self.visit(node.test)
        block_if = self.new_block()
        block_orelse = None
        if node.orelse:
            block_orelse = self.new_block()
        block_merge = self.new_block()
        if_branch_inst = ('CBRANCH', node.test.register, block_if, block_merge if not block_orelse else block_orelse)
        
        self.program[self.cur_function]['code'].append(if_branch_inst)
        self.program[self.cur_function]['code'].append(('LABEL', block_if))
        not_return_in_if_block = True
        for statement in node.body:
            self.visit(statement)
            if isinstance(statement, ast.ReturnStatement):
                not_return_in_if_block = False
                break
        if not_return_in_if_block:
            self.program[self.cur_function]['code'].append(('BRANCH', block_merge)) # solo tiene hacer este branch si no hay ningun return en el bloque del if en cuanto hay un return todo lo demas se ignora
                                                                                # ya que no pueden añadirse instrucciones a un bloque llvm una vez se ha hecho el return
        if block_orelse:
            self.program[self.cur_function]['code'].append(('LABEL', block_orelse))
            not_return_in_else_block = True
            for statement in node.orelse:
                self.visit(statement)
                if isinstance(statement, ast.ReturnStatement):
                    not_return_in_else_block = False
                    break
            if not_return_in_else_block: # igual que en el if
                self.program[self.cur_function]['code'].append(('BRANCH', block_merge))
        
        self.program[self.cur_function]['code'].append(('LABEL', block_merge))

    def visit_WhileStatement(self, node):
        block_startloop = self.new_block()
        self.program[self.cur_function]['code'].append(('BRANCH', block_startloop))
        self.program[self.cur_function]['code'].append(('LABEL', block_startloop))
        block_while = self.new_block()
        block_merge = self.new_block()
        self.visit(node.test)
        cond_branch_inst = ('CBRANCH', node.test.register, block_while, block_merge)
        self.program[self.cur_function]['code'].append(cond_branch_inst)
        self.program[self.cur_function]['code'].append(('LABEL', block_while))
        non_return_in_while_block = True
        for statement in node.body:
            self.visit(statement)
            if isinstance(statement, ast.ReturnStatement):
                non_return_in_while_block = False
                break
        if non_return_in_while_block:
            self.program[self.cur_function]['code'].append(('BRANCH', block_startloop))
        self.program[self.cur_function]['code'].append(('LABEL', block_merge))
    
    def visit_ReturnStatement(self, node):
        self.visit(node.value)
        target = self.new_register()
        self.program[self.cur_function]['code'].append(('RET', node.value.register))
    
    def visit_ArgumentDeclaration(self, node):
        self.local_variables.append(node.name)

    def visit_FunctionDef(self, node):
        self.program[node.name] = {'function_name': node.name, 'params_types': [], 'code': [], 'return_type': node.type.name, 'params_labels': []}
        self.local_variables.clear()
        self.cur_function = node.name
        # Hacer un 
        for arg in node.args:
            self.program[node.name]['params_types'].append(arg.type.name)
            self.program[node.name]['params_labels'].append(arg.name)
            self.visit(arg)
        for statements in node.body:
            self.visit(statements)
        
        if not isinstance(node.body[-1], ast.ReturnStatement):
            self.visit(ast.ReturnStatement(ast.IntegerLiteral(0)))
        self.cur_function = 'premain'
    
    def visit_Call(self, node):
        params_register = [] 
        for param in node.params:
            self.visit(param)
            params_register.append(param.register)
        target = self.new_register()
        instr = ('CALL', node.func.func_name, *params_register, target)
        self.program[self.cur_function]['code'].append(instr)
        node.register = target


def compile_ircode(source):
    '''
    Generate intermediate code from source.
    '''
    from .parser import parse
    from .checker import check_program
    from .errors import errors_reported

    ast = parse(source)
    check_program(ast)

    # If no errors occurred, generate code
    if not errors_reported():
        gen = GenerateCode()
        gen.visit(ast)
        import json
        # print(json.dumps(gen.program, indent=4))
        return gen.program # should be a list of functions 
    else:
        return []

def main():
    import sys

    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python3 -m gone.ircode filename\n")
        raise SystemExit(1)

    source = open(sys.argv[1]).read()
    code = compile_ircode(source)
    print(code)
    pdb.set_trace()
    for instr in code:
        print(instr)

if __name__ == '__main__':
    main()
