import ply.lex as lex
import ply.yacc as yacc
import sys

from collections import deque

from utils.symbol_table import *
from utils.semantic_cube import *
from utils.quadruples import *
from utils.shared import *

# Create global variables
stack_de_operadores = deque()
stack_de_operandos = deque()
stack_de_tipos = deque()
lista_de_cuadruplos = []

cubo_semantico = SemanticCube()

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
          | PROGRAMA ID punto_programa COLON dec_var_cycle dec_func_cycle inicio
          | PROGRAMA ID punto_programa COLON dec_func_cycle inicio
  '''
  p[0] = None

def p_dec_var_cycle(p):
  '''
  dec_var_cycle : dec_var dec_var_cycle
                | empty
  '''

def p_dec_func_cycle(p):
  '''
  dec_func_cycle : dec_func dec_func_cycle
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
  for quadruple in lista_de_cuadruplos: 
    print(quadruple) 

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

def p_type(p):
  '''
  type : ENTERO
      | DECIMAL
      | LETRA
  '''
  p[0] = p[1]
  global current_var_type

  current_var_type = convert_type(p[0])

def p_array(p):
  '''
  array : RENGLON type ARROW ID LBRACKET CTEI RBRACKET punto_array arrayCycle SEMICOLON
  arrayCycle : COMMA ID LBRACKET CTEI RBRACKET punto_array arrayCycle
              | empty
  '''
  p[0] = None

def p_punto_array(p):
  '''
  punto_array :
  '''
  dir_func.add_variable(current_var_type, p[-4], current_func, 1, p[-2])

def p_matrix(p):
  '''
  matrix : TABLA type ARROW ID LBRACKET CTEI RBRACKET LBRACKET CTEI RBRACKET punto_matrix matrixCycle SEMICOLON
  matrixCycle : COMMA ID LBRACKET CTEI RBRACKET LBRACKET CTEI RBRACKET punto_matrix matrixCycle
              | empty
  '''
  p[0] = None

def p_punto_matrix(p):
  '''
  punto_matrix :
  '''
  dir_func.add_variable(current_var_type, p[-7], current_func, 2, (p[-5],p[-2]))

def p_dec_func(p):
  '''
  dec_func : FUNCION dec_func_type ID punto_add_func LPAREN parameter RPAREN LBRACE dec_var_cycle estatutos decFuncCycle dec_func_regresar RBRACE SEMICOLON
  decFuncCycle : estatutos decFuncCycle
              | empty 
  '''
def p_dec_func_regresar(p):
  '''
  dec_func_regresar : REGRESAR variable SEMICOLON
                    | empty
  '''
  p[0] = p[1]

def p_dec_func_type(p):
  '''
  dec_func_type : type
                | SINREGRESAR
  '''
  p[0] = p[1]

def p_punto_add_func(p):
    '''
    punto_add_func :
    '''
    global current_func
    current_func = p[-1]
    dir_func.add_function(p[-1], convert_type(p[-2]))

def p_parameter(p):
  '''
  parameter : type ID punto_parameter parameterCycle
            | empty
  parameterCycle : COMMA type ID punto_parameter parameterCycle
                  | empty 
  '''
  p[0] = None

def p_punto_parameter(p):
  '''
  punto_parameter :
  '''
  dir_func.add_function_params(current_func, convert_type(p[-2]), p[-1])

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
  asignar : variable ASSIGN hyper_exp SEMICOLON
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

#Operadores logicos y,o
def p_hyper_exp(p):
  '''
  hyper_exp : super_exp hyper_exp_aux
  '''
 
def p_hyper_exp_aux(p):
  '''
  hyper_exp_aux : push_op_logicos super_exp check_op_logicos
                    | empty
  '''

