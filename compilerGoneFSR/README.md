# Version del compilador Gone (Statically Compiled Language) escrita por Pedro Castro

Escribi este compilador basandome en la guia del repositorio de Git escrita por David Beazley.

## Introduccion
Primero hice los ejercicios que se recomendaban hacer antes del programa se encuentran en la directorio /exercises. Una vez complete todos los ejercicios empece con el projecto del compilador. Las cinco primeras partes es decir hasta que haces el programa basico de generacion de bytecode llvm (fichero _llvmgen.py_) son bastante guiadas. Despues toda la implementacion de booleanos, operaciones logicas binarias, flujos condicionales (if, ifelse, while), ... no tiene ningun tipo de guía.

## Como funciona

Este compilador consta de los siguientes ficheros

    Lexer (generacion de tokens)
    * tokenizer.py

    Generacion de arbol AST (Abstract Syntax Tree)
    * parser.py
    * ast.py

    Comprobacion de errores
    * checker.py
    * typesys.py

    Generacion de codigo intermedio
    * ircode.py

    Generacion de codigo llvm
    * llvmgen.py

El flujo del programa seria algo asi:
 

 ![compiler schema](./compiler\-schema.png)

 #### 1. Tokenizer
 El tokenizer genera los tokens en base al contenido del archivo con los que despues el parser generara la estructura AST.

 #### 2. Parser
 Genera la estructura AST a traves de una gramatica y una precedencia definida

 #### 3. Checker
 Comprueba que no haya fallos semanticos en el codigo, como asignar un tipo char a una variable con un valor int.

 #### 4. IRCODE Generator
 Genera un codigo intermedio en la forma de SSA (Single Static Assignment), utilizando registros y mnemonicos.

 #### 5. LLVM Generator
 Genera codigo intermedio LLVM (low level virtual machine)

 #### 6. CLANG
 CLANG pasa el codigo intermedio LLVM a codigo maquina.



## Sintaxis
Toda instruccion en Gone debe acabar en ';', como debe ser.
### Tipos de datos
* int : entero clasico de 4 bytes (32bits)
* float : flotante que luego realmente se mapea a un double (64bits) en el codigo llvm
* bool : true/false
* char : un caracter (ejemplo 'a') (tambien estan incluidos caracteres como '\\' '\n' '\\'' '\\xhh' (siendo h cualquier valor hexadecimal, por lo que se puede representar cualquier caracter))
### Constantes
```
const ID = value;
```

El tipo se infiere del valor.

### Variables
```
var ID datatype = value;
```

El tipo se especifica explicitamente.

### Operaciones Binarias

#### Aritmeticas
* int + int = int
* int - int = int
* int * int = int
* int / int = int
* float + float = float
* float - float = float
* float * float = float
* float / float = float
En mi version de Gone los tipos no se convierten automaticamente, asi que el checker detectara un error si intentas hacer una operacion con 2 tipos distintos

#### Booleanas 
Toda operacion booleana se puede usar como condicion para bifurcar el codigo a traves de los statements if, ifelse y while.

las operaciones booleanas son:
* int < int = bool | int <= int = bool
* int > int = bool | int >= int = bool
* int == int = bool | int != int = bool
* float < float = bool | float <= float = bool
* float > float = bool | float >= float = bool
* float == float = bool | float != float = bool

#### Logicas
* bool && bool = bool
* bool || bool = bool
* bool == bool = bool
* bool != bool = bool


## Operaciones Unarias
Estas operaciones solo afectan a un valor, son especialmente importante a la hora de definir la precedencia del parser, esto afeca en como se hacen las operaciones de shift/reduce pero eso es otro tema. 

Las operaciones unarias permitidas son
* - int = int | - float = float
* + int = int | + float = float
* ! bool = bool

Todo lo que se 

### If, Ifelse y while
Sintaxis de la sentencia if
```
if (condicion) {
    instrucciones
}
```

Sintaxis de la sentencia ifelse
```
if (condicion) {
    instrucciones
}
else {
    instrucciones
}
```

Sintaxis de la sentencia while
```
while (condicion) {
    instrucciones
}
```

todas estas sentencias a nivel interno lo que hacen es generar bloques en el codigo intermedio para que el codigo pueda hacer saltos, todo esto en mas profundidad se puede ver en el archivo _ircode.py_.

### Funciones

Las funciones siempre tienen que retornar un tipo y todos los flujos de la funcion deben de retornar al final de su secuencia o si no el checker detectara un error (escribi un sistema en el _checker.py_ para detectar que todos los flujos del programa retornan).

El codigo que se escribe fuera de las funciones se considera global y a nivel practico lo que hago es crear otra funcion con todo ese codigo externo y reunirlo en otra funcion llamada **premain**, que se llama nada mas comienza la funcion **main** a ejecutar.

Sintaxis de las funcion en Gone
```
func NOMBRE_FUNCION(*ARGUMENTOS) RETURN_DATATYPE {

}
```

## Como usar Gone
Para usar Gone solo tienes que escribir un fichero nombreFichero.g con tu programa. Y despues ejecutar esta instruccion dentro de este proyecto
```
python3 -m gone.compile tu_fichero.g
```

Esto generara un binario en tu directorio llamado a.out (puedes cambiar el nombre de este fichero, modificando _compile.py_ o guardando el codigo intermedio llvm y compilandolo con CLANG a mano). 

Para ejecutar tu programa tan solo tendras que hacer
```
./a.out
```

## Testing
El compilador lo he intentado probar de muchas maneras y con muchos programas ademas de los que ya venian en el propio proyecto. Los programas mas complejos que venian en el programa para hacer testing son los que estan guardados en el directorio /programs.

Tambien estan los tests unitarios en la carpeta /Tests que ayudan a ver el comportamiento del compilador en cada etapa.

## Mas informacion sobre el proyecto
En el directorio cheking_experiments tengo algunos experimentos que he ido haciendo para comprobar comportamientos.

En el directorio automation_scripts tengo scripts que lanzan automaticamente algunos tests y devuelven los resultados en el directorio solutions.

## Conclusion 
Ha sido muy divertido hacer el compilador, se que tiene muchas cosas que mejorar.