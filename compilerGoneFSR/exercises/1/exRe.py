import re
import warnings as warn

ID = r'(?P<ID>[a-zA-Z_][a-zA-Z0-9_]*)'
NUMBER = r'(?P<NUMBER> \d+)'
SPACE = r'(?P<SPACE>\s+)'

patterns = [ID, NUMBER, SPACE]

pat = re.compile('|'.join(patterns))

def tokenize(text):
    index = 0
    while index < len(text):
        m = pat.match(text, index)
        if m:
            if m.lastgroup != 'SPACE':
                yield (m.lastgroup, m.group())
            index = m.end()
        else:
            #raise SyntaxError('Bad char %r' % text[index])
            warn.warn("Bad char %r" % text[index])
            index += 1
        


text = "abc 123 cde 456"
text2 = "abc 123 $ cde 456"
for tok in tokenize(text2): print(tok)