from collections import deque
from knuthMorrisPratt import KnuthMorrisPratt

def eigenvalue(s,n):
    '''
    suffix = s[:n-1] (pattern)
    text = suffix[1:]
    return j; 1 <= j <= n-1
    '''
    suffix = deque()
    s0 = iter(s)
    length = 0
    while length < n:
        suffix.appendleft(next(s0))
        length += 1
    text = iter(suffix)
    next(text)
    return( n - KnuthMorrisPratt(text,suffix)[0])