def p_check_op_logicos(p):
  '''
  check_op_logicos :
  '''
  global stack_de_operadores, stack_de_operandos, stack_de_tipos, lista_de_cuadruplos
  if len(stack_de_operadores) != 0:
    top_operador = stack_de_operadores.pop()
    if top_operador == 'y' or top_operador == 'o':
      operando_der = stack_de_operandos.pop()
      operando_izq = stack_de_operandos.pop()

      tipo_operando_der = stack_de_tipos.pop()
      tipo_operando_izq = stack_de_tipos.pop()

      converted_operador = convert_type(top_operador)

      operation_type = cubo_semantico.get_type(tipo_operando_izq, tipo_operando_der, converted_operador)
      if operation_type == 5:
        raise Exception("ERROR: Type Mismatch")
      else:
        temporal_variable = None
        quadruple = Quadruple(converted_operador, operando_izq, operando_der, temporal_variable)
        lista_de_cuadruplos.append(quadruple)
        stack_de_operandos.append(temporal_variable)
        stack_de_tipos.append(operation_type)
      
    else:
      stack_de_operadores.append(top_operador)

def p_push_op_logicos(p):
  '''
  push_op_logicos : Y 
        | O 
        | empty
  '''
  p[0] = p[1]
  stack_de_operadores.append(p[0])

#Operadores relacionales <,>,>=,<=,!=,==
def p_super_exp(p):
  '''
  super_exp : exp super_exp_aux
  '''

def p_super_exp_aux(p):
  '''
  super_exp_aux : push_op_relacionales exp check_op_relacionales
                | empty
  '''

def p_check_op_relacionales(p):
  '''
  check_op_relacionales :
  '''
  global stack_de_operadores, stack_de_operandos, stack_de_tipos, lista_de_cuadruplos
  if len(stack_de_operadores) != 0:
    top_operador = stack_de_operadores.pop()
    if top_operador == '>' or top_operador == '<' or top_operador == '<=' or top_operador == '>=' or top_operador == '!=' or top_operador == '==':
      operando_der = stack_de_operandos.pop()
      operando_izq = stack_de_operandos.pop()

      tipo_operando_der = stack_de_tipos.pop()
      tipo_operando_izq = stack_de_tipos.pop()

      converted_operador = convert_type(top_operador)

      operation_type = cubo_semantico.get_type(tipo_operando_izq, tipo_operando_der, converted_operador)
      if operation_type == 5:
        raise Exception("ERROR: Type Mismatch")
      else:
        temporal_variable = None
        quadruple = Quadruple(converted_operador, operando_izq, operando_der, temporal_variable)
        lista_de_cuadruplos.append(quadruple)
        stack_de_operandos.append(temporal_variable)
        stack_de_tipos.append(operation_type)
      
    else:
      stack_de_operadores.append(top_operador)

def p_push_op_relacionales(p):
  '''
  push_op_relacionales : GREATER
        | LESS 
        | GREATEREQ
        | LESSEQ
        | NOTEQUAL
        | EQUAL
        | empty
  '''
  p[0] = p[1]
  stack_de_operadores.append(p[0])

def p_exp(p):
  '''
  exp : term check_op_masmenos exp_aux
  '''

def p_exp_aux(p):
  '''
  exp_aux : push_op_exp_masmenos exp
          | empty
  '''

def p_push_op_exp_masmenos(p):
  '''
  push_op_exp_masmenos : PLUS 
        | MINUS 
        | empty
  '''
  p[0] = p[1]
  stack_de_operadores.append(p[0])

def p_check_op_masmenos(p):
  '''
  check_op_masmenos :
  '''
  global stack_de_operadores, stack_de_operandos, stack_de_tipos, lista_de_cuadruplos
  if len(stack_de_operadores) != 0:
    top_operador = stack_de_operadores.pop()
    if top_operador == '+' or top_operador == '-':
      operando_der = stack_de_operandos.pop()
      operando_izq = stack_de_operandos.pop()

      tipo_operando_der = stack_de_tipos.pop()
      tipo_operando_izq = stack_de_tipos.pop()

      converted_operador = convert_type(top_operador)
      operation_type = cubo_semantico.get_type(tipo_operando_izq, tipo_operando_der, converted_operador)
      if operation_type == 5:
        raise Exception("ERROR: Type Mismatch")
      else:
        temporal_variable = None
        quadruple = Quadruple(converted_operador, operando_izq, operando_der, temporal_variable)
        lista_de_cuadruplos.append(quadruple)
        stack_de_operandos.append(temporal_variable)
        stack_de_tipos.append(operation_type)
      
    else:
      stack_de_operadores.append(top_operador)

