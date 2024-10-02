
from llvmlite import ir

# Crear un módulo LLVM
module = ir.Module(name="mi_modulo")

# Definir una cadena constante
mensaje = "Hola, LLVM!"
mensaje_bytes = bytearray(mensaje.encode("utf-8")) + bytearray([0])  # Incluye el carácter nulo al final
mensaje_const = ir.Constant(ir.ArrayType(ir.IntType(8), len(mensaje_bytes)), mensaje_bytes)

# Declara una variable global para almacenar la cadena
mensaje_global = ir.GlobalVariable(module, mensaje_const.type, name="mensaje")
mensaje_global.linkage = "internal"
mensaje_global.global_constant = True
mensaje_global.initializer = mensaje_const

# Generar el código LLVM
print(module)
