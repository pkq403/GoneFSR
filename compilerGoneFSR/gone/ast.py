'''
Abstract Syntax Tree (AST) objects.
Author: Pedro Castro
'''

class AST(object):
    _nodes = { } 

    @classmethod
    def __init_subclass__(cls):
        AST._nodes[cls.__name__] = cls

        if not hasattr(cls, '__annotations__'):
            return

        fields = list(cls.__annotations__.items())
                
        def __init__(self, *args, **kwargs):
            if len(args) != len(fields):
                raise TypeError(f'Expected {len(fields)} arguments')
            for (name, ty), arg in zip(fields, args):
                if isinstance(ty, list):
                    if not isinstance(arg, list):
                        raise TypeError(f'{name} must be list')
                    if not all(isinstance(item, ty[0]) for item in arg):
                        raise TypeError(f'All items of {name} must be {ty[0]}')
                elif not isinstance(arg, ty):
                    raise TypeError(f'{name} must be {ty}')
                setattr(self, name, arg)

            for name, val in kwargs.items():
                setattr(self, name, val)

        cls.__init__ = __init__
        cls._fields = [name for name,_ in fields]

    def __repr__(self):
        vals = [ getattr(self, name) for name in self._fields ]
        argstr = ', '.join(f'{name}={type(val).__name__ if isinstance(val, AST) else repr(val)}'
                           for name, val in zip(self._fields, vals))
        return f'{type(self).__name__}({argstr})'


# Abstract AST nodes
class Statement(AST):
    pass

class Expression(AST):
    pass

class DataType(AST):
    pass

class SimpleType(DataType):
    name : str

class Location(AST):
    pass

class SimpleLocation(Location):
    name : str

class FunctionLocation(Location):
    name : str

class Literal(Expression):
    '''
    A literal value such as 2, 2.5, or "two"
    '''
    pass

# Concrete AST nodes
class PrintStatement(Statement):
    '''
    print expression ;
    '''
    value : Expression

class CoderStatement(Statement):
    '''
    coder path0, path1 ;
    '''
    inputp : Expression
    outputp: Expression

class DecoderStatement(Statement):
    '''
    decoder path0, path1 ;
    '''
    inputp : Expression
    outputp: Expression

class Assignment(Statement):
    '''
    ID EQ expression ;
    '''
    location : Location
    value : Expression

class IfStatement(Statement):
    test: Expression
    body: list
    orelse: (list, type(None))

class WhileStatement(Statement):
    test: Expression
    body: list

class FunctionDef(Statement):
    name : str
    datatype : DataType
    args : list
    body : list

class ReturnStatement(Statement):
    value : Expression

class ArgumentDeclaration(Statement):
    name: str
    datatype : DataType

class ReadFunction(Expression):
    location : FunctionLocation

class Call(Expression):
    func : ReadFunction
    params : list

# Declarations
class ConstDeclaration(Statement):
    '''
    const name = value ;
    '''
    name : str
    value : Expression

class VarDeclaration(Statement):
    '''
    (inicializar la variable es opcional)
    var name datatype [ = value ];
    '''
    name : str
    datatype : DataType
    value : (Expression, type(None)) # Optional

class IntegerLiteral(Literal):
    value : int

class FloatLiteral(Literal):
    value : float

class CharLiteral(Literal):
    value : str

class BoolLiteral(Literal):
    value : bool

class StringLiteral(Literal):
    value : str

class BinOp(Expression):
    '''
    A Binary operator such as 2 + 3 or x * y
    '''
    op    : str
    left  : Expression
    right : Expression

class UnaryOp(Expression):
    '''
    Unary Operator such as - 2 or + 3
    '''
    op : str
    operand : Expression

class ReadValue(Expression):
    '''
    read a variable or a constant
    '''
    location : Location


# The following classes for visiting and rewriting the AST are taken
# from Python's ast module.   

class VisitDict(dict):
    def __setitem__(self, key, value):
        if key in self:
            raise AttributeError(f'Duplicate definition for {key}')
        super().__setitem__(key, value)
        
class NodeVisitMeta(type):
    @classmethod
    def __prepare__(cls, name, bases):
        return VisitDict()
    
class NodeVisitor(metaclass=NodeVisitMeta):
    def visit(self, node):
        '''
        Execute a method of the form visit_NodeName(node) where
        NodeName is the name of the class of a particular node.
        '''
        if isinstance(node, list):
            for item in node:
                self.visit(item)
        elif isinstance(node, AST):
            method = 'visit_' + node.__class__.__name__
            visitor = getattr(self, method, self.generic_visit)
            visitor(node)
    
    def generic_visit(self,node):
        '''
        Method executed if no applicable visit_ method can be found.
        This examines the node to see if it has _fields, is a list,
        or can be further traversed.
        '''
        for field in getattr(node, '_fields'):
            value = getattr(node, field, None)
            self.visit(value)

    @classmethod
    def __init_subclass__(cls):
        '''
        Sanity check. Make sure that visitor classes use the right names
        '''
        for key in vars(cls):
            if key.startswith('visit_'):
                assert key[6:] in globals(), f"{key} doesn't match any AST node"

def flatten(top):
    '''
    Flatten the entire parse tree into a list for the purposes of
    debugging and testing.  This returns a list of tuples of the
    form (depth, node) where depth is an integer representing the
    parse tree depth and node is the associated AST node.
    '''
    class Flattener(NodeVisitor):
        def __init__(self):
            self.depth = 0
            self.nodes = []
        def generic_visit(self, node):
            self.nodes.append((self.depth, node))
            self.depth += 1
            NodeVisitor.generic_visit(self, node)
            self.depth -= 1

    d = Flattener()
    d.visit(top)
    return d.nodes
