# import pdb
'''
Parser Gone FSR
Author: Pedro Castro
'''
'''
program : statements
        | empty

statements :  statements statement
           |  statement

statement :  const_declaration
          |  var_declaration
          |  assign_statement
          |  print_statement
          |  if_statement
          |  while_statement
          |  return_statement

const_declaration : CONST ID = expression ;

var_declaration : VAR ID datatype ;
                | VAR ID datatype = expression ;

assign_statement : location = expression ;

print_statement : PRINT expression ;

coder_statement: CODER expression , expression ;

decoder_statement: DECODER expression , expression ;


if_statement : IF expression { statements }
             | IF expression { statements } ELSE { statements }
             
while_statement: WHILE expression { statements }

function_definition : FUNC ID LPAREN arguments RPAREN datatype { statements }

parameters: parameter
           | parameters COMMA parameter
           | expression
           | empty

function_calling: function_location LPAREN parameters RPAREN SEMI

arg_declaration: ID datatype

arguments: argument
           | arguments comma argument
           | arg_declaration
           | empty

expression : + expression
           | - expression
           | ! expression
           | expression && expression
           | expression || expression
           | expression == expression
           | expression != expression
           | expression < expression
           | expression <= expression
           | expression > expression
           | expression >= expression
           | expression + expression
           | expression - expression
           | expression * expression           
           | expression / expression
           | ( expression )
           | location
           | literal
           | function_call
               

literal : INTEGER     
        | FLOAT       
        | CHAR     
        | BOOL 

function_location: ID

location : ID
         ;

datatype : ID
         ;

empty    :

'''

from sly import Parser

from .errors import error

from .tokenizer import GoneLexer

from .ast import *

