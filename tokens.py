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
    "const": "KW_CONST",
}

tokens += list(set(keywords.values()))
