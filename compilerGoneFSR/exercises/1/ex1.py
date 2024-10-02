# Ejercicio 1 pero utilizando SLY (herramienta especializada en tokenizacion)
# Ejercicio escrito por Pedro Castro
from sly import Lexer

class SimpleLexer(Lexer):
    tokens = { NUMBER, ID, ASSIGN, PLUS, LPAREN, RPAREN, TIMES, 
              LE, LT,  GT, GE, EQ, NE, IF, ELSE, WHILE }

    ignore = ' \t'

    NUMBER = r'\d+'
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE
    PLUS = r'\+'
    LPAREN = r'\('
    RPAREN = r'\)'
    TIMES = r'\*'
    LT = r'<'
    LE = r'<='
    GE = r'>='
    GT = r'>'
    EQ = r'=='
    NE = r'!='
    ASSIGN = '='

    def error(self, t):
        print('Bad character %r' % t.value[0])
        self.index += 1
    
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

if __name__ == '__main__':
    text = 'abc 123 $ cde 456'
    text2 = 'a = 3 + (4 * 5)'
    text3 = '''
           a < b
           a <= b
           a > b
           a >= b
           a == b
           a != b
    '''
    text4 = '''
           if a < b
           else a <= b
           while a > b
           a >= b
           a == b
           a != b
    '''
    lexer= SimpleLexer()
    for tok in lexer.tokenize(text4):
        print(tok)