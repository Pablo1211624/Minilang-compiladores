import ply.lex as lex
from tokens import tokens, keywords


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
    r'\n[ \t]*'
    t.lexer.lineno += t.value.count('\n')
    
    # Calcular la columna de la nueva línea
    espacios = t.value.split('\n')[-1]
    col = 0
    for char in espacios:
        if char == ' ': col += 1
        elif char == '\t': col += 4 # O tu tabsize
        
    cima = pila_indentacion[-1]
    
    if col > cima:
        pila_indentacion.append(col)
        t.type = 'INDENT'
        return t
    elif col < cima:
        # Generar múltiples DEDENTs si es necesario
        while col < pila_indentacion[-1]:
            pila_indentacion.pop()
            dedents_pendientes.append('DEDENT')
        
        if dedents_pendientes:
            t.type = dedents_pendientes.pop(0)
            return t
    
    # Si col == cima, es solo un cambio de línea, no cambia indentación
    # Pero el parser necesita saber que terminó la sentencia
    t.type = 'NEWLINE'
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
    columna = find_column(t.lexer.lexdata, t)
    print(f"[{t.lexer.lineno}:{columna}] TOKEN: {t.type:<10} | Valor: '{t.value}'")
    linea_token = True
    return t


def t_FLOTANTE(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    global linea_token
    col = find_column(t.lexer.lexdata, t)
    print(f"[{t.lexer.lineno}:{col}] TOKEN: FLOTANTE     | Valor: '{t.value}'")
    linea_token = True
    return t

def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    global linea_token
    col = find_column(t.lexer.lexdata, t)
    print(f"[{t.lexer.lineno}:{col}] TOKEN: ENTERO     | Valor: '{t.value}'")
    linea_token = True
    return t


def t_CADENA(t):
    r'"([^"\\]|\\.)*"'
    global linea_token
    col = find_column(t.lexer.lexdata, t)
    print(f"[{t.lexer.lineno}:{col}] TOKEN: CADENA    | Valor: '{t.value}'")
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
