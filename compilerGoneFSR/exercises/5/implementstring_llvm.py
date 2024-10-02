
from llvmlite.ir import Module, Function, FunctionType, IntType, IRBuilder, Constant, DoubleType, GlobalVariable, VoidType, ArrayType, PointerType
import llvmlite.binding as llvm


mod = Module('main')
hello_func = Function(mod, FunctionType(IntType(32), []), name='main')
block = hello_func.append_basic_block('entry')
builder = IRBuilder(block)
msg = bytearray("jajaja".encode("utf-8")) 
llvm_string = Constant(ArrayType(IntType(8), len(msg)), msg)
string_var = GlobalVariable(mod, llvm_string.type, name="cadena")
string_var.initializer = llvm_string
#builder.ret(Constant(IntType(32), 37))

# Implementing a function with a string as args
func_type =FunctionType(VoidType(), [PointerType(IntType(8))])
print_cad = Function(mod, func_type, name="printcad")
arg_cad = print_cad.args

builder.ret(Constant(IntType(32), 37))
# Implementing a function with a string as args
print(mod)