class GoneParser(Parser):
    # Same token set as defined in the lexer
    tokens = GoneLexer.tokens

    precedence = (
        ('left', 'OR', 'AND'),
        ('nonassoc', 'LT', 'GT'),  # Nonassociative operators
        ('left','LE', 'GE', 'EQ', 'NE'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('right', 'NOT'),
    )

    @_('statement')
    def statements(self, p):
        return [ p.statement ]

    @_('statements statement')
    def statements(self, p):
        p.statements.append(p.statement)
        return p.statements

    @_('coder_statement', 'decoder_statement','print_statement', 'assign_statement', 'const_declaration', 'var_declaration', 
       'if_statement', 'while_statement', 'function_definition', 'return_statement', 
       'function_calling')
    def statement(self, p):
        return p[0]
    
    # ---- Statements ----
    @_('PRINT expression SEMI') # print statement
    def print_statement(self, p):
        return PrintStatement(p.expression, lineno = p.lineno)
    
    @_('CODER expression COMMA expression SEMI')
    def coder_statement(self, p):
        return CoderStatement(p.expression0, p.expression1, lineno=p.lineno)
    
    @_('DECODER expression COMMA expression SEMI')
    def decoder_statement(self, p):
        return DecoderStatement(p.expression0, p.expression1, lineno=p.lineno)
    
    @_('ID ASSIGN expression SEMI') # assign statement
    def assign_statement(self, p):
        return Assignment(SimpleLocation(p.ID, lineno = p.lineno), p.expression, lineno = p.lineno)
    
    @_('RET expression SEMI') # return statement
    def return_statement(self, p):
        return ReturnStatement(p.expression, lineno = p.lineno)
    
    # ---- Functions Definition ----
    @_('FUNC ID LPAREN arguments RPAREN datatype LCURLY statements RCURLY')
    def function_definition(self, p):
        return FunctionDef(p.ID, SimpleType(p.datatype, lineno = p.lineno), p.arguments, p.statements, lineno=p.lineno)
    
    # ---- Functions Args ----
    @_('argument')
    def arguments(self, p):
        return [ p.argument ]
    
    @_('arguments COMMA argument')
    def arguments(self, p):
        p.arguments.append(p.argument)
        return p.arguments
    
    @_('')
    def arguments(self, p):
        return []
    
    @_('arg_declaration')
    def argument(self, p):
        return p[0]
    
    @_('ID datatype')
    def arg_declaration(self, p):
        return ArgumentDeclaration(p.ID, SimpleType(p.datatype, lineno=p.lineno), lineno = p.lineno)

    # ---- Control Flow ---
    @_('IF expression LCURLY statements RCURLY')
    def if_statement(self, p):
        return IfStatement(p.expression, p.statements, None, lineno = p.lineno)
    
    @_('IF expression LCURLY statements RCURLY ELSE LCURLY statements RCURLY')
    def if_statement(self, p):
        return IfStatement(p.expression, p.statements0, p.statements1, lineno = p.lineno)

    # TODO IMPORTANT: evaluate empty blocks, Now it detects a sintax fail if any block is empty    
    # @_('IF expression LCURLY  RCURLY') # empty if
    # def if_statement(self, p):
    #     return IfStatement(p.expression, None, None, lineno = p.lineno)
    
    @_('WHILE expression LCURLY statements RCURLY')
    def while_statement(self, p):
        return WhileStatement(p.expression, p.statements, lineno = p.lineno)
    
    # ---- Declarations ----
    @_('CONST ID ASSIGN expression SEMI')
    def const_declaration(self, p):
        return ConstDeclaration(p.ID, p.expression, lineno = p.lineno)
    
    @_('VAR ID datatype SEMI')
    def var_declaration(self, p):
        return VarDeclaration(p.ID, SimpleType(p.datatype, lineno = p.lineno), None, lineno = p.lineno)

    @_('VAR ID datatype ASSIGN expression SEMI')
    def var_declaration(self, p):
        return VarDeclaration(p.ID, SimpleType(p.datatype, lineno = p.lineno), p.expression, lineno = p.lineno)        
    
    @_('function_location LPAREN parameters RPAREN SEMI')
    def function_calling(self, p):
        return Call(p.function_location, p.parameters, lineno=p.lineno)
    
    @_('location')
    def function_location(self, p):
        return ReadFunction(FunctionLocation(p.location, lineno = p.lineno), lineno = p.lineno)
    
    # ---- expression ---- 
    # TODO: Deberia de haber statements que sean las expresiones con ; ? 
    # para poder hacer 2 + 3; sin que ese resultado se guarde en ningun sitio? (en c se puede)
    @_('NOT expression', 'PLUS expression', 'MINUS expression')
    def expression(self, p):
        return UnaryOp(p[0], p.expression, lineno = p.lineno)
    
    @_('expression PLUS expression', 'expression MINUS expression', 'expression TIMES expression', 
       'expression DIVIDE expression','expression EQ expression', 'expression NE expression', 
       'expression GT expression','expression GE expression','expression LT expression',
       'expression LE expression', 'expression AND expression', 'expression OR expression')
    def expression(self, p):
        return BinOp(p[1], p.expression0, p.expression1, lineno = p.lineno)
    
    @_('LPAREN expression RPAREN')
    def expression(self, p):
        return p.expression
    
    @_('location') 
    def expression(self, p):
        return ReadValue(SimpleLocation(p.location, lineno = p.lineno), lineno = p.lineno)
    
    @_('literal')
    def expression(self, p):
        return p.literal
    
    # ---- Function Calls ----
    @_('function_location LPAREN parameters RPAREN')
    def expression(self, p):
        return Call(p.function_location, p.parameters, lineno=p.lineno)
    
    # ---- parameters ----
    @_('parameter')
    def parameters(self, p):
        return [ p.parameter ]
    
    @_('parameters COMMA parameter')
    def parameters(self, p):
        p.parameters.append(p.parameter)
        return p.parameters
    
    @_('')
    def parameters(self, p):
        return []
    
    @_('expression')
    def parameter(self, p):
        return p[0]
    
    # --- literals ---
    @_('INTEGER')
    def literal(self, p):
        return IntegerLiteral(int(p.INTEGER), lineno = p.lineno)

    @_('FLOAT')
    def literal(self, p):
        return FloatLiteral(float(p.FLOAT), lineno = p.lineno)

    @_('CHAR')
    def literal(self, p):
        return CharLiteral(eval(p.CHAR), lineno = p.lineno)
    
    @_('BOOL')
    def literal(self, p):
        return BoolLiteral(p.BOOL == 'true', lineno = p.lineno)

    @_('STRING')
    def literal(self, p):
        return StringLiteral(eval(p.STRING), lineno = p.lineno)
    
    @_('ID')
    def location(self, p):
        return p.ID
    
    @_('ID')
    def datatype(self, p):
        return p.ID
    
    def error(self, p):
        if p:
            error(p.lineno, "Syntax error in input at token '%s'" % p.value)
        else:
            error('EOF','Syntax error. No more input.')


def parse(source):
    '''
    Parse source code into an AST. Return the top of the AST tree.
    '''
    lexer = GoneLexer()
    parser = GoneParser()
    ast = parser.parse(lexer.tokenize(source))
    return ast

def main():
    '''
    Main program. Used for testing.
    '''
    import sys

    if len(sys.argv) != 2:
        sys.stderr.write('Usage: python3 -m gone.parser filename\n')
        raise SystemExit(1)

    # Parse and create the AST
    ast = parse(open(sys.argv[1]).read())

    # Output the resulting parse tree structure
    for depth, node in flatten(ast):
        print('%s: %s%s' % (getattr(node, 'lineno', None), ' '*(4*depth), node))

if __name__ == '__main__':
    main()
