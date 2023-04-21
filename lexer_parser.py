import ply.lex as lex
import ply.yacc as yacc
import sys

from utils.symbol_table import *
from utils.semantic_cube import *

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

# Keywords declaration
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
    'porcada' : 'PORCADA',
    'en' : 'EN',
    'mientras' : 'MIENTRAS',
    'funcion' : 'FUNCION',
    'regresar' : 'REGRESAR',
    'imprimir' : 'IMPRIMIR',
    'leer' : 'LEER',
    'y' : 'y',
    'o' : 'o',
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
    t.lexer.lineno += t.value.count("\n")

# Error handling rule
def t_error(t):
    print("Character no válido'%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
start = 'programa'

"""
#Testing the lexer
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

#__________PARSER____________

# Define the grammars
def p_programa(p):
  '''
  programa : PROGRAMA ID punto_programa COLON inicio
          | PROGRAMA ID punto_programa COLON dec_var_cycle inicio
          | PROGRAMA ID punto_programa COLON dec_var_cycle dec_func inicio
          | PROGRAMA ID punto_programa COLON dec_func inicio
  '''
  p[0] = None

def p_dec_var_cycle(p):
  '''
  dec_var_cycle : dec_var dec_var_cycle
                | empty
  '''

def p_punto_programa(p):
  '''
  punto_programa : 
  '''
  global dir_func, current_func
  dir_func = SymbolTable()
  current_func = "programa"
  dir_func.symbol_table['dir_functions']['dir_func_names'].add("programa")

def p_inicio(p):
  '''
  inicio : INICIO LPAREN RPAREN LBRACE estatutos RBRACE SEMICOLON
  '''
  p[0] = None

def p_dec_var(p):
  '''
  dec_var : simple_var
          | array
          | matrix
  '''
  p[0] = None

def p_simple_var(p):
  '''
  simple_var : VARIABLE type ARROW ID punto_simple_var simpleVarCycle SEMICOLON
  simpleVarCycle : COMMA ID punto_simple_var simpleVarCycle
                  | empty
  '''
  p[0] = None

def p_punto_simple_var(p):
  '''
  punto_simple_var :
  '''
  dir_func.add_variable(current_var_type, p[-1], current_func)
  print("dir_func", dir_func.symbol_table)

def p_type(p):
  '''
  type : ENTERO
      | DECIMAL
      | LETRA
  '''
  p[0] = p[1]
  global current_var_type

  if p[0] == 'entero':
    current_var_type = 1
  elif p[0] == 'decimal':
    current_var_type = 2
  elif p[0] == 'letra':
    current_var_type = 3

def p_array(p):
  '''
  array : RENGLON type ARROW ID LBRACKET CTEI RBRACKET arrayCycle SEMICOLON
  arrayCycle : COMMA ID LBRACKET CTEI RBRACKET arrayCycle
              | empty
  '''
  p[0] = None

def p_matrix(p):
  '''
  matrix : TABLA type ARROW ID LBRACKET CTEI RBRACKET LBRACKET CTEI RBRACKET matrixCycle SEMICOLON
  matrixCycle : COMMA ID LBRACKET CTEI RBRACKET LBRACKET CTEI RBRACKET matrixCycle
              | empty
  '''
  p[0] = None

def p_dec_func(p):
  '''
  dec_func : FUNCION dec_func_return punto_dec_func ID LPAREN parameter RPAREN LBRACE dec_var estatutos decFuncCycle REGRESAR variable SEMICOLON RBRACE SEMICOLON
  dec_func_return : type
                  | SINREGRESAR
  decFuncCycle : estatutos decFuncCycle
              | empty 
  '''
  p[0] = None

def p_punto_dec_func(p):
  '''
  punto_dec_func: 
  '''
  global func_return_type
  func_return_type = p[-1]

def p_parameter(p):
  '''
  parameter : type ID parameterCycle 
  parameterCycle : COMMA type ID parameterCycle
                  | empty 
  '''
  p[0] = None

def p_estatutos(p):
  '''
  estatutos : asignar
          | llamada_func
          | ciclo_for
          | ciclo_while
          | condicion
          | escribe
          | leer
          | empty
  '''
  p[0] = None

def p_asignar(p):
  '''
  asignar : variable ASSIGN exp SEMICOLON
  '''
  p[0] = None

def p_variable(p):
  '''
  variable : ID variable_aux
  variable_aux : LBRACKET exp RBRACKET
              | LBRACKET exp RBRACKET LBRACKET exp RBRACKET
              | empty
  '''
  p[0] = None

def p_leer(p):
  '''
  leer : LEER variable SEMICOLON
  '''
  p[0] = None

def p_ciclo_while(p):
  '''
  ciclo_while : MIENTRAS LPAREN exp RPAREN LBRACE estatutos whileCycle RBRACE SEMICOLON
  whileCycle : estatutos whileCycle
              | empty
  '''
  p[0] = None

def p_ciclo_for(p):
  '''
  ciclo_for : PORCADA exp EN exp LBRACE estatutos forCycle RBRACE SEMICOLON
  forCycle : estatutos forCycle
          | empty
  '''
  p[0] = None

def p_condicion(p):
  '''
  condicion : SI LPAREN exp RPAREN LBRACE estatutos condicionCycle RBRACE sinoCondicion SEMICOLON
  condicionCycle : estatutos condicionCycle
              | empty
  sinoCondicion : SINO LBRACE estatutos condicionCycle RBRACE
              | empty
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
  factor : factor_constante
          | factor_variable
          | factor_expresion
  factor_constante : CTEI
                  | CTEF
  factor_variable : ID
                  | ID LBRACKET exp RBRACKET
                  | ID LBRACKET exp RBRACKET LBRACKET exp RBRACKET
                  | ID llamada_func
  factor_expresion : LPAREN exp RPAREN
  '''
  p[0] = None 

def p_llamada_func(p):
  '''
  llamada_func : ID LPAREN llamadaCYCLE RPAREN SEMICOLON
  llamadaCYCLE : exp llamadaCYCLE_aux
              | empty
  llamadaCYCLE_aux : COMMA exp llamadaCYCLE_aux
                  | empty
  '''
  p[0] = None 

def p_escribe(p):
  '''
  escribe : IMPRIMIR LPAREN escribe_aux RPAREN SEMICOLON
  escribe_aux : exp escribeCycle
              | CTESTRING escribeCycle
  escribeCycle : COMMA escribe_aux
              | empty
  '''
  p[0] = None

def p_empty(p):
  '''
  empty : 
  '''
  pass

def p_error(p):
  print("Syntax error at token", p.type)

parser = yacc.yacc()

def readFile():
  #Testear el parser y léxico juntos
  try:
      file = open("./tests/examples.txt", "r")
      print(f"PLY LEXER AND PARSER")
      archivo = file.read()
      file.close()
      parser.parse(archivo)
  except EOFError:
      print('ERROR')

if __name__ == '__main__':
	readFile()