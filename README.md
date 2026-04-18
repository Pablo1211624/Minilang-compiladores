# MiniLang – Analizador Léxico y Sintáctico

## Descripción

Este proyecto implementa tanto el **analizador léxico** como el **analizador sintáctico** para un lenguaje de programación estructurado denominado *MiniLang*. El objetivo de esta fase es reconocer tokens a partir de un archivo fuente con extensión `.mlng`, validar la estructura del programa según la gramática del lenguaje y reportar errores léxicos y sintácticos sin detener la ejecución.

### Analizador Léxico

El analizador léxico es responsable de:
- Reconocer tokens válidos del lenguaje.
- Llevar control de línea y columna.
- Manejar indentación significativa mediante tokens `INDENT` y `DEDENT`.
- Generar un archivo de salida `.out` con el listado completo de tokens.
- Reportar errores léxicos en pantalla sin detener el análisis.

### Analizador Sintáctico

El analizador sintáctico ascendente:
- Utiliza los tokens generados por el analizador léxico.
- Valida la estructura sintáctica del código según la gramática definida para *MiniLang*.
- Aplica precedencias y asociatividad en las expresiones.
- Reporta errores sintácticos y continúa analizando el archivo hasta el final, sin abortar.

## Cómo ejecutar

El ejecutable del programa se llama `minilang`.

1. **Compilar y ejecutar el programa:**

   ```bash
   ./minilang