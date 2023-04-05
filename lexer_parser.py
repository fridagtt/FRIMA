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

#Declarar las keywords
reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'program' : 'PROGRAM',
    'var' : 'VAR',
    'print' : 'PRINT',
    'int' : 'INT',
    'float' : 'FLOAT',
}

tokens += reserved.values()

t_COLON = r':'
t_SEMICOLON = r';'
t_COMMA = r','
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_GREATER = r'>'
t_LESS = r'<'
t_NOTEQUAL = r'<>'
t_ASSIGN = r'='

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
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
    r'"[a-zA-Z0-9!@#$%^&*()]*"'
    t.type = 'CTESTRING'
    return t

def t_newline(t):
    r'\n+'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

#Testear el léxico
"""
lexer.input('if else print program var print int float 14.5 14 + - * / > = frida_98 "Frida"')

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
"""

#__________PARSER____________

#Definir las gramáticas
def p_program(p):
    '''
    program : PROGRAM ID SEMICOLON programT bloque
    programT : vars
             | empty
    '''
    p[0] = None

def p_vars(p):
    '''
    vars : VAR ID varsT COLON tipo SEMICOLON varsF
    varsT : COMMA ID varsT
          | empty
    varsF : ID varsT COLON tipo SEMICOLON varsF
          | empty
    '''
    p[0] = None

def p_tipo(p):
    '''
    tipo : INT
         | FLOAT
    '''
    p[0] = None

def p_bloque(p):
    '''
    bloque : LBRACKET bloqueT RBRACKET
    bloqueT : estatuto bloqueT
            | empty
    '''
    p[0] = None

def p_estatuto(p):
    '''
    estatuto : asignacion
             | condicion
             | escritura
    '''
    p[0] = None

def p_asignacion(p):
    '''
    asignacion : ID ASSIGN expresion SEMICOLON
    '''
    p[0] = None

def p_escritura(p):
    '''
    escritura : PRINT LBRACKET escrituraT RBRACKET SEMICOLON
    escrituraT : expresion escrituraF
               | CTESTRING escrituraF
    escrituraF : COMMA escrituraT
               | empty
    '''
    p[0] = None

def p_expresion(p):
    '''
    expresion : exp expresionT
    expresionT : GREATER exp
               | LESS exp
               | NOTEQUAL exp
               | empty
    '''
    p[0] = None

def p_condicion(p):
    '''
    condicion : IF LPAREN expresion RPAREN bloque condicionT
    condicionT : ELSE bloque
               | SEMICOLON
    '''
    p[0] = None

def p_exp(p):
    '''
    exp : termino expT
    expT : PLUS exp
         | MINUS exp
         | empty
    '''
    p[0] = None

def p_termino(p):
    '''
    termino : factor terminoT
    terminoT : TIMES termino
             | DIVIDE termino
             | empty
    '''
    p[0] = None

def p_factor(p):
    '''
    factor : LPAREN expresion RPAREN
           | factorT
    factorT : factorF varcte
    factorF : PLUS
            | MINUS
            | empty
    '''
    p[0] = None

def p_varcte(p):
    '''
    varcte : ID
            | CTEI
            | CTEF
    '''
    p[0] = None

def p_empty(p):
    '''
    empty : 
    '''
    p[0] = None

def p_error(p):
    print("Syntax error at token", p.type)

parser = yacc.yacc()

#Analizar el archivo con los ejemplos
try:
    file = open("ejemplos.txt", "r")
    print(f"PLY LEXER AND PARSER")
    for line in file:
        parser.parse(line)
        print(f"approved line: {line}")
except EOFError:
    print('ERROR')
