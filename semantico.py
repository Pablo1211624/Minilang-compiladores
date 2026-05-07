class TablaSimbolos:

    def __init__(self):
        #trabajamos la tabla como diccionario
        self.tabla = {}

    #metodo en el cual declaramos una variable por primera vez
    def declarar(self, nombre, tipo, valor=None, constante=False):

        self.tabla[nombre] = {

            "tipo": tipo,
            "valor": valor,
            "constante": constante
        }

    #metodo para verificar si una variable ya existe en la tabla de simbolos
    def existe(self, nombre):

        return nombre in self.tabla

    #retorna la variable de la tabla de simbolos por su nombre
    def obtener(self, nombre):

        return self.tabla[nombre]

    #actualiza el valor de una variable ya declarada
    def insertar(self, nombre, valor):

        self.tabla[nombre]["valor"] = valor


    def imprimir(self):

        print("\nTABLA DE SIMBOLOS")

        for nombre, datos in self.tabla.items():

            print(f"Nombre     : {nombre}\nTipo       : {datos['tipo']}\nValor      : {datos['valor']}\nConstante  : {datos['constante']}")

class AnalizadorSemantico:
    def __init__(self):
        # Inicializamos la tabla de símbolos
        self.tabla_simbolos = TablaSimbolos()

    def analizar(self, sintaxis):
        # Aquí recorreríamos la sintaxis generado por el parser
        # y realizaríamos las verificaciones semánticas necesarias.

        if sintaxis is None:
                print("Error: No se pudo generar el árbol de sintaxis.")
                return
            
        for produccion in sintaxis[1]: 
            #la primera produccion del parser es programa asi que debemos iniciar desde la segunda y continuar con el resto de producciones
            self.analizar_produccion(produccion)

    def analizar_produccion(self, produccion):
        tipo_produccion = produccion[0]
            
        #cuando se declara la variable pero no se inicializa
        if tipo_produccion == 'decl':
            tipo = produccion[1] #tipo de dato
            nombre = produccion[2] #nombre de la variable
            if self.tabla_simbolos.existe(nombre):
                print(f"Error: Variable '{nombre}' ya declarada.")
                return
            self.tabla_simbolos.declarar(nombre, tipo) #declaramos la variable en la tabla de simbolos


        #se declara y se asigna valor
        elif tipo_produccion == 'decl_assign':
            tipo = produccion[1]
            nombre = produccion[2] 
            valor = self.evaluar_expresion(produccion[3]) #valor asignado
            if self.tabla_simbolos.existe(nombre):
                print(f"Error: Variable '{nombre}' ya declarada.")
                return
            tipo_valor = self.tipo_expresion(produccion[3])
            if tipo != tipo_valor:
                print(f"Error: Tipo de valor '{tipo_valor}' no coincide con el tipo de variable '{tipo}'.")
                return
            self.tabla_simbolos.declarar(nombre, tipo, valor)

        #se declara una constante sin valor
        elif tipo_produccion == 'const_decl':
            tipo = produccion[1] 
            nombre = produccion[2]
            if self.tabla_simbolos.existe(nombre):
                print(f"Error: Variable '{nombre}' ya declarada.")
                return
            self.tabla_simbolos.declarar(nombre, tipo, constante=True) #declaramos la constante en la tabla de simbolos

        #se declara una constante con valor
        elif tipo_produccion == 'const_decl_assign':
            tipo = produccion[1] 
            nombre = produccion[2] 
            if self.tabla_simbolos.existe(nombre):
                print(f"Error: Variable '{nombre}' ya declarada.")
                return
            tipo_valor = self.tipo_expresion(produccion[3])
            if tipo != tipo_valor:
                print(f"Error: Tipo de valor '{tipo_valor}' no coincide con el tipo de variable '{tipo}'.")
                return
            valor = self.evaluar_expresion(produccion[3]) #valor asignado
            self.tabla_simbolos.declarar(nombre, tipo, valor, constante=True) #declaramos la constante en la tabla de simbolos con su valor

        #cuando solo se asigna un valor a una variable ya declarada
        elif tipo_produccion == 'assign':
            nombre = produccion[1]
            valor = self.evaluar_expresion(produccion[2])

            if not self.tabla_simbolos.existe(nombre):
                print(f"Error: Variable '{nombre}' no declarada.")
                return

            simbolo = self.tabla_simbolos.obtener(nombre)
            tipo_variable = simbolo["tipo"]
            tipo_valor = self.tipo_expresion(produccion[2])

            if tipo_variable != tipo_valor:
                print(f"Error: Tipo de valor '{tipo_valor}' no coincide con el tipo de variable '{tipo_variable}'.")
                return

            if simbolo["constante"]:
                print(f"Error: No se puede asignar a la constante '{nombre}'.")
                return

            self.tabla_simbolos.insertar(nombre, valor) #actualizamos el valor de la variable en la tabla de simbolos

        #evaluacion de if
        elif tipo_produccion == 'if':
            condicion = produccion[1]
            tipo_condicion = self.tipo_expresion(condicion)
            if tipo_condicion != 'bool':
                print(f"Error: La condición del if debe ser de tipo bool, no {tipo_condicion}.")
                return
            
            bloque_if = produccion[2]
            for instruccion in bloque_if:
                self.analizar_produccion(instruccion)
            bloque_else = produccion[3]
            if bloque_else is not None:
                for instruccion in bloque_else:
                    self.analizar_produccion(instruccion)

        elif tipo_produccion == 'while':
            condicion = produccion[1]
            tipo_condicion = self.tipo_expresion(condicion)
            if tipo_condicion != 'bool':
                print(f"Error: La condición del while debe ser de tipo bool, no {tipo_condicion}.")
                return
            
            bloque_while = produccion[2]
            for instruccion in bloque_while:
                self.analizar_produccion(instruccion)

        

    def evaluar_expresion(self, expresion):
        #se hara verificaciones de tipos y acciones semanticas relacionadas a las expresiones
        tipo_expresion = expresion[0]

        if tipo_expresion == 'val':
            return expresion[1] #retorna el valor literal de la expresión
        
        elif tipo_expresion == 'binop':
            operador = expresion[1]
            izquierda = self.evaluar_expresion(expresion[2])
            derecha = self.evaluar_expresion(expresion[3])

            typeizquierda = type(izquierda)
            typederecha = type(derecha)

            if typeizquierda != typederecha:
                print(f"Error: Tipos incompatibles en la expresión: {typeizquierda} y {typederecha}.")
                return None
            
            if typeizquierda == bool or typederecha == bool:
                print(f"Error: Operadores aritméticos no pueden operar con bool.")
                return None
            
            try:
                if operador == '+':
                    return izquierda + derecha
                elif operador == '-':
                    return izquierda - derecha
                elif operador == '*':
                    return izquierda * derecha
                elif operador == '/':
                    if derecha == 0:
                        print("Error: División por cero.")
                        return None
                    return izquierda / derecha
                elif operador == '%':
                    return izquierda % derecha
            except Exception as e:
                print(f"Error semantico: {e}")
                return None
        
        elif tipo_expresion == 'rel':
            operador = expresion[1]
            izquierda = self.evaluar_expresion(expresion[2])
            derecha = self.evaluar_expresion(expresion[3])

            typeizquierda = type(izquierda)
            typederecha = type(derecha)

            if typeizquierda != typederecha:
                print(f"Error: Tipos incompatibles en la expresión relacional: {typeizquierda} y {typederecha}.")
                return None
            try:
                if operador == '==':
                    return izquierda == derecha
                elif operador == '!=':
                    return izquierda != derecha
                elif operador == '<':
                    return izquierda < derecha
                elif operador == '>':
                    return izquierda > derecha
                elif operador == '<=':
                    return izquierda <= derecha
                elif operador == '>=':
                    return izquierda >= derecha
            except Exception as e:
                print(f"Error semantico: {e}")
                return None
            
        elif tipo_expresion == 'bool_op':
            operador = expresion[1]
            izquierda = self.evaluar_expresion(expresion[2])
            derecha = self.evaluar_expresion(expresion[3])
            if type(izquierda) != bool or type(derecha) != bool:
                print(f"Error: Operadores booleanos solo pueden operar con bool, no {type(izquierda)} y {type(derecha)}.")
                return None
            try:
                if operador == 'and':
                    return izquierda and derecha
                elif operador == 'or':
                    return izquierda or derecha
            except Exception as e:
                print(f"Error semantico: {e}")
                return None
        
        elif tipo_expresion == 'not':
            operando = self.evaluar_expresion(expresion[1])
            if type(operando) != bool:
                print(f"Error: Operador 'not' solo puede operar con bool, no {type(operando)}.")
                return None
            try:
                return not operando
            except Exception as e:
                print(f"Error semantico: {e}")
                return None
        
        elif tipo_expresion == 'id':
            nombre = expresion[1]
            if not self.tabla_simbolos.existe(nombre):
                print(f"Error: Variable '{nombre}' no declarada.")
                return None
            
            simbolo = self.tabla_simbolos.obtener(nombre)
            return simbolo["valor"]
            

    def tipo_expresion(self, expresion):
        tipo_expresion = expresion[0]

        if tipo_expresion == 'val':
            
            valor = expresion[1]
            
            if isinstance(valor, bool):
                return 'bool'
            elif isinstance(valor, int):
                return 'int'
            elif isinstance(valor, float):
                return 'float'
            
            #caso diferente para IDS y string
            elif isinstance(valor, str):
                return 'string'
            
        elif tipo_expresion == 'binop':
            izquierda = self.tipo_expresion(expresion[2])
            derecha = self.tipo_expresion(expresion[3])

            if izquierda != derecha:
                print(f"Error: Tipos no se pueden comparar: {izquierda} y {derecha}.")
                return None
            
            if izquierda == 'bool' or derecha == 'bool':
                print(f"Error: Operadores aritméticos no pueden operar con bool.")
                return None

            return izquierda  # El tipo de la expresión binaria es el mismo que el de sus operandos
        
        elif tipo_expresion == 'rel':
            izquierda = self.tipo_expresion(expresion[2])
            derecha = self.tipo_expresion(expresion[3])

            if izquierda != derecha:
                print(f"Error: Tipos no se pueden comparar: {izquierda} y {derecha}.")
                return None

            return 'bool'  # El resultado de una expresión relacional siempre es bool
        
        elif tipo_expresion == 'bool_op':
            izquierda = self.tipo_expresion(expresion[2])
            derecha = self.tipo_expresion(expresion[3])

            if izquierda != 'bool' or derecha != 'bool':
                print(f"Error: Operadores booleanos solo pueden operar con bool, no {izquierda} y {derecha}.")
                return None

            return 'bool'  # El resultado de una expresión booleana siempre es bool
        
        elif tipo_expresion == 'not':
            operando = self.tipo_expresion(expresion[1])

            if operando != 'bool':
                print(f"Error: Operador 'not' solo puede operar con bool, no {operando}.")
                return None

            return 'bool'
        
        elif tipo_expresion == 'id':
            nombre = expresion[1]
            if not self.tabla_simbolos.existe(nombre):
                print(f"Error: Variable '{nombre}' no declarada.")
                return None
            
            simbolo = self.tabla_simbolos.obtener(nombre)
            return simbolo["tipo"]
        