import ply.yacc as yacc
from collections import deque

from lexer_frima import tokens

from utils.symbol_table import *
from utils.semantic_cube import *
from utils.virtual_memory import *
from utils.quadruples import *
from utils.shared import *

# Create global variables
cubo_semantico = SemanticCube()

stack_de_operadores = deque()
stack_de_operandos = deque()
stack_de_tipos = deque()
stack_de_saltos = deque()

lista_de_cuadruplos = []
vControl = current_func = current_var_type = None

#__________PARSER____________

# Start of the program
start = 'programa'

# Definition of the grammars
def p_programa(p):
  '''
  programa : PROGRAMA ID punto_programa COLON inicio
          | PROGRAMA ID punto_programa COLON dec_var_cycle inicio
          | PROGRAMA ID punto_programa COLON dec_var_cycle dec_func_cycle inicio
          | PROGRAMA ID punto_programa COLON dec_func_cycle inicio
  '''
  p[0] = None

# Creates the symbol table with its default structure and adds the function "programa" to the set of functions.
def p_punto_programa(p):
  '''
  punto_programa : 
  '''
  global dir_func, current_func, lista_de_cuadruplos
  dir_func = SymbolTable() # Create symbol table
  current_func = "programa" # Sets global scope
  dir_func.symbol_table['dir_functions']['dir_func_names'].add("programa")

  quadruple = Quadruple(80, None, None , None) # Crete GOTO quadruple
  lista_de_cuadruplos.append(quadruple.transform_quadruple())

def p_inicio(p):
  '''
  inicio : INICIO LPAREN RPAREN LBRACE punto_update_goto estatutos RBRACE SEMICOLON
  '''
  p[0] = None
  print("TABLA DE VARIABLES", dir_func.symbol_table)
  for quadruple in lista_de_cuadruplos: 
    print(quadruple)

def p_punto_update_goto(p):
  '''
  punto_update_goto :
  '''
  global current_func, lista_de_cuadruplos
  current_func = 'programa'
  lista_de_cuadruplos[0]=(80,None,None,len(lista_de_cuadruplos))

# Allows multiple declaration of variables
def p_dec_var_cycle(p):
  '''
  dec_var_cycle : dec_var dec_var_cycle
                | empty
  '''

# Allows multiple declaration of functions
def p_dec_func_cycle(p):
  '''
  dec_func_cycle : dec_func dec_func_cycle
                | empty
  '''

# Types of variable declarations
def p_dec_var(p):
  '''
  dec_var : simple_var
          | array
          | matrix
  '''
  p[0] = p[1]

# Types of variables. It converts the type of the variable from a string to a number
# and saves it within current_var_type.
def p_type(p):
  '''
  type : ENTERO
      | DECIMAL
      | LETRA
  '''
  p[0] = p[1]
  global current_var_type

  current_var_type = convert_type(p[1])

# Declaration of simple variables
def p_simple_var(p):
  '''
  simple_var : VARIABLE type ARROW ID punto_simple_var simpleVarCycle SEMICOLON
  simpleVarCycle : COMMA ID punto_simple_var simpleVarCycle
                  | empty
  '''
  p[0] = None

# Adds variables to the variable table of the corresponding and current function.
def p_punto_simple_var(p):
  '''
  punto_simple_var :
  '''
  var_dir_address = assign_memory(current_var_type, current_func, False, False)
  dir_func.add_variable(current_var_type, p[-1], current_func, var_dir_address)

# Declaration of arrays
def p_array(p):
  '''
  array : RENGLON type ARROW ID LBRACKET CTEI RBRACKET punto_array arrayCycle SEMICOLON
  arrayCycle : COMMA ID LBRACKET CTEI RBRACKET punto_array arrayCycle
              | empty
  '''
  p[0] = None

# Adds arrays to the variable table of the corresponding and current function.
# It sends additional values such as its dimension and size. 
def p_punto_array(p):
  '''
  punto_array :
  '''
  dir_func.add_variable(current_var_type, p[-4], current_func, 1, p[-2])

# Declaration of matrix
def p_matrix(p):
  '''
  matrix : TABLA type ARROW ID LBRACKET CTEI RBRACKET LBRACKET CTEI RBRACKET punto_matrix matrixCycle SEMICOLON
  matrixCycle : COMMA ID LBRACKET CTEI RBRACKET LBRACKET CTEI RBRACKET punto_matrix matrixCycle
              | empty
  '''
  p[0] = None

# Adds matrix to the variable table of the corresponding and current function.
# It sends additional values such as its dimension and its size as a tuple. 
def p_punto_matrix(p):
  '''
  punto_matrix :
  '''
  dir_func.add_variable(current_var_type, p[-7], current_func, 2, (p[-5],p[-2]))

