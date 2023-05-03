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
stack_de_saltos = deque()
lista_de_cuadruplos = []
cubo_semantico = SemanticCube()
vControl = None

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

#Testing the lexer
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

#__________PARSER____________

# Definition of the grammars

# Start of the program
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

# Creates the symbol table with its default body and adds the function "programa" to the set of functions.
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
  inicio : INICIO LPAREN RPAREN LBRACE estatutos_aux RBRACE SEMICOLON
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

# Adds variables to the variable table of the corresponding function.
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
  dec_func : FUNCION dec_func_type ID punto_add_func LPAREN parameter RPAREN LBRACE dec_var_cycle estatutos_aux dec_func_regresar RBRACE SEMICOLON
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

# Adds function to the function's directory.
# Updates current_func pointer as we are accessing a new function.
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

# Adds parameter to the variable table of the current function.
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
          | imprimir
          | leer
  '''
  p[0] = None

def p_estatutos_aux(p):
	'''
	estatutos_aux : estatutos estatutos_aux
						    | empty
	'''

def p_asignar(p):
  '''
  asignar : variable ASSIGN push_op_igual hyper_exp check_op_igual SEMICOLON
  '''
  p[0] = None

# Push the "=" operator to the stack of operators.
def p_push_op_igual(p):
  '''
  push_op_igual :
  '''
  global stack_de_operadores
  stack_de_operadores.append(p[-1])

# Creates the quadruple for the assignation process.
def p_check_op_igual(p):
  '''
  check_op_igual :
  '''
  global stack_de_operadores, stack_de_operandos, stack_de_tipos, lista_de_cuadruplos
  top_operador = stack_de_operadores.pop()
  tipo_operando = stack_de_tipos.pop()
  operando = stack_de_operandos.pop()

  converted_operador = convert_type(top_operador)
  assign_variable_type = dir_func.get_variable_type(current_func, p[-4])

  operation_type = cubo_semantico.get_type(assign_variable_type, tipo_operando, converted_operador)
  # Raise exception if the operation between the two types is not valid.
  if operation_type == 5:
    raise Exception("ERROR: Type Mismatch")
  else:
    quadruple = Quadruple(converted_operador, operando, None , p[-4])
    lista_de_cuadruplos.append(quadruple.transform_quadruple())

def p_variable(p):
  '''
  variable : ID variable_aux
  variable_aux : LBRACKET exp RBRACKET
              | LBRACKET exp RBRACKET LBRACKET exp RBRACKET
              | empty
  '''
  p[0] = p[1]

def p_leer(p):
  '''
  leer : LEER variable SEMICOLON
  '''
  p[0] = None

def p_ciclo_while(p):
  '''
  ciclo_while : MIENTRAS punto_inicio_while LPAREN hyper_exp RPAREN punto_medio_while LBRACE estatutos_aux RBRACE punto_fin_while SEMICOLON
  '''
  p[0] = None

# Save the starting point of the comparison to come back and re-evaluate.
def p_punto_inicio_while(p):
  '''
  punto_inicio_while :
  '''
  global stack_de_saltos
  stack_de_saltos.append(len(lista_de_cuadruplos))

# Validate if the result of the expression is a boolean. If it's not raise an exception.
# It if is a boolean create a GOTOF quadruple with its 4th position empty, and add
# its position within the array to the stack of jumps.
def p_punto_medio_while(p):
  '''
  punto_medio_while :
  '''
  global stack_de_tipos, stack_de_saltos, lista_de_cuadruplos
  top_tipos = stack_de_tipos.pop()
  if(top_tipos != 4):
    raise Exception("ERROR: Type mismatch. Se espera una condición.")
  else:
    result = stack_de_operandos.pop()
    quadruple = Quadruple(75, result, None, None)
    lista_de_cuadruplos.append(quadruple.transform_quadruple())
    stack_de_saltos.append((len(lista_de_cuadruplos) - 1))

# Complete the missing GOTOF qudadruple, generate a GOTO quadruple with the return position as ts 4th position.
def p_punto_fin_while(p):
  '''
  punto_fin_while :
  '''
  global stack_de_saltos, lista_de_cuadruplos
  false = stack_de_saltos.pop()
  retorno = stack_de_saltos.pop()
  quadruple = Quadruple(80, None, None, retorno)
  lista_de_cuadruplos.append(quadruple.transform_quadruple())
  lista_de_cuadruplos = fill(false, len(lista_de_cuadruplos), lista_de_cuadruplos)

def p_ciclo_for(p):
  '''
  ciclo_for : PORCADA ID punto_existe_id ASSIGN hyper_exp punto_valida_int HASTA hyper_exp punto_valida_exp LBRACE estatutos_aux RBRACE punto_termina_for SEMICOLON
  '''
  p[0] = None

def p_punto_existe_id(p):
  '''
  punto_existe_id : 
  '''
   # Validate if the id exists either locally or globally
  if not dir_func.is_variable_declared(current_func, p[-1]):
    raise Exception(f"ERROR: La variable {p[-1]} no está declarada.")
  else:
    stack_de_operandos.append(p[-1])
  
def p_punto_valida_int(p):
  '''
  punto_valida_int : 
  '''
  #Validate if the hyper_exp is equal to an integer number
  global stack_de_operadores, stack_de_operandos, stack_de_tipos, lista_de_cuadruplos
  top_operador = stack_de_operadores.pop()
  tipo_exp = stack_de_tipos.pop()

  converted_operador = convert_type(top_operador)
  assign_variable_type = dir_func.get_variable_type(current_func, p[-4])

  if tipo_exp != 1 and assign_variable_type != 1:
    raise Exception(f"ERROR: Type Mismatch. El ID y su valor deben ser enteros") 
  else: 
    operando_exp = stack_de_operandos.pop()
    vControl = stack_de_operandos.pop()
    quadruple = Quadruple(converted_operador, operando_exp, None , vControl)
    lista_de_cuadruplos.append(quadruple.transform_quadruple())

def p_punto_valida_exp(p):
  '''
  punto_valida_exp : 
  '''
  global stack_de_operandos, stack_de_tipos, lista_de_cuadruplos
  tipo_exp = stack_de_tipos.pop()
  if tipo_exp != 1:
        raise Exception(f"ERROR: Type Mismatch. El valor de la expresion debe ser entera") 
  else: 
    operando_exp = stack_de_operandos.pop()
    vFinal = operando_exp
    quadruple = Quadruple(70,operando_exp,None,vFinal)
    lista_de_cuadruplos.append(quadruple.transform_quadruple())

    quadruple2 = Quadruple(35,vControl,vFinal,None) #Pendiente el resultado en lugar de None
    lista_de_cuadruplos.append(quadruple2.transform_quadruple())

    stack_de_saltos.append(len(lista_de_cuadruplos)-1)
    quadruple_goto = Quadruple(75,None,None,None) #El segundo none es el valor que esta en Quadruple2
    lista_de_cuadruplos.append(quadruple_goto.transform_quadruple())
    stack_de_saltos.append(len(lista_de_cuadruplos)-1)
  
def p_punto_termina_for(p):
  '''
  p_punto_termina_for : 
  '''
  global stack_de_operandos, stack_de_tipos, lista_de_cuadruplos

  quadruple = Quadruple(10,vControl,1,vControl) # El uno tiene que ir en la tabla como constante y el segundo vControl es dirección de mememoria
  lista_de_cuadruplos.append(quadruple.transform_quadruple())

  fin = stack_de_saltos.pop()
  retorno = stack_de_saltos.pop()
  quadruple2 = Quadruple(80,None,None,retorno)
  lista_de_cuadruplos.append(quadruple2.transform_quadruple())
  lista_de_cuadruplos = fill(fin, len(lista_de_cuadruplos), lista_de_cuadruplos)
  
def p_condicion(p):
  '''
  condicion : SI LPAREN hyper_exp RPAREN punto_si LBRACE estatutos_aux RBRACE punto_fin_si sinoCondicion SEMICOLON
  sinoCondicion : SINO punto_sino LBRACE estatutos_aux RBRACE
              | empty
  '''
  p[0] = None

# Validate if the result of the expression is a boolean. If it's not raise an exception.
# It if is a boolean create a GOTOF quadruple with its 4th position empty, and add
# its position within the array to the stack of jumps.
def p_punto_si(p):
  '''
  punto_si : 
  '''
  global stack_de_tipos, stack_de_saltos, lista_de_cuadruplos
  top_tipos = stack_de_tipos.pop()
  if(top_tipos != 4):
    raise Exception("ERROR: Type mismatch. Se espera una condición.")
  else:
    result = stack_de_operandos.pop()
    quadruple = Quadruple(75, result, None, None)
    lista_de_cuadruplos.append(quadruple.transform_quadruple())
    stack_de_saltos.append((len(lista_de_cuadruplos) - 1))

# Complete the missing GOTOF(if) or GOTO(if-else) quadruple.
def p_punto_fin_si(p):
  '''
  punto_fin_si :
  '''
  global stack_de_saltos, lista_de_cuadruplos
  end = stack_de_saltos.pop()
  lista_de_cuadruplos = fill(end, len(lista_de_cuadruplos), lista_de_cuadruplos)

# Complete the missing GOTOF qudadruple, generate a GOTO quadruple, and its position to the stack of jumps.
def p_punto_sino(p):
  '''
  punto_sino :
  '''
  global stack_de_saltos, lista_de_cuadruplos
  false = stack_de_saltos.pop()
  quadruple = Quadruple(80, None, None, None)
  lista_de_cuadruplos.append(quadruple.transform_quadruple())
  lista_de_cuadruplos = fill(false, len(lista_de_cuadruplos), lista_de_cuadruplos)

# Logic operators: and, or
def p_hyper_exp(p):
  '''
  hyper_exp : super_exp hyper_exp_aux
  '''
 
def p_hyper_exp_aux(p):
  '''
  hyper_exp_aux : push_op_logicos super_exp check_op_logicos
                | empty
  '''

# When there's a logical operator to be solved within the stack
# of operators, it creates a Quadruple for it.
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
      # Raise exception if the operation between the two types is not valid.
      if operation_type == 5:
        raise Exception("ERROR: Type Mismatch")
      else:
        temporal_variable = -1
        quadruple = Quadruple(converted_operador, operando_izq, operando_der, temporal_variable)
        lista_de_cuadruplos.append(quadruple.transform_quadruple())
        stack_de_operandos.append(temporal_variable)
        stack_de_tipos.append(operation_type)
      
    else:
      stack_de_operadores.append(top_operador)

# Push of logical operators to the stack of operators.
def p_push_op_logicos(p):
  '''
  push_op_logicos : Y 
        | O 
        | empty
  '''
  stack_de_operadores.append(p[1])

# Relational operators: <,>,>=,<=,!=,==
def p_super_exp(p):
  '''
  super_exp : exp super_exp_aux
  '''

def p_super_exp_aux(p):
  '''
  super_exp_aux : push_op_relacionales exp check_op_relacionales
                | empty
  '''

# When there's a relational operator to be solved within the stack
# of operators, it creates a Quadruple for it.
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
      # Raise exception if the operation between the two types is not valid.
      if operation_type == 5:
        raise Exception("ERROR: Type Mismatch")
      else:
        temporal_variable = None
        quadruple = Quadruple(converted_operador, operando_izq, operando_der, temporal_variable)
        lista_de_cuadruplos.append(quadruple.transform_quadruple())
        stack_de_operandos.append(temporal_variable)
        stack_de_tipos.append(operation_type)
      
    else:
      stack_de_operadores.append(top_operador)

# Push of relational operators to the stack of operators.
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
  stack_de_operadores.append(p[1])

# Start of the arithmetic operators
def p_exp(p):
  '''
  exp : term check_op_masmenos exp_aux
  '''

def p_exp_aux(p):
  '''
  exp_aux : push_op_exp_masmenos exp
          | empty
  '''

# Push of arithmetic operators: +, -
def p_push_op_exp_masmenos(p):
  '''
  push_op_exp_masmenos : PLUS 
        | MINUS 
        | empty
  '''
  stack_de_operadores.append(p[1])

# When there's a minus or plus operator to be solved within the stack
# of operators, it creates a Quadruple for it.
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
      # Raise exception if the operation between the two types is not valid.
      if operation_type == 5:
        raise Exception("ERROR: Type Mismatch")
      else:
        temporal_variable = None
        quadruple = Quadruple(converted_operador, operando_izq, operando_der, temporal_variable)
        lista_de_cuadruplos.append(quadruple.transform_quadruple())
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

# When there's a times or division operator to be solved within the stack
# of operators, it creates a Quadruple for it.
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
      # Raise exception if the operation between the two types is not valid.
      if operation_type == 5:
        raise Exception("ERROR: Type Mismatch")
      else:
        temporal_variable = None
        quadruple = Quadruple(converted_operador, operando_izq, operando_der, temporal_variable)
        lista_de_cuadruplos.append(quadruple.transform_quadruple())
        stack_de_operandos.append(temporal_variable)
        stack_de_tipos.append(operation_type)

    else:
      stack_de_operadores.append(top_operador)

# Push of arithmetic operators: *, /
def p_push_op_exp_pordiv(p):
  '''
  push_op_exp_pordiv : TIMES 
        | DIVIDE 
        | empty
  '''
  stack_de_operadores.append(p[1])

def p_factor(p):
  '''
  factor : factor_constante
          | factor_variable
          | factor_expresion
  '''
  p[0] = p[1] 

# Constant values
def p_factor_constante(p) :
  '''
  factor_constante : CTEI push_int
                | CTEF push_float 
  '''

# Normal IDs, arrays, matrix, or returned values of functions.
def p_factor_variable(p) : 
  '''
  factor_variable : ID push_id
                | ID LBRACKET hyper_exp RBRACKET
                | ID LBRACKET hyper_exp RBRACKET LBRACKET hyper_exp RBRACKET
                | ID llamada_func
  '''

# Arithmetic expressions within parenthesis.
def p_factor_expresion(p) : 
  '''
  factor_expresion : LPAREN meter_fondo_falso hyper_exp RPAREN quitar_fondo_falso
  '''

# Push of a parenthesis to simulate the false bottom
def p_meter_fondo_falso(p) : 
  '''
  meter_fondo_falso :
  '''
  stack_de_operadores.append('(')

# Removal of the false bottom
def p_quitar_fondo_falso(p) : 
  '''
  quitar_fondo_falso :
  '''
  stack_de_operadores.pop()

# Push of INT constants
def p_push_int(p) : 
  '''
  push_int :
  '''
  global stack_de_operandos, stack_de_tipos
  if p[-1] != None:
    stack_de_operandos.append(p[-1])
    stack_de_tipos.append(1)

# Push of FLOAT constants
def p_push_float(p) : 
  '''
  push_float :
  '''
  global stack_de_operandos, stack_de_tipos
  if p[-1] != None:
    stack_de_operandos.append(p[-1])
    stack_de_tipos.append(2)

# Push of IDs
def p_push_id(p) : 
  '''
  push_id :
  '''
  # Validate if the id exists either locally or globally
  if not dir_func.is_variable_declared(current_func, p[-1]):
    raise Exception(f"ERROR: La variable {p[-1]} no está declarada.")

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

def p_imprimir(p):
  '''
  imprimir : IMPRIMIR LPAREN imprimir_aux RPAREN SEMICOLON
  imprimir_aux : exp push_imprimir imprimirCycle
              | CTESTRING push_imprimir imprimirCycle
  imprimirCycle : COMMA imprimir_aux
              | empty
  '''
  p[0] = None

# It created a Quadruple for the print instruction. If there's something left within the
# stack of operands it will pop it out from the stack and to store it as the result of the quadruple.
# if not, it will only print the variable sent.
def p_push_imprimir(p):
  '''
  push_imprimir :
  '''
  global stack_de_operandos, stack_de_tipos
  converted_operador = convert_type('imprimir')
  if len(stack_de_operandos) != 0:
    top_operando = stack_de_operandos.pop()
    quadruple = Quadruple(converted_operador, None, None, top_operando)
    lista_de_cuadruplos.append(quadruple.transform_quadruple())
  else:
    quadruple = Quadruple(converted_operador, None, None, p[-1])
    lista_de_cuadruplos.append(quadruple.transform_quadruple())

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
        

