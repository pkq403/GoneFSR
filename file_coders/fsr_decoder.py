from utils.binary_op import XOR

class FsrDecoder:
    def __init__(self, independent, minterms, m):
        self.independent = independent
        self.minterms = minterms
        self.m = m
    
    def decode_fsr(self, initial_state, final_len):
        i = self.m
        seq = initial_state
        while i < final_len:
            seq += self.evaluate(seq[-self.m:])
            i += 1
        return seq

    def evaluate(self, values): # usar esta funcion para descomprimir a partir de los minterms/coefs
        result = self.independent
        for minterm in self.minterms:
            result = XOR(result, all([XOR(int(values[-i-1]),v) for i,v in enumerate(minterm)]))
        return '1' if result else '0'
