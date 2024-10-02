
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

# Declarar la cadena directamente como un puntero a i8
mensaje = "jajaja\00"  # Incluye el terminador nulo
mensaje_global = ir.GlobalVariable(mod, ir.IntType(8).as_pointer(), name="cadena")
mensaje_global.linkage = 'internal'
mensaje_global.global_constant = True
mensaje_global.initializer = ir.Constant(ir.ArrayType(ir.IntType(8), len(mensaje)),
                                         bytearray(mensaje.encode("utf-8")))

# Llamar a la función `imprimir_cadena` pasando el puntero directamente
builder.call(imprimir_func, [mensaje_global])

# Retornar 0 (éxito) para la función main
builder.ret(ir.Constant(ir.IntType(32), 0))

# Imprimir el código LLVM
print(mod)
