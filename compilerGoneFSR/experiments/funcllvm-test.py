from llvmlite.ir import Module, Function, FunctionType, IntType, IRBuilder, Constant, DoubleType, GlobalVariable, VoidType
import llvmlite.binding as llvm

mod = Module('module')
# Function
add_func = Function(mod, FunctionType(IntType(32), [IntType(32), IntType(32)]), name="add")
add_func_block = add_func.append_basic_block('entry')
add_func_builder = IRBuilder(add_func_block)

x, y = add_func.args
print("add func args -> ", x, y)
print("x type -> ", type(x))
var_local_x_add_func = add_func_builder.alloca(IntType(32), name="x")
add_func_builder.store(x,var_local_x_add_func )
add_func_builder.add(x, y)


# main
main = Function(mod, FunctionType(IntType(32), []), name="main")
block = main.append_basic_block('entry')
block2 = main.append_basic_block('xdd')
builder = IRBuilder(block)
var_local_x = builder.alloca(IntType(32), name="x")
print("var_local_x -> ", var_local_x)
builder.store(Constant(IntType(32), 0), var_local_x)
var_local_x_load = builder.load(var_local_x)
builder.ret(Constant(IntType(32), 1))
print(mod)