def p_term(p):
  '''
  term : factor check_op_pordiv term_aux
  '''
  p[0] = None

def p_term_aux(p):
  '''
  term_aux : push_op_exp_pordiv term 
        | empty
  '''

def p_check_op_pordiv(p):
  '''
  check_op_pordiv :
  '''
  global stack_de_operadores, stack_de_operandos, stack_de_tipos, lista_de_cuadruplos
  if len(stack_de_operadores) != 0:
    top_operador = stack_de_operadores.pop()
    if top_operador == '*' or top_operador == '/':
      operando_der = stack_de_operandos.pop()
      operando_izq = stack_de_operandos.pop()

      tipo_operando_der = stack_de_tipos.pop()
      tipo_operando_izq = stack_de_tipos.pop()

      converted_operador = convert_type(top_operador)
      operation_type = cubo_semantico.get_type(tipo_operando_izq, tipo_operando_der, converted_operador)
      if operation_type == 5:
        raise Exception("ERROR: Type Mismatch")
      else:
        temporal_variable = None
        quadruple = Quadruple(converted_operador, operando_izq, operando_der, temporal_variable)
        lista_de_cuadruplos.append(quadruple)
        stack_de_operandos.append(temporal_variable)
        stack_de_tipos.append(operation_type)

    else:
      stack_de_operadores.append(top_operador)

def p_push_op_exp_pordiv(p):
  '''
  push_op_exp_pordiv : TIMES 
        | DIVIDE 
        | empty
  '''
  p[0] = p[1]
  stack_de_operadores.append(p[0])

def p_factor(p):
  '''
  factor : factor_constante
          | factor_variable
          | factor_expresion
  '''
  p[0] = None 

def p_factor_constante(p) :
  '''
  factor_constante : CTEI push_int
                | CTEF push_float 
  '''

def p_factor_variable(p) : 
  '''
  factor_variable : ID push_id
                | ID LBRACKET hyper_exp RBRACKET
                | ID LBRACKET hyper_exp RBRACKET LBRACKET hyper_exp RBRACKET
                | ID llamada_func
  '''
  
def p_factor_expresion(p) : 
  '''
  factor_expresion : LPAREN meter_fondo_falso hyper_exp RPAREN quitar_fondo_falso
  '''

def p_meter_fondo_falso(p) : 
  '''
  meter_fondo_falso :
  '''
  stack_de_operadores.append('(')

def p_quitar_fondo_falso(p) : 
  '''
  quitar_fondo_falso :
  '''
  stack_de_operadores.pop()

def p_push_int(p) : 
  '''
  push_int :
  '''
  global stack_de_operandos, stack_de_tipos
  if p[-1] != None:
    stack_de_operandos.append(p[-1])
    stack_de_tipos.append(1)

def p_push_float(p) : 
  '''
  push_float :
  '''
  global stack_de_operandos, stack_de_tipos
  if p[-1] != None:
    stack_de_operandos.append(p[-1])
    stack_de_tipos.append(2)

def p_push_id(p) : 
  '''
  push_id :
  '''
  # Validate if id is within the set of variables of the current function
  if p[-1] not in dir_func.get_function_variables(current_func):
    raise Exception("ERRRO: La variable {p[-1]} no está declarada.")

  global stack_de_operandos, stack_de_tipos
  if p[-1] != None:
    stack_de_operandos.append(p[-1])
    id_type = dir_func.get_variable_type(current_func, p[-1])
    stack_de_tipos.append(id_type)

def p_llamada_func(p):
  '''
  llamada_func : ID LPAREN llamadaCYCLE RPAREN SEMICOLON
  llamadaCYCLE : hyper_exp llamadaCYCLE_aux
              | empty
  llamadaCYCLE_aux : COMMA hyper_exp llamadaCYCLE_aux
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
        

