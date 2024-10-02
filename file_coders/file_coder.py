from coder_nlfsr import code_to_nlfsr_format
from coder_string_nlfsr_file import code_to_string_format
import sys
import os
if __name__=="__main__":
    already_calculated_nlc = code_to_nlfsr_format(sys.argv[1], sys.argv[2])

    code_to_string_format(sys.argv[1], sys.argv[2].replace("bin", "str"), nlc = already_calculated_nlc)
