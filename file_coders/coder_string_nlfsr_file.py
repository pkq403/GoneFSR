from non_linear_compl import non_linear_complexity
from bitstring import BitArray, Bits
def code_to_string_format(input_file, output_file, nlc=False):
    with open(input_file, 'rb') as file:
        data = BitArray(file.read())
    if not nlc:
        nlc = non_linear_complexity(data, len(data))
    print("Calculating nlfsr ...")
    seqlen_16_bin = bin(len(data))[2:][:16].zfill(16)
    m_16_bin = bin(nlc.m)[2:][:16].zfill(16)
    data_to_write = seqlen_16_bin + m_16_bin + str(data[:nlc.m].bin) + nlc.__str__()
    with open(output_file, 'w+') as file:
        file.write(data_to_write)
    print(f"[*] {input_file} converted to string format")
