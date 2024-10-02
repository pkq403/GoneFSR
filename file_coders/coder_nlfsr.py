import sys
from lib_coder_nlfsr import code_to_nlfsr_format

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    code_to_nlfsr_format(input_file, output_file)