# Declares a function
def p_dec_func(p):
  '''
  dec_func : FUNCION type ID punto_add_func punto_global_func_var LPAREN parameter RPAREN LBRACE dec_var_cycle estatutos dec_func_regresar RBRACE SEMICOLON punto_end_function
            | FUNCION SINREGRESAR ID punto_add_func LPAREN parameter RPAREN LBRACE dec_var_cycle estatutos RBRACE SEMICOLON punto_end_function
  '''

def p_punto_global_func_var(p):
  '''
  punto_global_func_var : 
  '''
  global dir_func
  current_func_type = convert_type(p[-3])
  global_func_var_address = assign_memory(current_func_type, 'programa', False, False)
  dir_func.add_variable(current_func_type, p[-2], 'programa', global_func_var_address)

def p_dec_func_regresar(p):
  '''
  dec_func_regresar : REGRESAR exp SEMICOLON
                    | empty
  '''
  p[0] = p[1]

# Deletes the local variables of the function and its variable table.
# Sets back the scope to be global.
def p_punto_end_function(p):
  '''
  punto_end_function :
  '''
  global dir_func, current_func, lista_de_cuadruplos

  quadruple = Quadruple(85, None, None , None)
  lista_de_cuadruplos.append(quadruple.transform_quadruple())
  
  reset_dir_local()
  reset_local_temp()
  dir_func.delete_function_var_table(current_func)
  current_func = 'programa'

# Adds function and its return type to the global function's directory.
# Updates "current_func" pointer as we are accessing a new function.
def p_punto_add_func(p):
    '''
    punto_add_func :
    '''
    global current_func, lista_de_cuadruplos
    current_func = p[-1]
    dir_func.add_function(p[-1], convert_type(p[-2]), len(lista_de_cuadruplos))

# Declares function's parameters (if any)
def p_parameter(p):
  '''
  parameter : type ID punto_add_parameter parameterCycle
            | empty
  '''
  p[0] = None

# Allows multiple declaration of parameters
def p_parameterCycle(p):
  '''
  parameterCycle : COMMA type ID punto_add_parameter parameterCycle
                  | empty 
  '''
  p[0] = None

# Adds parameter (and its type) to the variable table of the current function.
def p_punto_add_parameter(p):
  '''
  punto_add_parameter :
  '''
  param_type = convert_type(p[-2])
  parameter_dir_address = assign_memory(param_type, current_func, False, False)
  dir_func.add_function_params(current_func, param_type, p[-1], parameter_dir_address)

# Allows multiple declaration of estatutos
def p_estatutos(p):
  '''
  estatutos : estatutos_opciones estatutos
            | empty
  '''

# List of the possible content on a function, conditional or cycle
def p_estatutos_opciones(p):
  '''
  estatutos_opciones : asignar
                      | llamada_func
                      | ciclo_for
                      | ciclo_while
                      | condicion
                      | imprimir
                      | leer
  '''
  p[0] = p[1]

def p_func_regresar(p):
  '''
  func_regresar : REGRESAR exp SEMICOLON
  '''
  p[0] = None

def p_asignar(p):
  '''
  asignar : variable ASSIGN push_op_igual hyper_exp check_op_igual SEMICOLON
  '''
  p[0] = None

def p_variable(p):
  '''
  variable : ID variable_aux
  '''
  p[0] = p[1]

# To assign a variable it can either be a simple var or an array and matrix position
def p_variable_aux(p):
  '''
  variable_aux : LBRACKET exp RBRACKET
              | LBRACKET exp RBRACKET LBRACKET exp RBRACKET
              | empty
  '''
  p[0] = p[1]

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
  global stack_de_operadores, stack_de_operandos, stack_de_tipos, lista_de_cuadruplos, dir_func
  top_operador = stack_de_operadores.pop()
  tipo_operando = stack_de_tipos.pop()
  operando = stack_de_operandos.pop()

  converted_operador = convert_type(top_operador)
  # Validate if the variable to assign exists either locally or globally
  if not dir_func.is_variable_declared(current_func, p[-4]):
    raise Exception(f"ERROR: La variable {p[-4]} no está declarada.")

  assign_variable_type = dir_func.get_variable_type(current_func, p[-4])

  operation_type = cubo_semantico.get_type(assign_variable_type, tipo_operando, converted_operador)
  # Raise exception if the assignation between the two types is not valid.
  if operation_type == 5:
    raise Exception("ERROR: Type mismatch en asignación")
  else:
    id_address = dir_func.get_variable_address(current_func, p[-4])
    quadruple = Quadruple(converted_operador, operando, None , id_address)
    lista_de_cuadruplos.append(quadruple.transform_quadruple())

def p_leer(p):
  '''
  leer : LEER variable SEMICOLON
  '''
  p[0] = None

