#import pdb
'''
Lexer
Author: Pedro Castro
'''
r'''
Reserved Keywords:
    CONST   : 'const'
    VAR     : 'var'  
    PRINT   : 'print'

Identifiers:
    ID      : Text starting with a letter or '_', followed by any number
              number of letters, digits, or underscores.
              Examples:  'abc' 'ABC' 'abc123' '_abc' 'a_b_c'

Operators and Delimiters:
    PLUS     : '+'
    MINUS    : '-'
    TIMES    : '*'
    DIVIDE   : '/'
    ASSIGN   : '='
    SEMI     : ';'
    LPAREN   : '('
    RPAREN   : ')'
    LCURLY   : '{'
    RCURLY   : '}'

Literals:
    INTEGER :  123   (decimal)

    FLOAT   : 1.234
              .1234
              1234.

    CHAR    : 'a'     (a single character - byte)
              '\''    The quote
              '\n'    Newline
              '\\'    Backslash
              '\xhh'  (byte value)

    STRING : ".*"
Comments:  To be ignored by your lexer
     //             Skips the rest of the line
     /* ... */      Skips a block (no nesting allowed)

Errors: 

     lineno: Illegal char 'c'         
     lineno: Unterminated character constant     
     lineno: Unterminated comment
'''

from .errors import error

from sly import Lexer

class GoneLexer(Lexer):

    tokens = {
        # keywords
        CONST, VAR, PRINT, CODER, DECODER, FUNC, RET,
                 
        # Identifiers
        ID, IF, ELSE, WHILE,

        # Literals
        INTEGER, FLOAT, CHAR, BOOL, STRING,

        # ASSIGN
        ASSIGN,

        # Logical Operators
        AND, OR, NOT, EQ, NE, LT, LE, GT, GE,

        # Operators 
        PLUS, MINUS, TIMES, DIVIDE,

        # Other symbols
        LPAREN, RPAREN, LCURLY, RCURLY, SEMI, COMMA }
    
    CONST = r"\bconst\b"
    VAR = r"\bvar\b"
    PRINT = r"\bprint\b"
    CODER = r"\bcoder\b"
    DECODER = r"\bdecoder\b"
    FUNC = r'\bfunc\b'
    RET = r'\breturn\b'

 
    # --> Ignored characters (whitespace)
    ignore = ' \t\r'


    # block-style comment (/* ... */)
    @_(r'/\*(\*(?!\/)|[^*])*\*/')
    def ignore_mult_comment(self, t):
        self.lineno += t.value.count('\n')
        
    # line-style comment (//...)
    @_(r'//.*')
    def ignore_line_comment(self, t):
        pass

    # One or more newlines \n\n\n...
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    # Unterminated multiple line comment
    @_(r'/\*.*')
    def unterminated_multiple_comment(self, t):
        self.lineno += t.value.count('\n')
        error(self.lineno,"Unterminated comment")

    # <-- Ignored characters (whitespace)

    # Logical operators (CUIDADO, el orden de definicion importa)
    AND = r'&&'
    OR = r'\|\|'
    LE = r'<='
    LT = r'<'
    GE = r'>='
    GT = r'>'
    EQ = r'=='
    NE = r'!='
    NOT = '!'
    ASSIGN = '='

    # Arithmetic operators
    PLUS = r'\+'      # Regex for a single plus sign
    MINUS = r'-'      # Regex for a single minur sign
    TIMES = r'\*'
    DIVIDE = r'/'
    LPAREN = r'\('
    RPAREN = r'\)'
    LCURLY = r'\{'
    RCURLY = r'\}'
    SEMI = ';'
    COMMA = ','


    FLOAT = r'\d+\.\d+e[+-]?\d+|\d+\.\d*|\.\d+'
    INTEGER = r'0x[a-f0-9]+|0o[0-7]+|0b[10]+|\d+'


    CHAR = r"'(?:\\(?:\\|n|x[0-9a-f]{2}|')|[^'\\])'"
    STRING = r"\".*\""

    @_(r"'.*")
    def unlimited_character(self, t):
        error(self.lineno,"Unterminated character literal")
        self.index += 1
    
    BOOL = r"\btrue\b|\bfalse\b"
    
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE

    # Bad character error handling
    def error(self, t):
        error(self.lineno,"Illegal character %r" % t.value[0])
        self.index += 1
    
def main():
    '''
    Main program. For debugging purposes.
    '''
    import sys
    
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python3 -m gone.tokenizer filename\n")
        raise SystemExit(1)

    lexer = GoneLexer()
    text = open(sys.argv[1]).read()
    for tok in lexer.tokenize(text):
        print(tok)

if __name__ == '__main__':
    main()

