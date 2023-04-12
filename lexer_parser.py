import ply.lex as lex
import ply.yacc as yacc
import sys

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
    'NOTEQUAL',
    'ASSIGN',
    'ID',
    'CTEI',
    'CTEF',
    'CTESTRING',
]

# Keywords declaration
reserved = {
    'parar' : 'PARAR',
    'opciones' : 'OPCIONES',
    'opcion' : 'OPCION',
    'sino' : 'SINO',
    'constante' : 'CONSTANTE',
    'entero' : 'ENTERO',
    'decimal' : 'DECIMAL',
    'frase' : 'FRASE',
    'renglon' : 'RENGLON',
    'sinregresar' : 'SINREGRESAR',
    'si' : 'SI',
    'entonces' : 'ENTONCES',
    'porcada' : 'PORCADA',
    'mientras' : 'MIENTRAS',
    'funcion' : 'FUNCION',
    'regresar' : 'REGRESAR',
    'tam' : 'TAM',
    'imprimir' : 'IMPRIMIR',
    'x' : 'X',
}

tokens += reserved.values()

t_COLON = r':'
t_SEMICOLON = r';'
t_COMMA = r','
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_GREATER = r'>'
t_LESS = r'<'
t_NOTEQUAL = r'!='
t_ASSIGN = r'='

# Ignored characters (spaces and tabs)
t_ignore  = ' \t'

def t_ID(t):
    r'[a-z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

def t_CTEF(t):
    r'[-]?\d+\.\d+'
    t.value = float(t.value)
    return t

def t_CTEI(t):
    r'[-]?\d+'
    t.value = int(t.value)
    return t

def t_CTESTRING(t):
    r'\".*?\"'
    t.type = 'CTESTRING'
    return t

# C or C++ comment (ignore)    
def t_ccode_comment(t):
    r'(/\*(.|\n)*?\*/)|(//.*)'
    pass

def t_newline(t):
    r'\n+'

# Error handling rule
def t_error(t):
    print("Character no válido'%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

#Testear el léxico
"""
lexer.input('si sino "" entero decimal 14.5 14 + - * / > = frida_98 "MariaRenee"')

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
"""

#__________PARSER____________

#Gramaticas FRIMA
def p_var(p):
    '''
    var : varType ID varsCycle SEMICOLON
    varsCycle : COMMA ID varsCycle
            | empty
    varType : simple_type
            | complex_type
    '''
    p[0] = None

def p_arr(p):
    '''
    arr : RENGLON simple_type ID TAM exp SEMICOLON
    '''
    p[0] = None

def p_func(p):
    '''
    func : FUNCION returnType ID LPAREN parameter RPAREN body SEMICOLON 
    returnType : simple_type | SINREGRESAR
    '''
    p[0] = None 

def p_parameter(p):
    '''
    parameter : simple_type ID parameterCycle 
    parameterCycle : COMMA simple_type ID parameterCycle | empty 
    '''
    p[0] = None 

def p_exp(p):
    '''
    exp : term expT
    expT : PLUS exp
         | MINUS exp
         | empty
    '''
    p[0] = None

def p_term(p):
    '''
    term : factor termT
    termT : TIMES term
            | DIVIDE term
            | empty
    '''
    p[0] = None

def p_factor(p):
    '''
    factor : numeric | arrPos 
    numeric: varCTE
    arrPos : LBRACKET exp RBRACKET 
    '''
    p[0] = None 

def p_varCTE(p):
    '''
    varCTE : CTEI | CTEF | ID
    '''
    p[0] = None 

def simple_type(p):
    '''
    simple_type : ENTERO | DECIMAL
    '''
    p[0] = None 

def complex_type(p):
    '''
    complex_type : RENGLON | FRASE 
    '''
    p[0] = None

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print("Syntax error at token", p.type)

parser = yacc.yacc()

#Testear el parcer y léxico juntos
"""
#Analizar el archivo con los ejemplos
try:
    file = open("ejemplos.txt", "r")
    print(f"PLY LEXER AND PARSER")
    for line in file:
        parser.parse(line)
        print(f"approved line: {line}")
except EOFError:
    print('ERROR')
"""
