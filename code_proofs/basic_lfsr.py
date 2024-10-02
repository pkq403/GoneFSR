import sys
from common.termcolor import ENDCOLOR, RED, GREEN, MAGENTA
"""
Basic LFSR implementation
Author: Pedro Castro
"""

def lfsr(s, taps, k):
    for i in range(k):
        lfsr_res = int(s[taps[0]])
        for t in range(1, len(taps)):
            lfsr_res ^= int(s[taps[t]])
        s = str(lfsr_res) + s[:-1]
    return s


if __name__=="__main__":
    if len(sys.argv) < 3:
        print(RED + "[*]" + ENDCOLOR +" Help Panel: ")
        print("\t python3 basic_lfsr.py initialstate taps steps")
        print("\t example: ")
        print("\t python3 basic_lfsr.py 0000101 3,4 3")
        sys.exit()
    init_state = sys.argv[1]
    taps = [int(i) for i in sys.argv[2].split(",")]
    k = int(sys.argv[3])
    final_state = lfsr(init_state, taps, k)
    print(RED + "[*]" + ENDCOLOR + " inital state: ", GREEN, init_state, ENDCOLOR)
    print(RED + "[*]" + ENDCOLOR + " taps: ",GREEN, taps, ENDCOLOR)
    print(RED + "[*]" + ENDCOLOR + " final state: ",GREEN,  final_state, ENDCOLOR)
