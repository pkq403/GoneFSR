def KnuthMorrisPratt(text, pattern):
 
    '''Yields all starting positions of copies of the pattern in the text.
Calling conventions are similar to string.find, but its arguments can be
lists or iterators, not just strings, it returns all matches, not just
the first one, and it does not need the whole text in memory at once.
Whenever it yields, it will have read the text exactly up to and including
the match that caused the yield.'''
 
    # allow indexing into pattern and protect against change during yield
    pattern = list(pattern)
    max_length = len(pattern)
    # build table of shift amounts
    shifts = [1] * (max_length + 1)
    shift = 1
    for pos in range(max_length):
        while shift <= pos and pattern[pos] != pattern[pos-shift]:
            shift += shifts[pos-shift]
        shifts[pos+1] = shift
    # do the actual search
    startPos = 0
    matchLen = 0
    max_found = 0
    max_pos = 0
    for c in text:
        while matchLen == max_length or \
              matchLen >= 0 and pattern[matchLen] != c:
            startPos += shifts[matchLen]
            matchLen -= shifts[matchLen]
        matchLen += 1
        if matchLen > max_found: # Despues de la primera coincidencia total este if deja de ser util
            max_found = matchLen
            max_pos = startPos
    return max_found, max_pos # devuelve cuantos caracteres matchean del patron, en que posicion empieza el primer match
