'''
Semantic Analysis
Author: Pedro Castro
'''
from .errors import error
from .ast import *
from .typesys import IntType, FloatType, CharType, StringType, BoolType, Type, check_binop, check_unaryop

class CheckProgramVisitor(NodeVisitor):
    def __init__(self):
        # Initialize the symbol table
        self.symbols = { }
        self.local_symbols = { }
        self.returned_branches = [] # Lista a la que se añade un booleano cada vez que se bifurca el flow del programa en una funcion, siendo True si ese Flow retorna o False si no retorna nada
                                  # Este registro solamente es necesario verificarlo si la funcion en su flujo principal no retorna
        self.functions = { } # functions table, should be initialized with built-in functions( o no, antes no tenia print, y entendia bien la funcion print, cambiar cuando toque)
        self.cur_function = None # current function
        self.global_code = True
        self.symbols.update({'types': {'int': IntType, 'float': FloatType, 'char': CharType, 'string': StringType, 'bool': BoolType}})
        self.builtin_types = ['int', 'float', 'char']

    # Private Auxiliary Methods ...
    def _checkIfExistsDeprecatedCode(self, statement_index, statementbody_len, node_lineno, node_name):
        if statement_index != statementbody_len - 1: error(node_lineno, f"Deprecated code after the return statement in function {node_name}") # ?? should be a warning
        

    # NODE Methods ...
    def visit_ArgumentDeclaration(self, node):
        total_symbols = self.symbols | self.local_symbols # union entre simbolos locales y globales
        location_node = total_symbols.get(node.name, None)
        if location_node:
            error(node.lineno, f"can't declare {node.name} as an arg, a symbol with that name already exists")
            return None 
        self.visit(node.datatype)
        node.type = node.datatype.type
        node.scope = 'local'
        self.local_symbols[node.name] = node

    def visit_ConstDeclaration(self, node):
        if node.name in self.builtin_types:
            error(node.lineno, f"{node.name} redefined. Previous definition on <builtin type>")
            return None
        table = self.symbols if self.global_code else self.local_symbols
        previous_instance = table.get(node.name, None)
        if not previous_instance:
            self.visit(node.value)
            node.type = node.value.type
            # node.scope = 'global' if self.global_code else 'local' (comentado por ahora, porque cualquier declaracion hecha en una funcion se toma como local)
            self.symbols[node.name] = node
        else:
            print("%s: %s redefined. Previous definition on %s" % (node.lineno, node.name, previous_instance.lineno))
    
    def visit_SimpleType(self, node):
        # Associate a type name such as "int" with a Type object
        node.type = self.symbols['types'].get(node.name, None)
        if node.type is None:
            error(node.lineno, f"unknown type name {node.name}")

    def visit_VarDeclaration(self, node):
        if node.name in self.builtin_types:
            error(node.lineno, f"{node.name} redefined. Previous definition on <builtin type>")
            return None
        table = self.symbols if self.global_code else self.local_symbols
        previous_instance = table.get(node.name, None)
        if not previous_instance:
            self.visit(node.datatype)
            self.visit(node.value)
            node.type = node.datatype.type
            # Check that the value matches defined type
            if node.type != None and node.value != None and node.type != node.value.type:
                error(node.lineno, f"type error. {node.type.name} = {node.value.type.name}")    
            # node.scope = 'global' if self.global_code else 'local' (comentado por ahora, porque cualquier declaracion hecha en una funcion se toma como local)
            self.symbols[node.name] = node

        else:
            error(node.lineno, "%s redefined. Previous definition on %s" % (node.name, previous_instance.lineno))

    def visit_SimpleLocation(self, node):
        node.type = Type
        total_symbols = self.symbols | self.local_symbols
        location_node = total_symbols.get(node.name, None)
        if not location_node and node.usage == 'read':
            error(node.lineno, f"Can't read from {node.name}")
            return None
        if not location_node and node.usage == "write":
            error(node.lineno, f"Can't assign to {node.name}")
            return None
        if not location_node:
            error(node.lineno, "%s undefined" % node.name)
            return None
        if node.usage == "write" and not isinstance(location_node, VarDeclaration) and not isinstance(location_node, ArgumentDeclaration):
            #print(location_node)
            error(node.lineno, f"Cant assign to {node.name}")
            return None
        node.type = location_node.type

    def visit_FunctionLocation(self, node):
        node.type = Type
        node.args_number = 'undefined'
        node.args_type = ['undefined']
        function_location_node = self.functions.get(node.name, None)
        if not function_location_node: # Revisa si la funcion esta definida o si es built-in
            error(node.lineno, "%s undefined function" % node.name)
            return None
        node.type = function_location_node.type
        node.args_number = len(function_location_node.args)
        node.args_type = [a.datatype.name for a in function_location_node.args]

    def visit_IntegerLiteral(self, node):
        node.type = IntType
    
    def visit_FloatLiteral(self, node):
        node.type = FloatType

    def visit_CharLiteral(self, node):
        node.type = CharType
    
    def visit_BoolLiteral(self, node):
        node.type = BoolType
    
    def visit_StringLiteral(self, node):
        node.type = StringType

    def visit_Assignment(self, node):
        node.location.usage = 'write'
        self.visit(node.value) 
        self.visit(node.location)
        # Check if the name is a builtin type
        if node.location.type != node.value.type:
            error(node.lineno, f"type error. {node.location.type.name} = {node.value.type.name}")
        
    def visit_ReadFunction(self, node):
        self.visit(node.location)
        node.type = node.location.type
        node.args_number = node.location.args_number
        node.func_name = node.location.name
        node.args_type = node.location.args_type

    def visit_ReadValue(self, node):
        node.location.usage = 'read'
        self.visit(node.location)
        node.type = node.location.type

    def visit_BinOp(self, node):
        # For operators, you need to visit each operand separately.  You'll
        # then need to make sure the types and operator are all compatible.
        self.visit(node.left)
        self.visit(node.right)
        if node.right.type == Type or node.left.type == Type:
            node.type = Type
            return None
        node.type = check_binop(node.left.type, node.op, node.right.type)
        # Perform various checks here
        if node.type == None:
            error(node.lineno, f"Unsupported operation {node.left.type.name} {node.op} {node.right.type.name}")   
            node.type =Type

    def visit_UnaryOp(self, node):
        self.visit(node.operand)
        if node.operand.type != Type:#  En caso de que el operando haya dado error no se propaga
            node.type = check_unaryop(node.op, node.operand.type)
            if node.type == None:
                error(node.lineno, f"Unsupported operation {node.op} {node.operand.type.name}")
            return None
        node.type = Type

    def visit_ReturnStatement(self, node):
        self.visit(node.value)
        node.type = node.value.type
        # Assert that the type you're returning is the same as the type of the function
        cur_function_type = self.functions[self.cur_function].type
        cur_function_type_name = 'undefined'if not cur_function_type else cur_function_type.name
        if node.type != cur_function_type:
            error(node.lineno, "return type %s in a function type %s " % (node.type.name, cur_function_type_name))
    
    def visit_PrintStatement(self, node):
        self.visit(node.value)
    
    def visit_CoderStatement(self, node):
        self.visit(node.inputp)
        self.visit(node.outputp)
        if node.inputp.type != StringType:
            error(node.lineno, f"Coder: input path is not an string")
        if node.outputp.type != StringType:
            error(node.lineno, f"Coder: output path is not an string")
    
    def visit_DecoderStatement(self, node):
        self.visit(node.inputp)
        self.visit(node.outputp)
        if node.inputp.type != StringType:
            error(node.lineno, f"Decoder: input path is not an string")
        if node.outputp.type != StringType:
            error(node.lineno, f"Decoder: output path is not an string")
            
    def visit_IfStatement(self, node):
        self.visit(node.test)
        if node.test.type != BoolType:
            error(node.lineno, f"Bad comparison: not bool expression")
        
        statement_body_len = len(node.body) # Esta optimizacion, la hago para que python no repita LOADS cuando pasa a IRCODE (se puede ver con el modulo dis)
        return_inst = False
        for i,statement in enumerate(node.body):
            self.visit(statement)
            if isinstance(statement, ReturnStatement):
                return_inst = True
                self._checkIfExistsDeprecatedCode(i, statement_body_len, node.lineno, 'if statement')
        self.returned_branches.append(return_inst)
        
        return_inst = False
        if node.orelse:
            statement_body_len = len(node.orelse)
            for i,statement in enumerate(node.orelse):
                self.visit(statement)
            if isinstance(statement, ReturnStatement):
                return_inst = True
                self._checkIfExistsDeprecatedCode(i, statement_body_len, node.lineno, 'else statement')
        self.returned_branches.append(return_inst) # Si no hay especificado un else se toma como que el bloque else no retorna nada
            
    def visit_WhileStatement(self, node):
        self.visit(node.test)
        if node.test.type != BoolType:
            error(node.lineno, f"Bad comparison: not bool expression")

        statement_body_len = len(node.body) # optimization
        return_inst = False
        for i, statement in enumerate(node.body):
            self.visit(statement)
            if isinstance(statement, ReturnStatement):
                return_inst = True
                self._checkIfExistsDeprecatedCode(i, statement_body_len, node.lineno, 'while statement')
        self.returned_branches.append(return_inst)

    def visit_FunctionDef(self, node):
        if not self.global_code: # If the function definition is already inside a function
            error(node.lineno, f'Not allowed nested fuction {node.name} inside function {self.cur_function}')
            return None
        
        # Save the function name in the global-symbols table
        previous_instance = self.symbols.get(node.name, None)
        if previous_instance: # If the name is already declared
            error(node.lineno, "%s redefined. Previous definition on %s" % (node.name, previous_instance.lineno))
            return None
        
        # --- function declaration ---    
        self.visit(node.datatype)
        node.type = node.datatype.type
        self.functions[node.name] = node
        #print("DEBUG NODE VALUE IN DICT FUNCTIONS: ", node) # linea de debug
        self.local_symbols.clear() # clear local symbols table
        self.returned_branches.clear() # clear del historial de retornos de los flujos
        self.global_code = False # Modo Local activado !
        main_flow_returns = False # True si se encuentra un return en el main flow de la funcion
        self.cur_function = node.name
        
        # Quizas sea necesario tambien un current block??

        # --- visiting args ---
        for arg in node.args:
            self.visit(arg)
        
        # --- visiting function body ---
        # 1. Detect all program flows and if every flow has a return
        '''
        ¿Como hacemos eso?
        Hay 2 opciones:
        Opcion 1: la funcion tiene un return al final de la funcion independientemente de las ramificaciones (ya que ese codigo sera incondicional)
        Opcion 2: la funcion no tiene un return al final de la funcion asi que hay que comprobar que todas las ramificaciones alcanzables tengan un return
        ''' 

        statement_body_len = len(node.body)
        for i, statement in enumerate(node.body):
            self.visit(statement)
            if isinstance(statement, ReturnStatement):
                main_flow_returns = True
                self._checkIfExistsDeprecatedCode(i, statement_body_len, node.lineno, node.name)
        
        # Trigger del analisis de caminos si no se ha encontrado un return como ultima instruccion de la funcion
        # Entonces analiza si todos los demas caminos tienen un return
        if not main_flow_returns and (not all(self.returned_branches) or not self.returned_branches):
            error(node.lineno, f"Not all flows returns in the function {node.name}")
        self.global_code = True # Vuelves al modo global por si el siguiente nodo no forma parte de ninguna funcion

    def visit_Call(self, node):
        self.visit(node.func)
        params_number = len(node.params)
        node.type = node.func.type
        if node.func.args_number != params_number:
            error(node.lineno, f"{node.func.func_name} takes {node.func.args_number} arguments, but you pass {params_number}")
            return None
        argindex = 0
        for p, argtype in zip(node.params, node.func.args_type):
            self.visit(p)
            if p.type.name != argtype and argtype != 'undefined':
                error(node.lineno, f"func {node.func.func_name}, args {argindex} of type {p.type.name} should be {argtype}")
            argindex += 1
    

def check_program(ast):
    '''
    Check the supplied program (in the form of an AST)
    '''
    checker = CheckProgramVisitor()
    checker.visit(ast)

def main():
    '''
    Main program. Used for testing
    '''
    import sys
    from .parser import parse

    if len(sys.argv) < 2:
        sys.stderr.write('Usage: python3 -m gone.checker filename\n')
        raise SystemExit(1)

    ast = parse(open(sys.argv[1]).read())
    check_program(ast)
    if '--show-types' in sys.argv:
        for depth, node in flatten(ast):
            print('%s: %s%s type: %s' % (getattr(node, 'lineno', None), ' '*(4*depth), node,
                                         getattr(node, 'type', None)))

if __name__ == '__main__':
    main()
