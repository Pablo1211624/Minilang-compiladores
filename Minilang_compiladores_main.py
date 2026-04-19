#! /usr/bin/env python3
import ply.lex as lex
import ply.yacc as yacc
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys

# ---------------------------------
# TOKENS
# ---------------------------------
tokens = [
    'ID', 'ENTERO', 'FLOTANTE', 'CADENA',

    'PLUS', 'MINUS', 'STAR', 'SLASH', 'MOD',

    'LT', 'GT', 'LE', 'GE', 'EQEQ', 'NE', 'EQ',

    'LPARENTESIS', 'RPARENTESIS',
    'LLLAVE', 'RLLAVE',

    'PUNTOPUNTO', 'COMA',

    'NEWLINE', 'INDENT', 'DEDENT'
]

# ---------------------------------
# KEYWORDS
# ---------------------------------
keywords = {
    "int": "KW_INT",
    "float": "KW_FLOAT",
    "string": "KW_STRING",
    "bool": "KW_BOOL",
    "if": "KW_IF",
    "else": "KW_ELSE",
    "while": "KW_WHILE",
    "func": "KW_FUNC",
    "Read": "KW_READ",
    "Write": "KW_WRITE",
    "true": "BOOL",
    "false": "BOOL",
    "and": "AND",
    "or": "OR",
    "not": "NOT",
}

tokens += list(set(keywords.values()))


pila_indentacion = [0]
inicio_linea = True
linea_token = False
tabsize = 4
dedents_pendientes = []
hay_error = False

t_PLUS = r'\+'
t_MINUS = r'-'
t_STAR = r'\*'
t_SLASH = r'/'
t_MOD = r'%'

t_EQEQ = r'=='
t_NE = r'!='
t_LE = r'<='
t_GE = r'>='
t_LT = r'<'
t_GT = r'>'
t_EQ = r'='

t_LPARENTESIS = r'\('
t_RPARENTESIS = r'\)'
t_LLLAVE = r'\{'
t_RLLAVE = r'\}'

t_PUNTOPUNTO = r':'
t_COMA = r','

t_ignore = ' \r'


def t_comment(t):
    r'\#.*'
    pass

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    global inicio_linea
    inicio_linea = True
    return t

def t_INDENT(t):
    r'[ \t]+'
    global inicio_linea, pila_indentacion, dedents_pendientes
    if not inicio_linea:
        return

    col = 0
    for ch in t.value:
        if ch == ' ': col += 1
        else: col += tabsize - (col % tabsize)
    
    cima = pila_indentacion[-1]
    if col > cima:
        pila_indentacion.append(col)
        t.type = 'INDENT'
        inicio_linea = False
        return t
    elif col < cima:
        while len(pila_indentacion) > 1 and pila_indentacion[-1] > col:
            pila_indentacion.pop()
            dedents_pendientes.append('DEDENT')
        if dedents_pendientes:
            t.type = dedents_pendientes.pop(0)
            inicio_linea = False
            return t
    inicio_linea = False

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    global linea_token

    if len(t.value) > 31:
        print(f"Error: ID muy largo en linea {t.lexer.lineno}")
        t.value = t.value[:31]

    t.type = keywords.get(t.value, 'ID')
    print("TOKEN:", t.type, t.value)
    linea_token = True
    return t


def t_FLOTANTE(t):
    r'\d+\.\d+'
    global linea_token
    linea_token = True
    return t

def t_ENTERO(t):
    r'\d+'
    global linea_token
    linea_token = True
    return t


def t_CADENA(t):
    r'"([^"\\]|\\.)*"'
    global linea_token
    linea_token = True
    return t

#Error lexico
def t_error(t):
    col = find_column(t.lexer.lexdata, t)
    print(f"Linea {t.lexer.lineno}, Columna {col}, Simbolo '{t.value[0]}', Error: Caracter ilegal")
    t.lexer.skip(1)

lexer = lex.lex()

def find_column(input, token):
    last_cr = input.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = -1
    return (token.lexpos - last_cr)


precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('nonassoc', 'LT', 'GT', 'LE', 'GE', 'EQEQ', 'NE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'STAR', 'SLASH', 'MOD'),
)

def p_programa(p):
    'programa : sentencias'
    p[0] = ('programa', p[1])

def p_sentencias(p):
    '''sentencias : bloque_sentencia sentencias
                  | empty'''
    if len(p) == 3:
        p[0] = ([p[1]] + p[2]) if p[1] is not None else p[2]
    else:
        p[0] = []

def p_bloque_sentencia(p):
    '''bloque_sentencia : sentencia NEWLINE
                        | sentencia
                        | NEWLINE'''
    p[0] = p[1]

def p_sentencia(p):
    '''sentencia : declaracion_variable
                 | asignacion
                 | sentencia_if
                 | sentencia_while
                 | entrada_salida
                 | funcion'''
    p[0] = p[1]
    
def p_sentencia_error(p):
    'sentencia : error NEWLINE'
    global hay_error
    hay_error = True
    print(f"Error recuperado en linea {p.lineno(1)}")
    parser.errok()
    
def p_empty(p):
    'empty :'
    pass

def p_declaracion_variable(p):
    '''declaracion_variable : tipo ID
                            | tipo ID EQ expresion'''
    if len(p) == 3:
        p[0] = ('decl', p[1], p[2])
    else:
        p[0] = ('decl_assign', p[1], p[2], p[4])

def p_asignacion(p):
    'asignacion : ID EQ expresion'
    p[0] = ('assign', p[1], p[3])

def p_tipo(p):
    '''tipo : KW_INT
            | KW_FLOAT
            | KW_STRING
            | KW_BOOL'''
    p[0] = p[1]

# IF / ELSE
def p_if(p):
    '''sentencia_if : KW_IF expresion_booleana PUNTOPUNTO bloque
                    | KW_IF expresion_booleana PUNTOPUNTO bloque KW_ELSE PUNTOPUNTO bloque'''
    
    if len(p) == 5:
        p[0] = ('if', p[2], p[4], None)
    else:
        p[0] = ('if', p[2], p[4], p[7])      

# WHILE
def p_while(p):
    'sentencia_while : KW_WHILE expresion_booleana PUNTOPUNTO bloque'
    p[0] = ('while', p[2], p[4])

# Funcion
def p_funcion(p):
    'funcion : KW_FUNC ID LPARENTESIS parametros RPARENTESIS PUNTOPUNTO bloque'
    p[0] = ('func', p[2], p[4], p[7])
    
# Parametros
def p_parametros(p):
    '''parametros : tipo ID
                  | tipo ID COMA parametros
                  | empty'''
    if len(p) == 3:
        p[0] = [(p[1], p[2])]
    elif len(p) == 5:
        p[0] = [(p[1], p[2])] + p[4]
    else:
        p[0] = []
 
#Argumentps
def p_argumentos(p):
    '''argumentos : expresion
                  | expresion COMA argumentos
                  | empty'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = []
        
# BLOQUE (INDENT)
def p_bloque(p):
    '''bloque : NEWLINE INDENT sentencias DEDENT
              | INDENT sentencias DEDENT'''
    p[0] = p[3] if len(p) == 5 else p[2]


def p_io(p):
    '''entrada_salida : KW_READ LPARENTESIS ID RPARENTESIS
                      | KW_WRITE LPARENTESIS expresion RPARENTESIS'''
    if p[1] == 'Read' or p.slice[1].type == 'KW_READ':
        p[0] = ('read', p[3])
    else:
        p[0] = ('write', p[3])


def p_bool_bin(p):
    '''expresion_booleana : expresion_booleana AND expresion_booleana
                          | expresion_booleana OR expresion_booleana'''
    p[0] = ('bool_op', p[2], p[1], p[3])

def p_bool_not(p):
    'expresion_booleana : NOT expresion_booleana'
    p[0] = ('not', p[2])

def p_bool_rel(p):
    'expresion_booleana : expresion operador_relacional expresion'
    p[0] = ('rel', p[2], p[1], p[3])

def p_bool_val(p):
    'expresion_booleana : BOOL'
    p[0] = ('bool', p[1])

def p_bool_paren(p):
    'expresion_booleana : LPARENTESIS expresion_booleana RPARENTESIS'
    p[0] = p[2]

def p_relop(p):
    '''operador_relacional : LT
                           | GT
                           | LE
                           | GE
                           | EQEQ
                           | NE'''
    p[0] = p[1]

# EXPRESIONES
def p_expr(p):
    '''expresion : expresion PLUS termino
                 | expresion MINUS termino'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expr_term(p):
    'expresion : termino'
    p[0] = p[1]

