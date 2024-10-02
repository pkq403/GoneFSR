'''
Implementacion sencilla de
calculo de los eigenwords y eigenvalue
de una secuencia binaria
Autor: Pedro Castro
'''
import sys
import copy
from common.termcolor import ENDCOLOR, RED, GREEN

def get_combinations(lst, k):
    combs = set()
    counter = 0
    while counter + k <= len(lst):
        combs.add(tuple(lst[counter:counter+k]))
        counter += 1
    return list(combs)

def get_vocabulary(seq):
    vocabulary = []
    for k in range(1, len(seq)+1):
        vocabulary.extend(get_combinations(seq, k))
    return vocabulary

def get_eigenwords(seq, vocab):
    proper_prefixes = seq[:-1]
    vocab_proper_prefixes = set(get_vocabulary(proper_prefixes))
    return list(set(vocab) - set(vocab_proper_prefixes))

if __name__=="__main__":
    seq = [int(i) for i in sys.argv[1]]
    print(f"{RED}[*]{ENDCOLOR} sequence(y^{len(seq)}): {seq}")
    seq_vocabulary = get_vocabulary(seq)
    lst_seq_vocabulary = sorted(seq_vocabulary, key=len)
    seq_eigenwords = sorted(get_eigenwords(seq, seq_vocabulary), key=len)
    print(f"{GREEN}[*]{ENDCOLOR} vocabulary: {lst_seq_vocabulary}")
    print(f"{GREEN}[*]{ENDCOLOR} eigenwords: {seq_eigenwords}")
    print(f"{GREEN}[*]{ENDCOLOR} eigenvalue(k(y^{len(seq)})): {len(seq_eigenwords)}")
    seq_eigenvalue_profile = []
    for i in range(1, len(seq)+1):
        seq_eigenvalue_profile.append(len(get_eigenwords(seq[:i], get_vocabulary(seq[:i]))))
    print(f"{GREEN}[*]{ENDCOLOR} eigenvalue profile (y^{len(seq)}): {seq_eigenvalue_profile}")


