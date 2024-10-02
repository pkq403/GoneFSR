'''
Takes a file and compress it with
non linear fsr tecnique
'''
from utils.non_linear_compl import non_linear_complexity
from fsr_decoder import FsrDecoder
from bitstring import BitArray, Bits

'''
TODO Fututo(Cuando ya este hecho para 2 bytes): adaptar el segmento len de cada minterm al numero de bis minimo para representar la m como maximo, 
por ejemplo para 350 necesitaras 9 bits, asi que eso sera lo que ocupe el segmento len
'''
# Por ahora solo se pueden comprimir data que en binario ocupe menos de 8kibibyes = 8192 bits
# Ademas m, tiene que ser menor tambien de 8192
def code_to_nlfsr_format(path_inputfile, path_outputfile):
    #print(f"[!] Coding - {path_inputfile}")
    with open(path_inputfile, 'rb') as file:
        data = BitArray(file.read())
    #print("[!] Calculating FSR ...")
    nlc = non_linear_complexity(data, len(data))
    seqlen_16_bin = bin(len(data))[2:][:16].zfill(16)
    m_16_bin = bin(nlc.m)[2:][:16].zfill(16)
    compressed = BitArray(bin=seqlen_16_bin)
    compressed += BitArray(bin=m_16_bin)
    compressed += data[:nlc.m]
    minterms = nlc.get_binary_terms_poly()
    for m in minterms:
        le_m = bin(len(m))[2:][:16].zfill(16)
        compressed += BitArray(bin=le_m)
        compressed += BitArray(bin=m)
    with open(path_outputfile, 'wb') as file:
        compressed.tofile(file)
    #print(f"[!] Coding Complete - {path_outputfile}")
    return nlc

def decode_nlfsr_format(path_inputfile, path_outputfile):
    with open(path_inputfile, 'rb') as file:
        compressed_data = BitArray(file.read())
    
    #print("[*] Parsing Compressed File ...")
    compressed_data = compressed_data.bin
    seq_len = int(compressed_data[:16], 2)
    nlc_m = int(compressed_data[16:32], 2)
    seq_init = compressed_data[32:32+nlc_m]
    
    start_window = 32 + nlc_m
    offset = 16
    minterms = []
    while start_window < len(compressed_data):
        len_minterm = int(compressed_data[start_window:start_window + offset], 2)
        start_window += 16
        minterms.append([ bool(int(bi)) for bi in compressed_data[start_window:start_window+len_minterm]])
        start_window += len_minterm
    if not minterms[-1]: # si la ultima lista es vacia
        minterms.pop()
    # Decoding process
    #print("[*] Recovering File ...")
    fsr_decoder = FsrDecoder(bool(int(seq_init[0])), minterms, nlc_m)
    decoded_fsr_seq = fsr_decoder.decode_fsr(seq_init, seq_len)
    decoded_seq_bitseq = BitArray(bin=decoded_fsr_seq)
    with open(path_outputfile, 'wb') as file:
        decoded_seq_bitseq.tofile(file)