def p_term(p):
    '''termino : termino STAR factor
               | termino SLASH factor
               | termino MOD factor'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_term_factor(p):
    'termino : factor'
    p[0] = p[1]

def p_factor(p):
    '''factor : ID
              | ENTERO
              | FLOTANTE
              | CADENA
              | LPARENTESIS expresion RPARENTESIS
              | ID LPARENTESIS argumentos RPARENTESIS'''
    
    if len(p) == 2:
        p[0] = ('val', p[1])
    elif len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = ('call', p[1], p[3])

#Error Sintactico
def p_error(p):
    global hay_error
    hay_error = True

    if p:
        col = find_column(p.lexer.lexdata, p)
        print(f"Linea {p.lineno}, Columna {col}, Simbolo '{p.value}', Error: sintaxis invalida")
        parser.errok()
    else:
        print("Error de sintaxis: Fin de archivo inesperado")

parser = yacc.yacc()


if __name__ == "__main__":
    archivo_test = "pruebas/prueba3Input.mlng" 
    
    try:
        with open(archivo_test, "r", encoding="utf-8") as f:
            data = f.read() + '\n'
            print(f"--- Analizando: {archivo_test} ---")
            
            data += '\n' 
            pila_indentacion = [0]
            dedents_pendientes = []
            inicio_linea = True
            linea_token = False
            hay_error = False
            data += '\n'
            resultado = parser.parse(data, lexer=lexer)
            
            if not hay_error:
                print("OK")
                print("Arbol:", resultado)
            else:
                print("Se encontraron errores")
                
    except FileNotFoundError:
        print(f"Error: No se encontro el archivo en la ruta: {archivo_test}")
    except Exception as e:
        print(f"Ocurrio un error inesperado: {e}")

class RedireccionConsola:
    def __init__(self, widget_texto):
        self.widget = widget_texto
    def write(self, string):
        self.widget.config(state=tk.NORMAL)
        self.widget.insert(tk.END, string)
        self.widget.see(tk.END)
        self.widget.config(state=tk.DISABLED)
    def flush(self):
        pass


class interfazGrafica:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MiniLang (Fase 2)")
        self.root.geometry("926x700")
        self.root.configure(bg="#201F1F")

        self.archivoActual = None
        self.FONDO = "#201F1F"
        self.BarraLAT = "#252526"
        self.BarraARRIBA = "#121212"
        self.BarraARRIBAB = "#3F3F3F"
        self.BarraOPCIONES = "#343333"
        self.ExplTexto = "#cccccc"

        self.barraOpc = tk.Frame(self.root, bg=self.BarraOPCIONES, width=50)
        self.barraOpc.pack(side="left", fill="y")
        tk.Button(self.barraOpc, text="archivos", bg=self.BarraOPCIONES, fg="white", relief="flat", command=self.abrirArchivo).pack(pady=10, fill="x")
        tk.Button(self.barraOpc, text="verificar", bg=self.BarraOPCIONES, fg="#5efff2", relief="flat", command=self.analizar).pack(pady=10, fill="x")

        self.barraL = tk.Frame(self.root, bg=self.BarraLAT, width=140)
        self.barraL.pack(side="left", fill="y")
        self.barraL.pack_propagate(False)
        tk.Label(self.barraL, text="EXPLORER", bg=self.BarraLAT, fg=self.ExplTexto, font=("Consolas", 9, "bold")).pack(pady=10, padx=5)
        self.archivoMuestra = tk.Label(self.barraL, text=" ", bg=self.BarraLAT, fg="#858585", font=("Consolas",9))
        self.archivoMuestra.pack(pady=5)

        self.barraA = tk.Frame(self.root, bg=self.BarraARRIBA, height=23)
        self.barraA.pack(side="top", fill="x")

        self.barraAB = tk.Frame(self.root, bg=self.BarraARRIBAB, height=5)
        self.barraAB.pack(side="top", fill="x")

        self.cuadroTexto = tk.Frame(self.root, bg=self.FONDO)
        self.cuadroTexto.pack(side="right", expand=True, fill="both")
        self.editor = tk.Text(self.cuadroTexto, bg=self.FONDO, fg="#e3dada", insertbackground="white", relief="flat", font=("Consolas", 11), padx=10, pady=10, undo=True, wrap=tk.NONE)
        self.editor.pack(expand=True, fill="both")

        self.consolaMensaje = tk.Text(self.cuadroTexto, bg="#111111", fg="#fffb00", height=10, relief="flat", font=("Consolas", 10), padx=10, pady=10)
        self.consolaMensaje.pack(side="bottom", fill="x")

        sys.stdout=RedireccionConsola( self.consolaMensaje)
        
        print("C:/users/personaprueba/downloads/minilang> subir un archivo .mlng y luego presione analizar")

        self.root.mainloop()

    def terminal(self, mensaje):
        self.consolaMensaje.config(state=tk.NORMAL)
        self.consolaMensaje.insert(tk.END, f">{mensaje}\n")
        self.consolaMensaje.config(state=tk.DISABLED)
        self.consolaMensaje.see(tk.END)

    def abrirArchivo(self):
        initial_dir = os.path.join(os.getcwd(), "pruebas")
        if not os.path.exists(initial_dir): initial_dir = os.getcwd()
        filepath = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("Minilang", "*.mlng"),("Legacy", "*.mlng")])
        if filepath:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.editor.delete(1.0, tk.END)
                self.editor.insert(1.0, f.read())
            self.archivoActual = filepath
            self.archivoMuestra.config(text=os.path.basename(filepath), fg="#e5e9ee")
            print(f"Archivo cargado: {filepath}")

    def analizar(self):
        global pila_indentacion, dedents_pendientes, inicio_linea, linea_token, hay_error
        
        codigo = self.editor.get(1.0, tk.END)
        if not codigo.endswith('\n'):
            codigo += '\n'
        codigo += '\n' 
        lexer.lineno=1
        pila_indentacion=[0]
        dedents_pendientes=[]
        inicio_linea = True
        linea_token = False
        hay_error = False

        self.consolaMensaje.config(state=tk.NORMAL)
        self.consolaMensaje.delete(1.0, tk.END)
        self.consolaMensaje.config(state=tk.DISABLED)
        try:
            resultado = parser.parse(codigo, lexer=lexer)
            if self.archivoActual:
                nombreSinExte = os.path.splitext(os.path.basename(self.archivoActual))[0]
                if not os.path.exists("salidas"): os.makedirs("salidas")
                rutaOut = os.path.join("salidas", nombreSinExte + ".out")
                contenidocompleto=self.consolaMensaje.get(1.0,tk.END)
                with open(rutaOut, "w", encoding="utf-8") as archivoout:
                    archivoout.write(contenidocompleto.strip())
                    archivoout.write("\nArbol:"+str(resultado)) 
                print(f"Archivo out (la salida de errores) se ha guardado en: {rutaOut}")

            if not hay_error:
                print("OK")
                print(f"Arbol:{resultado}")
            else:
                print("Se encontraron errores")
        
        except Exception as e:
            print(f"Ocurrio un error inesperado: {e}")

if __name__ == "__main__":
    interfazGrafica()
