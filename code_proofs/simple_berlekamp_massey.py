from random import randint
from copy import deepcopy
import pdb
'''
Straightforward berlekamp massey implementation
for sequence of numbers in base 10.

Author: Pedro Castro
'''

def simple_berlekampmassey(s):
    c = []
    oldc = []
    f = -1
    for i in range(len(s)):
        delta = s[i]
        for j in range(1, len(c)+1):
            delta -= c[j-1] * s[i-j]
        if delta == 0: continue
        if f == -1:
            c = [0 for r in range(i+1)]
            f = i
        else:
            print("fallo i: ", i)
            d = [-x for x in oldc]
            d.insert(0, 1)
            df1 = 0 # d(f+1)
            for j in range(1, len(d)+1):
                df1 += d[j-1] * s[f+1-j]
            assert df1 != 0
            print("df1: ",df1)
            coef = delta / df1
            print("delta/df1 ", coef)
            for j in range(len(d)):
                d[j] *= coef
            left_zeros_shift = [0 for z in range(i - f - 1)]
            d = left_zeros_shift + d
            print("final d: ", d)
            temp = deepcopy(c)
            if len(c) < len(d):
                c.extend([0 for m in range(len(d) - len(c))])
            for j in range(len(d)):
                c[j] += d[j]
            print("final c", c)
            print("f: ", f)
            if i - len(temp) > f - len(oldc):
                print("actualiza oldc")
                oldc = temp
                f = i
    return c

# test
if __name__ == "__main__":
    seq = [1, 3, 9, 15, 9, -81]
    print(simple_berlekampmassey(seq))
