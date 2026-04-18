# MiniLang – Analizador Léxico y Sintáctico

## Descripción

Este proyecto implementa tanto el **analizador léxico** como el **analizador sintáctico** para un lenguaje de programación estructurado denominado *MiniLang*. El objetivo de esta fase es reconocer tokens a partir de un archivo fuente con extensión `.mlng`, validar la estructura del programa según la gramática del lenguaje y reportar errores léxicos y sintácticos sin detener la ejecución.

### Analizador Léxico

El analizador léxico es responsable de:
- Reconocer **tokens válidos** del lenguaje.
- Llevar control de **línea y columna**.
- Manejar **indentación significativa** mediante tokens `INDENT` y `DEDENT`.
- Generar un archivo de salida `.out` con el listado completo de tokens.
- Reportar **errores léxicos** en pantalla sin detener el análisis.

### Analizador Sintáctico

El analizador sintáctico ascendente:
- Utiliza los **tokens generados por el analizador léxico**.
- Valida la **estructura sintáctica** del código según la gramática definida para MiniLang.
- Aplica **precedencias y asociatividad** en las expresiones.
- Reporta **errores sintácticos** y continúa analizando el archivo hasta el final, sin abortar.

## Cómo ejecutar

El ejecutable del programa se llama `minilang`.

1. **Compilar y ejecutar el programa:**

   ```bash
   ./minilang
Ingreso de archivo: Ingresar la ruta del archivo .mlng cuando el programa lo solicite.
Salida

Se genera automáticamente un archivo con el mismo nombre que el archivo de entrada, pero con la extensión .out.

Ejemplo:

programa.mlng → programa.out

Formato del archivo .out

El archivo .out contiene un listado de tokens con el formato:

(línea, columna_inicio-columna_fin) TIPO_TOKEN valor=lexema

Ejemplo de salida:

(1, 1-3) KW_INT valor=int
(1, 5-5) ID valor=x
(1, 7-7) EQ valor==
(1, 9-9) ENTERO valor=2
En pantalla

Se mostrará en pantalla:

El listado de errores léxicos si existen.
El mensaje de éxito si no hay errores.
Tokens Reconocidos
Identificadores
Máximo 31 caracteres.
Formato: Letra o _ seguido de letras, números o _.
Números
Enteros: Números sin ceros a la izquierda (excepto 0).
Flotantes: Formato dígitos.dígitos.
Cadenas
Delimitadas por comillas dobles: "texto".
No pueden quedar sin cerrar.
Palabras clave
Tipos: int, float, string, bool.
Estructuras de control: if, else, while, func.
Entrada/Salida: Read, Write.
Literales: true, false.
Control de flujo: return.
Manejo de Indentación

El analizador maneja una pila de niveles de indentación para:

Emitir INDENT cuando el nivel de indentación aumenta.
Emitir DEDENT cuando el nivel de indentación disminuye.

Si el nivel de indentación no coincide con la pila, se reporta un error de indentación. Esto permite implementar indentación significativa similar a Python.

Manejo de Errores Léxicos

El analizador léxico detecta y reporta los siguientes errores:

Identificadores mayores a 31 caracteres.
Enteros con ceros a la izquierda.
Cadenas sin cerrar.
Caracteres inválidos.
Niveles de indentación incorrectos.

El análisis continúa hasta el final del archivo, incluso si se encuentran errores léxicos.

Manejo de Errores Sintácticos

El analizador sintáctico:

Detecta errores de sintaxis en la estructura del código.
Recupera de errores para seguir analizando el archivo hasta EOF.

Los errores sintácticos se reportan en pantalla indicando:

Línea y columna.
Símbolo que provocó el error.
Descripción del error.
Limitaciones
No valida la semántica del código (solo la sintaxis).
No evalúa expresiones.
No ejecuta código.
Solo realiza reconocimiento léxico y sintáctico.