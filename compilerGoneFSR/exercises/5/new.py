
from llvmlite import ir

# Crear un módulo LLVM
mod = ir.Module(name="main")

# Definir una función que toma un `i8*` como parámetro (la cadena) y retorna void
func_type = ir.FunctionType(ir.VoidType(), [ir.PointerType(ir.IntType(8))])
imprimir_func = ir.Function(mod, func_type, name="imprimir_cadena")

# Definir la función main que retorna un entero de 32 bits
hello_func = ir.Function(mod, ir.FunctionType(ir.IntType(32), []), name="main")

# Crear un bloque de entrada a la función main
block = hello_func.append_basic_block(name="entry")
builder = ir.IRBuilder(block)

# Crear la cadena como un array de bytes
msg = bytearray("jajaja".encode("utf-8"))  # Cadena "jajaja" como bytes
llvm_string = ir.Constant(ir.ArrayType(ir.IntType(8), len(msg)), msg)

# Declarar la cadena como una variable global
string_var = ir.GlobalVariable(mod, llvm_string.type, name="cadena")
string_var.initializer = llvm_string
string_var.linkage = 'internal'  # Para que sea privada al módulo
string_var.global_constant = True  # Declararla como constante

# GUIA RAPIDA:
# 1. declaras la funcion como array de bytes
# 2. Antes de pasar la cadena a una funcion lo pasas a un puntero i8*
# 3. Pasas el puntero a la funcion

# Obtener un puntero a la cadena
string_ptr = builder.bitcast(string_var, ir.PointerType(ir.IntType(8)))

# Llamar a la función `imprimir_cadena` pasando `string_ptr` como argumento
builder.call(imprimir_func, [string_ptr])

# Retornar 0 (éxito) para la función main
builder.ret(ir.Constant(ir.IntType(32), 0))

# Imprimir el código LLVM
print(mod)
