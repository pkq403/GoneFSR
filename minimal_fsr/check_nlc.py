import pdb
import sys
from random import randrange
from non_linear_compl import non_linear_complexity
from utils import verify_mfsr
from common.termcolor import GREEN, RED, ENDCOLOR

'''
Test File to test
minimal feedback shift register
method of a binary sequence
Author: Pedro Castro
'''
if __name__=="__main__":
    s = [randrange(2) for i in range(int(sys.argv[1]))]
    l = len(s)
    print("[!] text size: ", l)
    nlc = non_linear_complexity(s,l)
    print("[!] non linear complexity: ")
    print("m : ", nlc.m)
    print(nlc)
    print("[!] Bit Poly Terms Array")
    print(nlc.get_binary_terms_poly())
    # pdb.set_trace()
    print("[!] Checking coding/compression ...")
    decoded_seq = verify_mfsr(s,nlc.__str__(), nlc.m)
    if s == decoded_seq:
        print("[!] Son iguales !")
    else:
        print("[x] Distintas ")
        print("\t original: ", s)
        print("\t recupera: ", decoded_seq)
    print("[!] text: ", GREEN, "".join(str(i) for i in s[:nlc.m]), ENDCOLOR, RED, "".join(str(i) for i in s[nlc.m:]), ENDCOLOR)