def p_ciclo_while(p):
  '''
  ciclo_while : MIENTRAS punto_inicio_while LPAREN hyper_exp RPAREN punto_medio_while LBRACE estatutos RBRACE punto_fin_while SEMICOLON
  '''
  p[0] = None

# Save the starting point of the comparison to come back and re-evaluate.
def p_punto_inicio_while(p):
  '''
  punto_inicio_while :
  '''
  global stack_de_saltos, lista_de_cuadruplos
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
  ciclo_for : PORCADA ID punto_existe_id ASSIGN hyper_exp punto_valida_int HASTA hyper_exp punto_valida_exp LBRACE estatutos RBRACE punto_termina_for SEMICOLON
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
  punto_termina_for : 
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
  condicion : SI LPAREN hyper_exp RPAREN punto_si LBRACE estatutos RBRACE punto_fin_si SEMICOLON
            | SI LPAREN hyper_exp RPAREN punto_si LBRACE estatutos RBRACE SINO punto_sino LBRACE estatutos RBRACE punto_fin_si SEMICOLON
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
  stack_de_saltos.append(len(lista_de_cuadruplos)-1)
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
  global stack_de_operadores, stack_de_operandos, stack_de_tipos, lista_de_cuadruplos, dir_func
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
        # create direction for boolean temporal variable (either globally or locally)
        temporal_dir_address = assign_memory(4, current_func, False, True)
        dir_func.add_cont_temp(4, current_func)

        quadruple = Quadruple(converted_operador, operando_izq, operando_der, temporal_dir_address)
        lista_de_cuadruplos.append(quadruple.transform_quadruple())
        stack_de_operandos.append(temporal_dir_address)
        stack_de_tipos.append(operation_type)
      
    else: # push operator back to stack
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
        temporal_dir_address = assign_memory(4, current_func, False, True)
        dir_func.add_cont_temp(4, current_func)

        quadruple = Quadruple(converted_operador, operando_izq, operando_der, temporal_dir_address)
        lista_de_cuadruplos.append(quadruple.transform_quadruple())
        stack_de_operandos.append(temporal_dir_address)
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
        raise Exception("ERROR: Type mismatch en suma y resta")
      else:
        temporal_dir_address = assign_memory(operation_type, current_func, False, True)
        dir_func.add_cont_temp(operation_type, current_func)
        
        quadruple = Quadruple(converted_operador, operando_izq, operando_der, temporal_dir_address)
        lista_de_cuadruplos.append(quadruple.transform_quadruple())
        stack_de_operandos.append(temporal_dir_address)
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
        raise Exception("ERROR: Type mismatch multiplicacion y division")
      else:
        temporal_dir_address = assign_memory(operation_type, current_func, False, True)
        dir_func.add_cont_temp(operation_type, current_func)

        quadruple = Quadruple(converted_operador, operando_izq, operando_der, temporal_dir_address)
        lista_de_cuadruplos.append(quadruple.transform_quadruple())
        stack_de_operandos.append(temporal_dir_address)
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

# Creates the address memory of the int constant (if it doesn't have one yet) 
# and push it to the stack of operands.
def p_push_int(p) : 
  '''
  push_int :
  '''
  global stack_de_operandos, stack_de_tipos, dir_func
  if p[-1] != None:
    constant = p[-1]
    constant_address = dir_func.get_constant_address(constant)
    if(not constant_address):
      constant_address = assign_memory(1, current_func, True, False)
      dir_func.add_constant_variable(1, constant, constant_address)
    stack_de_operandos.append(constant_address)
    stack_de_tipos.append(1)

# Creates the address memory of the float constant (if it doesn't have one yet)
# and push it to the stack of operands.
def p_push_float(p) : 
  '''
  push_float :
  '''
  global stack_de_operandos, stack_de_tipos, dir_func
  if p[-1] != None:
    constant = p[-1]
    constant_address = dir_func.get_constant_address(constant)
    if(not constant_address):
      constant_address = assign_memory(2, current_func, True, False)
      dir_func.add_constant_variable(2, constant, constant_address)
    stack_de_operandos.append(constant_address)
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
    id_address = dir_func.get_variable_address(current_func, p[-1])
    stack_de_operandos.append(id_address)
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
# stack of operands that means it is either a variable, expression or an int/float. If not it means it's
# a constant string. For each it will create the corresponding Quadruple.
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
    constant = p[-1]
    constant_address = dir_func.get_constant_address(constant)
    if(not constant_address):
      constant_address = assign_memory(5, current_func, True, False)
      dir_func.add_constant_variable(5, constant, constant_address)
    quadruple = Quadruple(converted_operador, None, None, constant_address)
    lista_de_cuadruplos.append(quadruple.transform_quadruple())

def p_empty(p):
  '''
  empty : 
  '''
  pass

def p_error(p):
  raise Exception("ERROR: Hay un error de syntaxis en la linea %d" % (p.lineno))

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