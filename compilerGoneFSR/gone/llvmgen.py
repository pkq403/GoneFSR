'''
LLVM generation
Author: Pedro Castro
'''
from llvmlite.ir import (
    Module, IRBuilder, Function, IntType, DoubleType, VoidType, PointerType, ArrayType, Constant, GlobalVariable,
    FunctionType
    )


int_type    = IntType(32)         # 32-bit integer
float_type  = DoubleType()        # 64-bit float
byte_type   = IntType(8)          # 8-bit integer
string_pointer_type = PointerType(IntType(8))
void_type   = VoidType()          # Void type.  This is a special type
                                  # used for internal functions returning
                                  # no value

class GenerateLLVM(object):
    def __init__(self):
        self.typemapper = {'int': int_type, 'float': float_type, 'char': byte_type, 
                           'bool': int_type, 'void': void_type}
        
        self.module = Module('module')

        self.builder = IRBuilder()

        self.functions = {}
        self.cur_function = 'undefined'

        self.vars = {}

        # Dictionary that holds all of the temporary registers created in
        # the intermediate code.
        self.temps = {}
        
        # Dictionary that holds all the blocks declaration
        self.blocks = {}

        # Initialize the runtime library functions (see below)
        self.declare_runtime_library()



    def declare_runtime_library(self):
        # built-in functions

        self.runtime = {}
        
        # Declare printing functions
        self.runtime['_print_int'] = Function(self.module,
                                              FunctionType(void_type, [int_type]),
                                              name="_print_int")

        self.runtime['_print_float'] = Function(self.module,
                                                FunctionType(void_type, [float_type]),
                                                name="_print_float")

        self.runtime['_print_byte'] = Function(self.module,
                                                FunctionType(void_type, [byte_type]),
                                                name="_print_byte")

        self.runtime['_print_string'] = Function(self.module,
                                                FunctionType(void_type, [string_pointer_type]),
                                                name="_print_string")

        self.runtime['_coder_nlfsr'] = Function(self.module,
                                                FunctionType(void_type, [string_pointer_type, string_pointer_type]),
                                                name="_coder_nlfsr")

        self.runtime['_decoder_nlfsr'] = Function(self.module,
                                                FunctionType(void_type, [string_pointer_type, string_pointer_type]),
                                                name="_decoder_nlfsr")

    def generate_function(self, function_name, params_types, return_type):
        params_types_llvm = [self.typemapper[p] for p in params_types]
        self.functions[function_name] = Function(self.module, FunctionType(self.typemapper[return_type],
                                                                           params_types_llvm), name=function_name)
        self.blocks[function_name] = {}
        self.blocks[function_name]['entry'] = self.functions[function_name].append_basic_block('entry')
            

    def generate_code(self, ircode, fn_name, params_labels, params_types):
        self.temps.clear()
        for instr in ircode:
            if instr[0] == 'LABEL':
                self.blocks[fn_name][instr[1]] = self.functions[fn_name].append_basic_block(instr[1])
        self.builder.position_at_end(self.blocks[fn_name]['entry'])
        if fn_name == 'main': self.builder.call(self.functions['premain'], [])
        
        for label, arg_type, arg in zip(params_labels, params_types,  self.functions[fn_name].args):
            self.temps[label] = self.builder.alloca(self.typemapper[arg_type], name=label)
            self.builder.store(arg, self.temps[label])

        self.cur_function = fn_name

        for opcode, *args in ircode:
            # print("opcode", opcode, " args: ", *args)
            if hasattr(self, 'emit_'+opcode):
                
                getattr(self, 'emit_'+opcode)(*args)
            else:
                print('Warning: No emit_'+opcode+'() method')

        if fn_name=="premain":
            self.builder.ret_void()


    def emit_MOVI(self, value, target):
        self.temps[target] = Constant(int_type, value)

    def emit_MOVF(self, value, target):
        self.temps[target] = Constant(float_type, value)

    def emit_MOVB(self, value, target):
        self.temps[target] = Constant(byte_type, value)

    def emit_MOVS(self, value, target):
        string_encoded = bytearray(value.encode("utf-8")) + bytearray([0])
        self.temps[target] = GlobalVariable(self.module,ArrayType(IntType(8), len(string_encoded)),name=target)
        self.temps[target].initializer = Constant(ArrayType(IntType(8), len(string_encoded)), string_encoded) 

    def emit_VARI(self, name):
        var = GlobalVariable(self.module, int_type, name=name)
        var.initializer = Constant(int_type, 0)
        self.vars[name] = var

    def emit_VARF(self, name):
        var = GlobalVariable(self.module, float_type, name=name)
        var.initializer = Constant(float_type, 0.0)
        self.vars[name] = var

    def emit_VARB(self, name):
        var = GlobalVariable(self.module, byte_type, name=name)
        var.initializer = Constant(byte_type, 0)
        self.vars[name] = var

    def emit_VARS(self, name):
        var = GlobalVariable(self.module, byte_type.as_pointer(), name=name)
        var.initializer = Constant(byte_type.as_pointer(), None)
        self.vars[name] = var

    def emit_ALLOCI(self, name):
        local_int_var = self.builder.alloca(int_type, name=name)
        self.builder.store(Constant(int_type, 0), local_int_var)
        self.temps[name] = local_int_var

    def emit_ALLOCF(self, name):
        local_float_var = self.builder.alloca(float_type, name=name)
        self.builder.store(Constant(float_type, 0.0), local_float_var)
        self.temps[name] = local_float_var

    def emit_ALLOCB(self, name):
        local_byte_var = self.builder.alloca(byte_type, name=name)
        self.builder.store(Constant(byte_type, 0), local_byte_var)
        self.temps[name] = local_byte_var
    
    def emit_ALLOCS(self, name):
        local_byte_var = self.builder.alloca(byte_type.as_pointer(), name=name)
        self.builder.store(Constant(byte_type.as_pointer(), None), local_byte_var)
        self.temps[name] = local_byte_var
    


 
    def emit_LOADI(self, name, target):
        self.temps[target] = self.builder.load(self.vars[name], target)

    def emit_LOADF(self, name, target):
        self.temps[target] = self.builder.load(self.vars[name], target)

    def emit_LOADB(self, name, target):
        self.temps[target] = self.builder.load(self.vars[name], target)
    
    def emit_LOADS(self, name, target):
        self.temps[target] = self.builder.load(self.vars[name], target)
    
    def emit_LOADFASTI(self, name, target):
        self.temps[target] = self.builder.load(self.temps[name], target)

    def emit_LOADFASTF(self, name, target):
        self.temps[target] = self.builder.load(self.temps[name], target)

    def emit_LOADFASTB(self, name, target):
        self.temps[target] = self.builder.load(self.temps[name], target)
    
    def emit_LOADFASTS(self, name, target): # load s
        self.temps[target] = self.builder.load(self.temps[name], target)

    def emit_STOREI(self, source, target):
        self.builder.store(self.temps[source], self.vars[target])

    def emit_STOREF(self, source, target):
        self.builder.store(self.temps[source], self.vars[target])

    def emit_STOREB(self, source, target):
        self.builder.store(self.temps[source], self.vars[target])
    
    def emit_STORES(self, source, target):
        string_pointer = self.builder.bitcast(self.temps[source], string_pointer_type)
        self.builder.store(self.temps[source], self.vars[target])

    def emit_STOREFASTI(self, source, target):
        self.builder.store(self.temps[source], self.temps[target])

    def emit_STOREFASTF(self, source, target):
        self.builder.store(self.temps[source], self.temps[target])

    def emit_STOREFASTB(self, source, target):
        self.builder.store(self.temps[source], self.temps[target])
    
    def emit_STOREFASTS(self, source, target):
        string_pointer = self.builder.bitcast(self.temps[source], string_pointer_type)
        self.builder.store(string_pointer, self.temps[target])

    # Binary logical operators
    def emit_AND(self, left, right, target):
        self.temps[right] = self.builder.trunc(self.temps[right], IntType(1), right)
        self.temps[left] = self.builder.trunc(self.temps[left], IntType(1), left)
        self.temps[target] = self.builder.and_(self.temps[left], self.temps[right], target)
    
    def emit_OR(self, left, right, target):
        self.temps[right] = self.builder.trunc(self.temps[right], IntType(1), right)
        self.temps[left] = self.builder.trunc(self.temps[left], IntType(1), left)
        self.temps[target] = self.builder.or_(self.temps[left], self.temps[right], target)

    def emit_XOR(self, left, right, target):
        self.temps[right] = self.builder.zext(self.temps[right], IntType(32), right)
        self.temps[target] = self.builder.xor(self.temps[left], self.temps[right], target)
        
    # Binary cmp operator
    def emit_CMPI(self, op, left, right, target):
        self.temps[target] = self.builder.icmp_signed(op, self.temps[left], self.temps[right], target)
    
    def emit_CMPF(self, op, left, right, target):
        self.temps[target] = self.builder.fcmp_ordered(op, self.temps[left], self.temps[right], target)

    def emit_CMPB(self, op, left, right, target):
        self.temps[target] = self.builder.icmp_signed(op, self.temps[left], self.temps[right], target)

    # Binary + operator
    def emit_ADDI(self, left, right, target):
        self.temps[target] = self.builder.add(self.temps[left], self.temps[right], target)

    def emit_ADDF(self, left, right, target):
        self.temps[target] = self.builder.fadd(self.temps[left], self.temps[right], target)

    # Binary - operator
    def emit_SUBI(self, left, right, target):
        self.temps[target] = self.builder.sub(self.temps[left], self.temps[right], target)

    def emit_SUBF(self, left, right, target):
        self.temps[target] = self.builder.fsub(self.temps[left], self.temps[right], target)

    # Binary * operator
    def emit_MULI(self, left, right, target):
        self.temps[target] = self.builder.mul(self.temps[left], self.temps[right], target)
        

    def emit_MULF(self, left, right, target):
        self.temps[target] = self.builder.fmul(self.temps[left], self.temps[right], target)

    # Binary / operator
    def emit_DIVI(self, left, right, target):
        self.temps[target] = self.builder.sdiv(self.temps[left], self.temps[right], target)

    def emit_DIVF(self, left, right, target):
        self.temps[target] = self.builder.fdiv(self.temps[left], self.temps[right], target)

    # Print statements
    def emit_PRINTI(self, source):
        self.temps[source] = self.builder.zext(self.temps[source], IntType(32), source)
        self.builder.call(self.runtime['_print_int'], [self.temps[source]])

    def emit_PRINTF(self, source):
        self.builder.call(self.runtime['_print_float'], [self.temps[source]])

    def emit_PRINTB(self, source):
        self.builder.call(self.runtime['_print_byte'], [self.temps[source]])

    def emit_PRINTS(self, source):
        # we need to transform it to a i8 pointer (i8*) before passing to function
        string_pointer = self.builder.bitcast(self.temps[source], string_pointer_type)
        self.builder.call(self.runtime['_print_string'], [string_pointer])
    
    # CODING STATEMENTS
    def emit_CODER(self, inputp, outputp):
        string_pointer_input = self.builder.bitcast(self.temps[inputp], string_pointer_type)
        string_pointer_output = self.builder.bitcast(self.temps[outputp], string_pointer_type)
        self.builder.call(self.runtime['_coder_nlfsr'], [string_pointer_input, string_pointer_output])
    
    def emit_DECODER(self, inputp, outputp):
        string_poiner_input = self.builder.bitcast(self.temps[inputp], string_pointer_type)
        string_poiner_output = self.builder.bitcast(self.temps[outputp], string_pointer_type)
        self.builder.call(self.runtime['_decoder_nlfsr'], [string_pointer_input, string_pointer_output])

    # Branch (If/Ifelse/While)
    def emit_BRANCH(self, block_name):
        self.builder.branch(self.blocks[self.cur_function][block_name])
    
    def emit_CBRANCH(self, test, true_branch, false_branch):
        self.temps[test] = self.builder.trunc(self.temps[test], IntType(1), test)
        self.builder.cbranch(self.temps[test], self.blocks[self.cur_function][true_branch], self.blocks[self.cur_function][false_branch])

    def emit_LABEL(self, block_name):
        self.builder.position_at_end(self.blocks[self.cur_function][block_name])
    
    # Functions
    def emit_CALL(self, *args):
        # print("llega al call -> ", args[0])
        fn_args = []
        for a in args[1:-1]:
            fn_args.append(self.temps[a])
        self.temps[args[-1]] = self.builder.call(self.functions[args[0]], fn_args)
    
    def emit_RET(self, source):
        self.builder.ret(self.temps[source])


def compile_llvm(source):
    from .ircode import compile_ircode

    # Compile intermediate code 
    fn_structs = compile_ircode(source)
    # Make the low-level code generator
    generator = GenerateLLVM()
    for function in fn_structs: # First, generates all the functions
        f = fn_structs[function]
        generator.generate_function(f['function_name'], f['params_types'], f['return_type'])
    for function in fn_structs: # Second, generates the code for each function
        f = fn_structs[function]
        generator.generate_code(f['code'], f['function_name'], f['params_labels'], f['params_types'])
    
    # Generate low-level code
    return str(generator.module)

def main():
    import sys

    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python3 -m gone.llvmgen filename\n")
        raise SystemExit(1)

    source = open(sys.argv[1]).read()
    llvm_code = compile_llvm(source)
    print(llvm_code)

if __name__ == '__main__':
    main()
