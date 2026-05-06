import ply.yacc as yacc
from lexico import lexer, find_column
from tokens import tokens, keywords

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