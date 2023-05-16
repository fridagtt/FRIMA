import ply.lex as lex

#__________LEXER____________

# Set of token names
tokens = [
    'COLON',
    'SEMICOLON',
    'COMMA',
    'LBRACKET',
    'RBRACKET',
    'LBRACE',
    'RBRACE',
    'LPAREN',
    'RPAREN',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'GREATER',
    'LESS',
    'GREATEREQ',
    'LESSEQ',
    'NOTEQUAL',
    'EQUAL',
    'ASSIGN',
    'ID',
    'CTEI',
    'CTEF',
    'CTECHAR',
    'CTESTRING',
    'ARROW',
]

# Keywords' declaration
reserved = {
    'programa' : 'PROGRAMA',
    'inicio' : 'INICIO',
    'entero' : 'ENTERO',
    'decimal' : 'DECIMAL',
    'letra' : 'LETRA',
    'variable' : 'VARIABLE',
    'renglon' : 'RENGLON',
    'tabla' : 'TABLA',
    'sinregresar' : 'SINREGRESAR',
    'si' : 'SI',
    'sino' : 'SINO',
    'desde' : 'DESDE',
    'hasta' : 'HASTA',
    'mientras' : 'MIENTRAS',
    'funcion' : 'FUNCION',
    'regresar' : 'REGRESAR',
    'imprimir' : 'IMPRIMIR',
    'leer' : 'LEER',
    'y' : 'Y',
    'o' : 'O',
}

tokens += reserved.values()

t_SEMICOLON = r'\;'
t_COMMA = r'\,'
t_COLON = r'\:'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_GREATER = r'\>'
t_LESS = r'\<'
t_GREATEREQ = r'\>='
t_LESSEQ = r'\<='
t_NOTEQUAL = r'\!='
t_EQUAL = r'\=='
t_ASSIGN = r'\='
t_ARROW = r'\->'
t_ignore  = ' \t' # Ignored characters (spaces and tabs)

def t_ID(t):
    r'[a-z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

def t_CTEF(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_CTEI(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CTESTRING(t):
    r'\".*?\"'
    t.type = 'CTESTRING'
    return t

def t_CTECHAR(t):
    r'\'[0-9A-Za-z*+-/=!¡¿?#$%&|_{}()]\''
    t.value = str(t.value)
    return t

# C or C++ comment (ignored characters)    
def t_code_comment(t):
    r'(/\*(.|\n)*?\*/)|(//.*)'
    pass

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule for lexer
def t_error(t):
    print("Character no válido'%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

# Segment for testing the lexer
"""
data = '''
si sino "" entero variable -14.5
decimal 'a' -> == 14.5 14 -14
  + - * / > = frida_98 "MariaRenee"
'''

lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: break # No more input
    print(tok)
"""