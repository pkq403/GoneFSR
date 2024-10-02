from llvmlite.ir import Module, Function, FunctionType, IntType, IRBuilder, Constant, DoubleType, GlobalVariable, VoidType
import llvmlite.binding as llvm

# First part: Introduction
mod = Module('hello')
hello_func = Function(mod, FunctionType(IntType(32), []), name='hello')
block = hello_func.append_basic_block('entry')
builder = IRBuilder(block)
builder.ret(Constant(IntType(32), 37))

# Second Part: Function with arguments
ty_double = DoubleType()
dsquared_func = Function(mod, FunctionType(ty_double, [ty_double, ty_double]), name='dsquared')
block = dsquared_func.append_basic_block('entry')
builder = IRBuilder(block)

# Get function args
x, y = dsquared_func.args

xsquared = builder.fmul(x, x)
ysquared = builder.fmul(y, y)

d2 = builder.fadd(xsquared, ysquared)
builder.ret(d2)

# Third Part: Calling an external function (like sqrt())
sqrt_func = Function(mod, FunctionType(ty_double, [ty_double]), name="sqrt")
distance_func = Function(mod, FunctionType(ty_double, [ty_double, ty_double]), name='distance')
block = distance_func.append_basic_block('entry')
builder = IRBuilder(block)
x, y = distance_func.args
d2 = builder.call(dsquared_func, [x, y])
d = builder.call(sqrt_func, [d2])
builder.ret(d)


# Fourth Part: Variables and State
x_var = GlobalVariable(mod, ty_double, 'x')
x_var.initializer = Constant(ty_double, 0.0)

incr_func = Function(mod, FunctionType(VoidType(), []), name='incr')
block = incr_func.append_basic_block('entry')
builder = IRBuilder(block)
tmp1 = builder.load(x_var) # Carga la constante
tmp2 = builder.fadd(tmp1, Constant(ty_double, 1.0))
builder.store(tmp2, x_var) # Guarda el resultado en la constante
builder.ret_void()

#print(mod) # This print generates the llvm(low level virtual machine) instructions (bytecode instructions)
           # with that instructions we can compile an executable binary using clang (bytecode compiler)


# Fifth Part: Compile directly in python (JIT (Just In Time) tool, ctypes)
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

target = llvm.Target.from_default_triple()
target_machine = target.create_target_machine()
compiled_mod = llvm.parse_assembly(str(mod))
engine = llvm.create_mcjit_compiler(compiled_mod, target_machine)

# Look up the function pointer (a Python int)
func_ptr = engine.get_function_address("distance")

# Turn into a Python callable using ctypes
from ctypes import CFUNCTYPE, c_int, c_double
distance = CFUNCTYPE(c_double, c_double, c_double)(func_ptr)

res = distance(3, 4)
print('distance(3,4) = ', res)
