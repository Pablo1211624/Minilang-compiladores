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
            self.tabla_simbolos.declarar(nombre, tipo) #declaramos la variable en la tabla de simbolos


        #se declara y se asigna valor
        elif tipo_produccion == 'decl_assign':
            tipo = produccion[1]
            nombre = produccion[2] 
            valor = self.evaluar_expresion(produccion[3]) #valor asignado
            self.tabla_simbolos.declarar(nombre, tipo, valor)

        #se declara una constante sin valor
        elif tipo_produccion == 'const_decl':
            tipo = produccion[1] 
            nombre = produccion[2] 
            self.tabla_simbolos.declarar(nombre, tipo, constante=True) #declaramos la constante en la tabla de simbolos

        #se declara una constante con valor
        elif tipo_produccion == 'const_decl_assign':
            tipo = produccion[1] 
            nombre = produccion[2] 
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

            if simbolo["constante"]:
                print(f"Error: No se puede asignar a la constante '{nombre}'.")
                return

            self.tabla_simbolos.insertar(nombre, valor) #actualizamos el valor de la variable en la tabla de simbolos

    def evaluar_expresion(self, expresion):
        #se hara verificaciones de tipos y acciones semanticas relacionadas a las expresiones
        return 