# MiniLang – Analizador Léxico

## Descripción

Este proyecto implementa el analizador léxico para un lenguaje de programación estructurado denominado *MiniLang*.

El objetivo de esta fase es reconocer y emitir tokens a partir de un archivo fuente con extensión `.mlng`, reportando errores léxicos sin detener la ejecución.

El analizador:
- Reconoce tokens válidos del lenguaje.
- Lleva control de línea y columna.
- Maneja indentación significativa mediante tokens `INDENT` y `DEDENT`.
- Genera un archivo de salida `.out` con el listado completo de tokens.
- Reporta errores léxicos en pantalla.


## Cómo ejecutar

El ejecutable del analizador léxico se llama: minilang

./minilang

Ingresar la ruta del archivo .mlng cuando el programa lo solicite.

## Salida
Se genera automáticamente un archivo con el mismo nombre del archivo de entrada pero con extensión .out.
programa.mlng → programa.out

El archivo .out contiene: (línea, columna_inicio-columna_fin) TIPO_TOKEN  valor=lexema

(1, 1-3) KW_INT  valor=int
(1, 5-5) ID  valor=x
(1, 7-7) EQ  valor==
(1, 9-9) ENTERO  valor=2

En pantalla se muestran:

Listado de errores léxicos si existen

O mensaje de éxito si no hay errores

Tokens Reconocidos
Identificadores

Máximo 31 caracteres

Formato: letra o _ seguido de letras, números o _

Números

Enteros sin ceros a la izquierda (excepto 0)

Flotantes con formato dígitos.dígitos

Cadenas

Delimitadas por comillas dobles "texto"

No pueden quedar sin cerrar

Palabras clave
int, float, string, bool
if, else, while, func
Read, Write
true, false
return

## Manejo de Indentación

El analizador mantiene una pila de niveles de indentación.

Cuando el nivel aumenta → se emite INDENT

Cuando disminuye → se emite DEDENT

Si el nivel no coincide con la pila → error de indentación

Esto permite implementar indentación significativa similar a Python.


## Manejo de Errores Léxicos

El analizador detecta:

Identificadores mayores a 31 caracteres

Enteros con ceros a la izquierda

Cadenas sin cerrar

Caracteres inválidos

Niveles de indentación incorrectos

El análisis continúa hasta EOF aunque existan errores.


## Limitaciones

No valida estructura sintáctica.

No evalúa expresiones.

No ejecuta código.

Solo realiza reconocimiento léxico.

