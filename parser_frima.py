import ply.yacc as yacc
from collections import deque

from lexer_frima import tokens

from utils.symbol_table import *
from utils.semantic_cube import *
from utils.virtual_memory import *
from utils.quadruples import *
from utils.shared import *
from utils.virtual_machine import *

# Create global variables
cubo_semantico = SemanticCube()

stack_de_operadores = deque()
stack_de_operandos = deque()
stack_de_tipos = deque()
stack_de_saltos = deque()
stack_de_dimensiones = deque()
vControl = deque()

lista_de_cuadruplos = []
dimensiones = []
input_array = []
output_array = []

current_func = current_var_type = called_func = current_var = errorMessage = None

contador_params = 0
current_size = 1
error = False

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

# Creates the symbol table with its default structure and adds the function "inicio" to the set of functions.
def p_punto_programa(p):
  '''punto_programa : '''

  global dir_func, current_func, lista_de_cuadruplos

  dir_func = SymbolTable() # Create symbol table
  current_func = "inicio" # Sets global scope
  dir_func.symbol_table['dir_functions']['dir_func_names'].add("inicio")

  quadruple = Quadruple(80, None, None , None) # Crete GOTO quadruple
  lista_de_cuadruplos.append(quadruple.transform_quadruple())

def p_inicio(p):
  '''
  inicio : INICIO LPAREN RPAREN LBRACE punto_update_goto inicio_estatutos RBRACE SEMICOLON punto_generar_vm
  '''

  # Segment for testing dir_func and quadruples
  # print("TABLA DE VARIABLES", dir_func.symbol_table)
  for index, quadruple in enumerate(lista_de_cuadruplos): 
    print(index, " -> ", quadruple)

def p_punto_generar_vm(p):
  '''punto_generar_vm :'''

  global lista_de_cuadruplos, dir_func, output_array

  virtual_machine = VirtualMachine(lista_de_cuadruplos, dir_func.symbol_table)

  if len(input_array) != 0:
    virtual_machine.input_array = input_array

  virtual_machine.execute()
  output_array = virtual_machine.output_array
  
  dir_func.delete_symbol_table()

# Body for inicio (without the return option)
def p_inicio_estatutos(p):
  '''
  inicio_estatutos : estatutos_opciones inicio_estatutos
                    | empty
  '''
  p[0] = p[1]

def p_punto_update_goto(p):
  '''punto_update_goto :'''

  global current_func, lista_de_cuadruplos
  current_func = 'inicio'
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
  dec_func_cycle : dec_func p_dec_func_aux
  '''

def p_dec_func_aux(p):
  '''
  p_dec_func_aux : dec_func p_dec_func_aux
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

# Adds variables to the variable table of the corresponding and current function.
def p_punto_simple_var(p):
  '''punto_simple_var :'''

  var_dir_address = assign_memory_global_local(current_var_type, current_func, 1)
  dir_func.add_variable(current_var_type, p[-1], current_func, var_dir_address, [1], 0)

# Declaration of arrays
def p_array(p):
  '''
  array : RENGLON type ARROW ID LBRACKET CTEI punto_array_size RBRACKET punto_save_array arrayCycle SEMICOLON
  arrayCycle : COMMA ID LBRACKET CTEI punto_array_size RBRACKET punto_save_array arrayCycle
              | empty
  '''

def p_punto_array_size(p):
  '''punto_array_size :'''

  global dimensiones
  if p[-1] < 1:
    raise Exception(f"ERROR: Estás creando un conjunto de datos con un tamaño de {p[-1]}. Deben siempre tener un tamaño mayor que 1.")

# Adds array to the variable table of the current function.
# It sends additional values such as its dimension and size. 
def p_punto_save_array(p):
  '''punto_save_array :'''

  # Add size of array to constant table to only work with addresses
  var_dir_address = assign_memory_global_local(current_var_type, current_func, p[-3])
  dir_func.add_variable(current_var_type, p[-5], current_func, var_dir_address, [p[-3]], 1)
  constant_address = dir_func.get_constant_address(p[-3])
  if(not constant_address):
    constant_address = assign_memory_constant(1)
    dir_func.add_constant_variable(1, p[-3], constant_address)

  constant_address = dir_func.get_constant_address(0)
  if(not constant_address):
    constant_address = assign_memory_constant(1)
    dir_func.add_constant_variable(1, 0, constant_address)

# Declaration of matrix
def p_matrix(p):
  '''
  matrix : TABLA type ARROW ID LBRACKET CTEI punto_matrix_size RBRACKET LBRACKET CTEI punto_matrix_size RBRACKET punto_save_matrix matrixCycle SEMICOLON
  matrixCycle : COMMA ID LBRACKET CTEI punto_matrix_size RBRACKET LBRACKET CTEI punto_matrix_size RBRACKET punto_save_matrix matrixCycle
              | empty
  '''

def p_punto_matrix_size(p):
  '''punto_matrix_size :'''

  global current_size, isArray, dimensiones

  if p[-1] < 1:
    raise Exception(f"ERROR: Estás creando un conjunto de datos con un tamaño de {p[-1]}. Deben siempre tener un tamaño mayor que 1.")
  current_size *= p[-1]
  dimensiones.append(p[-1])

# Adds matrix to the variable table of the corresponding and current function.
# It sends additional values such as its dimension and its size as a tuple. 
def p_punto_save_matrix(p):
  '''punto_save_matrix : '''

  global dimensiones, current_size
  var_dir_address = assign_memory_global_local(current_var_type, current_func, current_size)
  dir_func.add_variable(current_var_type, p[-9], current_func, var_dir_address, dimensiones, 2)

  if(not dir_func.get_constant_address(dimensiones[0])):
    constant_address = assign_memory_constant(1)
    dir_func.add_constant_variable(1, dimensiones[0], constant_address)
  
  if(not dir_func.get_constant_address(dimensiones[1])):
    constant_address = assign_memory_constant(1)
    dir_func.add_constant_variable(1, dimensiones[1], constant_address)

  constant_address = dir_func.get_constant_address(0)
  if(not constant_address):
    constant_address = assign_memory_constant(1)
    dir_func.add_constant_variable(1, 0, constant_address)
  
  dimensiones = [] # Empty list of dimensions for new matrix
  current_size = 1

# Declares a function
def p_dec_func(p):
  '''
  dec_func : FUNCION type ID punto_add_func punto_global_func_var LPAREN parameter RPAREN LBRACE dec_var_cycle estatutos RBRACE SEMICOLON punto_end_function
            | FUNCION SINREGRESAR ID punto_add_func LPAREN parameter RPAREN LBRACE dec_var_cycle estatutos RBRACE SEMICOLON punto_end_function
  '''

# Creates global var with the same name as the declared function
def p_punto_global_func_var(p):
  '''punto_global_func_var : '''

  current_func_type = convert_type(p[-3])
  global_func_var_address = assign_memory_global_local(current_func_type, 'inicio', 1)
  dir_func.add_variable(current_func_type, p[-2], 'inicio', global_func_var_address, [1], 0)

# Deletes the local variables of the function and its variable table.
# Sets back the scope to be global.
def p_punto_end_function(p):
  '''punto_end_function :'''

  global dir_func, current_func, lista_de_cuadruplos

  quadruple = Quadruple(85, None, None , None)
  lista_de_cuadruplos.append(quadruple.transform_quadruple())
  
  reset_dir_local()
  reset_local_temp()
  dir_func.delete_function_var_table(current_func)
  current_func = 'inicio'

# Adds function and its return type to the global function's directory.
# Updates "current_func" pointer as we are accessing a new function.
def p_punto_add_func(p):
  '''punto_add_func :'''
  
  global current_func, lista_de_cuadruplos
  current_func = p[-1]
  dir_func.add_function(p[-1], convert_type(p[-2]), len(lista_de_cuadruplos))

# Declares function's parameters (if any)
def p_parameter(p):
  '''
  parameter : type ID punto_add_parameter parameterCycle
            | empty
  '''

# Allows multiple declaration of parameters
def p_parameterCycle(p):
  '''
  parameterCycle : COMMA type ID punto_add_parameter parameterCycle
                  | empty 
  '''

# Adds parameter (and its type) to the variable table of the current function.
def p_punto_add_parameter(p):
  '''punto_add_parameter :'''

  param_type = convert_type(p[-2])
  parameter_dir_address = assign_memory_global_local(param_type, current_func, 1)
  dir_func.add_function_params(current_func, param_type, p[-1], parameter_dir_address)

# Body for functions
def p_estatutos(p):
  '''
  estatutos : estatutosCycle
            | func_regresar
  '''

# Allows multiple declaration of estatutos
def p_estatutosCycle(p):
	'''
	estatutosCycle : estatutos_opciones estatutos
                | estatutos_opciones
                | empty
	'''

# List of the possible content on a function, conditional or cycle
def p_estatutos_opciones(p):
  '''
  estatutos_opciones : asignar
                      | llamada_func_void
                      | ciclo_for
                      | ciclo_while
                      | condicion
                      | imprimir
                      | leer
  '''
  p[0] = p[1]

def p_func_regresar(p):
  '''
  func_regresar : REGRESAR LPAREN exp RPAREN SEMICOLON punto_check_types
  '''

# Validates that the type of return is the same as the type that was used when function was declared,
# If types match it created the RETURN quadruple.
def p_punto_check_types(p):
  '''punto_check_types :'''

  global stack_de_tipos, stack_de_operandos, lista_de_cuadruplos

  func_return_type = dir_func.symbol_table['dir_functions'][current_func]['return_type']
  if(func_return_type == 0):
    raise Exception(f"ERROR: La función {current_func} es de tipo sinregresar.")
  exp_type = stack_de_tipos.pop()
  if (exp_type != func_return_type):
    raise Exception(f"ERROR: El valor regresado no coincide con el tipo de la función {current_func}.")
  else:
    result = stack_de_operandos.pop()
    quadruple = Quadruple(110, None, None, result)
    lista_de_cuadruplos.append(quadruple.transform_quadruple())
    
def p_asignar(p):
  '''
  asignar : variable ASSIGN hyper_exp push_op_igual check_op_igual SEMICOLON
  '''

# Invokes a variable that can be either a simple variable, an array or a matrix.
def p_variable(p):
  '''
  variable : ID push_id variable_aux
  variable_aux : LBRACKET punto_dimensioned meter_fondo_falso hyper_exp punto_create_ver_quad punto_termina_arr RBRACKET quitar_fondo_falso variable_aux_dim
                | empty
  variable_aux_dim : LBRACKET meter_fondo_falso hyper_exp punto_create_lastDim_cuadruplo RBRACKET quitar_fondo_falso generate_address_quadruple
                | empty
  '''
  p[0] = p[1]

# Gets the information about the dimensioned variable and push it into the stack of dimensions.
# Pops out the ID from the stack of operands since it won't be needed.
def p_punto_dimensioned(p):
  '''punto_dimensioned :'''

  global stack_de_operandos, stack_de_dimensiones

  var_info = dir_func.get_variable_var_dimInfo(current_func, p[-3])
  stack_de_operandos.pop()
  stack_de_dimensiones.append((var_info[1], var_info[0])) # (baseAddress, [size1, size2]) or  (baseAddress, [size1])
  # agregar a la tabla de contsntes la dir base const address = dirbase

# Only if it's an array (the size of the top element of the stack of operands is equal to 1) then
# remove the array info from the stack of dimensions and grab from it the baseAddress.
# Generates the (DIM, exp, baseAddress, (tn)) quadruple. We use DIM as a new operator
# to distinguish we need to add a baseAddress(pointer) to a regular value (exp).
def p_punto_termina_arr(p):
  '''punto_termina_arr :'''

  global stack_de_operandos, stack_de_dimensiones, stack_de_tipos, lista_de_cuadruplos
 
  if len(stack_de_dimensiones[-1][1]) == 1:
    top_dim = stack_de_dimensiones.pop()
    top_operando = stack_de_operandos.pop()
    stack_de_tipos.pop()

    dirBase = top_dim[0] # Grab baseAddress
    # Grab type from the baseAddress (type of the dimensioned variable)
    dirBase_type = dir_func.get_variable_type(current_func, current_var)
    dim_pointer = get_dim_pointer() # Grab next pointer available

    quadruple = Quadruple(125, top_operando, dirBase, dim_pointer)
    lista_de_cuadruplos.append(quadruple.transform_quadruple())
    stack_de_operandos.append(dim_pointer)
    stack_de_tipos.append(dirBase_type)

# Push the "=" operator to the stack of operators.
def p_push_op_igual(p):
  '''push_op_igual :'''

  global stack_de_operadores
  stack_de_operadores.append(p[-2])

# Creates the quadruple for the assignation process.
def p_check_op_igual(p):
  '''check_op_igual :'''

  global stack_de_operadores, stack_de_operandos, stack_de_tipos, lista_de_cuadruplos, dir_func
  
  top_operador = stack_de_operadores.pop()

  operando_der = stack_de_operandos.pop()
  operando_izq = stack_de_operandos.pop()

  tipo_operando_der = stack_de_tipos.pop()
  tipo_operando_izq = stack_de_tipos.pop()

  converted_operador = convert_type(top_operador)

  # Validate if the variable to assign exists either locally or globally
  if not dir_func.is_variable_declared(current_func, p[-4]):
    raise Exception(f"ERROR: La variable {p[-4]} no está declarada.")

  operation_type = cubo_semantico.get_type(tipo_operando_izq, tipo_operando_der, converted_operador)
  # Raise exception if the assignation between the two types is not valid.
  if operation_type == 5:
    raise Exception("ERROR: Type mismatch en asignación")
  else:
    quadruple = Quadruple(converted_operador, operando_der, None , operando_izq)
    lista_de_cuadruplos.append(quadruple.transform_quadruple())

def p_leer(p):
  '''
  leer : LEER LPAREN punto_push_leer ID punto_create_leer RPAREN SEMICOLON
  '''

def p_punto_push_leer(p):
  '''punto_push_leer :''' 
  
  global stack_de_operadores

  converted_operador = convert_type(p[-2])
  stack_de_operadores.append(converted_operador)

def p_punto_create_leer(p):
  '''punto_create_leer :'''

  global stack_de_operadores, stack_de_tipos

  if(p[-1] != None):
    if not dir_func.is_variable_declared(current_func, p[-1]):
      raise Exception(f"ERROR: La variable {p[-1]} no está declarada.")

    id_address = dir_func.get_variable_address(current_func, p[-1])
    id_type = dir_func.get_variable_type(current_func, p[-1])

    converted_operador = stack_de_operadores.pop()
    quadruple = Quadruple(converted_operador, None, id_type, id_address)
    lista_de_cuadruplos.append(quadruple.transform_quadruple())

def p_ciclo_while(p):
  '''
  ciclo_while : MIENTRAS punto_inicio_while LPAREN hyper_exp RPAREN punto_medio_while LBRACE estatutos RBRACE punto_fin_while SEMICOLON
  '''

# Save the starting point of the comparison to come back and re-evaluate.
def p_punto_inicio_while(p):
  '''punto_inicio_while :'''

  global stack_de_saltos, lista_de_cuadruplos
  stack_de_saltos.append(len(lista_de_cuadruplos))

# Validate if the result of the expression is a boolean. If it's not raise an exception.
# It if is a boolean create a GOTOF quadruple with its 4th position empty, and add
# its position within the array to the stack of jumps.
def p_punto_medio_while(p):
  '''punto_medio_while :'''

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
  '''punto_fin_while :'''

  global stack_de_saltos, lista_de_cuadruplos

  false = stack_de_saltos.pop()
  retorno = stack_de_saltos.pop()
  quadruple = Quadruple(80, None, None, retorno)
  lista_de_cuadruplos.append(quadruple.transform_quadruple())
  lista_de_cuadruplos = fill(false, len(lista_de_cuadruplos), lista_de_cuadruplos)

def p_ciclo_for(p):
  '''
  ciclo_for : DESDE LPAREN ID punto_existe_id ASSIGN hyper_exp RPAREN punto_valida_int HASTA LPAREN hyper_exp RPAREN punto_valida_exp LBRACE estatutos RBRACE punto_termina_for SEMICOLON
  '''

# Validate if the id exists either locally or globally.
# If it does add its virtual address to the stack of operands.
def p_punto_existe_id(p):
  '''punto_existe_id : '''

  global stack_de_operandos, stack_de_tipos

  if not dir_func.is_variable_declared(current_func, p[-1]):
    raise Exception(f"ERROR: La variable {p[-1]} no está declarada.")
  else:
    id_address = dir_func.get_variable_address(current_func, p[-1])
    id_type = dir_func.get_variable_type(current_func, p[-1])
    stack_de_operandos.append(id_address)
    stack_de_tipos.append(id_type)

def p_punto_valida_int(p):
  '''punto_valida_int : '''

  #Validate if the hyper_exp is equal to an integer number
  global stack_de_operadores, stack_de_operandos, stack_de_tipos, lista_de_cuadruplos, vControl

  result_type = stack_de_tipos.pop()
  id_type = stack_de_tipos.pop()

  if result_type != 1 and id_type != 1:
    raise Exception(f"ERROR: Type mismatch. El ID y su valor deben ser enteros") 
  else: 
    result_operando = stack_de_operandos.pop()
    vControl.append(stack_de_operandos.pop())
    quadruple = Quadruple(70, result_operando, None , vControl[-1])
    lista_de_cuadruplos.append(quadruple.transform_quadruple())

def p_punto_valida_exp(p):
  '''punto_valida_exp : '''

  global stack_de_operandos, stack_de_tipos, lista_de_cuadruplos, vControl

  tipo_exp = stack_de_tipos.pop()
  if tipo_exp != 1:
    raise Exception(f"ERROR: Type Mismatch. El valor de la expresion debe ser entera") 
  else: 
    operando_exp = stack_de_operandos.pop()
    vFinal = assign_memory_temporal(1, current_func)
    quadruple = Quadruple(70,operando_exp,None,vFinal)
    lista_de_cuadruplos.append(quadruple.transform_quadruple())

    temporal_dir_address = assign_memory_temporal(4, current_func)
    quadruple2 = Quadruple(35,vControl[-1],vFinal,temporal_dir_address)
    lista_de_cuadruplos.append(quadruple2.transform_quadruple())
    stack_de_saltos.append(len(lista_de_cuadruplos)-1)

    quadruple_goto = Quadruple(75,temporal_dir_address,None,None) #El segundo none es el valor que esta en Quadruple2
    lista_de_cuadruplos.append(quadruple_goto.transform_quadruple())
    stack_de_saltos.append(len(lista_de_cuadruplos)-1)
  
def p_punto_termina_for(p):
  '''punto_termina_for : '''

  global dir_func, stack_de_operandos, stack_de_tipos, lista_de_cuadruplos

  constant_address = dir_func.get_constant_address(1)
  if(not constant_address):
    constant_address = assign_memory_constant(1)
    dir_func.add_constant_variable(1, 1, constant_address)

  temporal_dir_address = assign_memory_temporal(1, current_func)
  quadruple = Quadruple(10,vControl[-1],constant_address,temporal_dir_address) # El uno tiene que ir en la tabla como constante y el segundo vControl es dirección de mememoria
  lista_de_cuadruplos.append(quadruple.transform_quadruple())

  quadruple = Quadruple(70,temporal_dir_address,None,vControl[-1])
  lista_de_cuadruplos.append(quadruple.transform_quadruple())
  vControl.pop()
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

# Validate if the result of the expression is a boolean. If it's not raise an exception.
# It if is a boolean create a GOTOF quadruple with its 4th position empty, and add
# its position within the array to the stack of jumps.
def p_punto_si(p):
  '''punto_si : '''

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
  '''punto_fin_si :'''

  global stack_de_saltos, lista_de_cuadruplos

  end = stack_de_saltos.pop()
  lista_de_cuadruplos = fill(end, len(lista_de_cuadruplos), lista_de_cuadruplos)

# Complete the missing GOTOF qudadruple, generate a GOTO quadruple, and its position to the stack of jumps.
def p_punto_sino(p):
  '''punto_sino :'''

  global stack_de_saltos, lista_de_cuadruplos

  false = stack_de_saltos.pop()
  quadruple = Quadruple(80, None, None, None)
  lista_de_cuadruplos.append(quadruple.transform_quadruple())
  stack_de_saltos.append(len(lista_de_cuadruplos)-1)
  lista_de_cuadruplos = fill(false, len(lista_de_cuadruplos), lista_de_cuadruplos)

# Highest level of operations. It starts withe the logic operators: and, or
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
  '''check_op_logicos :'''

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
        temporal_dir_address = assign_memory_temporal(4, current_func)
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
  '''check_op_relacionales :'''

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
        temporal_dir_address = assign_memory_temporal(4, current_func)
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
  '''
  stack_de_operadores.append(p[1])

# When there's a minus or plus operator to be solved within the stack
# of operators, it creates a Quadruple for it.
def p_check_op_masmenos(p):
  '''check_op_masmenos :'''

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
        raise Exception("ERROR: Type mismatch en suma o resta")
      else:
        temporal_dir_address = assign_memory_temporal(operation_type, current_func)
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

def p_term_aux(p):
  '''
  term_aux : push_op_exp_pordiv term 
        | empty
  '''

# When there's a times or division operator to be solved within the stack
# of operators, it creates a Quadruple for it.
def p_check_op_pordiv(p):
  '''check_op_pordiv :'''

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
        raise Exception("ERROR: Type mismatch multiplicacion o division")
      else:
        temporal_dir_address = assign_memory_temporal(operation_type, current_func)
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
  '''
  stack_de_operadores.append(p[1])

# Normal IDs, arrays, matrix, or returned values of functions.
def p_factor(p) : 
  '''
  factor : LPAREN meter_fondo_falso hyper_exp RPAREN quitar_fondo_falso
          | factor_constante
          | llamada_func_return
          | variable
  '''
  p[0] = p[1]

# This part only happens if we are on a matrix.
# Generates the (DIM, exp, baseAddress, (tn)) quadruple. We use DIM as a new operator
# to distinguish we need to add a baseAddress(pointer) to a regular value (exp).
# Appends the type of the baseAddress to be able to assign either decimals or integers.
def p_generate_address_quadruple(p):
  '''generate_address_quadruple :'''

  global stack_de_tipos, stack_de_operandos, stack_de_dimensiones, lista_de_cuadruplos

  top_operando = stack_de_operandos.pop()
  top_dim = stack_de_dimensiones.pop()
  dirBase = top_dim[0]

  dirBase_type = dir_func.get_variable_type(current_func, current_var)
  dim_pointer = get_dim_pointer()

  stack_de_tipos.pop() # s1m1+s2
  quadruple = Quadruple(125, top_operando, dirBase, dim_pointer)
  lista_de_cuadruplos.append(quadruple.transform_quadruple())
  stack_de_operandos.append(dim_pointer)

# Validates if the evaluated expression for indexing a dimensioned variable is of type int.
# It generates the quadruple to validate if the value of the expression is between the bounds.
# If it's a matrix, it generates the (*, exp, column, tn) -> (S1*m1) quadruple.
def p_punto_create_ver_quad(p):
  '''punto_create_ver_quad :'''

  global stack_de_tipos, stack_de_operandos, stack_de_dimensiones, lista_de_cuadruplos
  
  tipo_operando_exp = stack_de_tipos.pop()
  if tipo_operando_exp != 1:
    raise Exception(f"ERROR: El índice de acceso para {p[-6]} deber ser entero.")
  
  var_dimension = dir_func.get_variable_dimension(current_func, p[-6])
  constant_address_inf = dir_func.get_constant_address(0)
  constant_address_sup = dir_func.get_constant_address(stack_de_dimensiones[-1][1][0])
  
  quadruple = Quadruple(120, stack_de_operandos[-1], constant_address_inf, constant_address_sup)
  lista_de_cuadruplos.append(quadruple.transform_quadruple())
 
  if var_dimension == 2:
    result_exp = stack_de_operandos.pop()
  
    temp_var = assign_memory_temporal(1, current_func)
    constant_address_columns = dir_func.get_constant_address(stack_de_dimensiones[-1][1][1])
    quadruple = Quadruple(20, result_exp, constant_address_columns, temp_var)
   
    stack_de_operandos.append(temp_var) 
    stack_de_tipos.append(1)
    lista_de_cuadruplos.append(quadruple.transform_quadruple())

# This part only happens if we are on a matrix.
# It Validates if the evaluated expression for indexing a dimensioned variable is of type int.
# It generates the quadruple to validate if the value of the expression is between the bounds.
# It then generates the (+, S1*M1, S2, tn) quadruple.
def p_punto_create_lastDim_cuadruplo(p):
  '''punto_create_lastDim_cuadruplo :'''

  global stack_de_tipos, stack_de_operandos, stack_de_dimensiones, lista_de_cuadruplos

  if stack_de_tipos[-1] != 1:
    raise Exception(f"ERROR: El índice de acceso para {current_var} deber ser entero.")

  constant_address_inf = dir_func.get_constant_address(0)
  constant_address_sup = dir_func.get_constant_address(stack_de_dimensiones[-1][1][1])

  #operando_exp = stack_de_operandos.pop()
  quadruple = Quadruple(120, stack_de_operandos[-1], constant_address_inf, constant_address_sup)
  lista_de_cuadruplos.append(quadruple.transform_quadruple())
  
  res_exp = stack_de_operandos.pop()
  sm = stack_de_operandos.pop()
  stack_de_tipos.pop() #res_exp_type
  stack_de_tipos.pop() #sm_type
  
  temp_var = assign_memory_temporal(1, current_func)

  quadruple = Quadruple(10, sm, res_exp, temp_var)
  lista_de_cuadruplos.append(quadruple.transform_quadruple())
  stack_de_tipos.append(1)
  stack_de_operandos.append(temp_var)

# Constant values
def p_factor_constante(p) :
  '''
  factor_constante : CTEI push_int
                | CTEF push_float
  '''
  p[0] = p[1]

# Push a parenthesis into the stack of operators to simulate the false bottom
def p_meter_fondo_falso(p) : 
  '''meter_fondo_falso :'''

  global stack_de_operadores
  stack_de_operadores.append('(')

# Removes the parenthesis from the stack of operators to simulate the end of the false bottom
def p_quitar_fondo_falso(p) : 
  '''quitar_fondo_falso :'''

  global stack_de_operadores
  stack_de_operadores.pop()

# Creates the address memory of the int constant (if it doesn't have one yet) 
# and push it to the stack of operands.
def p_push_int(p) : 
  '''push_int :'''

  global stack_de_operandos, stack_de_tipos, dir_func

  if p[-1] != None:
    constant = p[-1]
    constant_address = dir_func.get_constant_address(constant)
    if(not constant_address):
      constant_address = assign_memory_constant(1)
      dir_func.add_constant_variable(1, constant, constant_address)
    stack_de_operandos.append(constant_address)
    stack_de_tipos.append(1)

# Creates the address memory of the float constant (if it doesn't have one yet)
# and push it to the stack of operands.
def p_push_float(p) : 
  '''push_float :'''

  global stack_de_operandos, stack_de_tipos, dir_func

  if p[-1] != None:
    constant = p[-1]
    constant_address = dir_func.get_constant_address(constant)
    if(not constant_address):
      constant_address = assign_memory_constant(2)
      dir_func.add_constant_variable(2, constant, constant_address)
    stack_de_operandos.append(constant_address)
    stack_de_tipos.append(2)

# Push ID's address into stack of operands and its stype into the stack of types
# Save the ID's name in a global variable named "current_var" for future references.
def p_push_id(p) : 
  '''push_id :'''

  global stack_de_operandos, stack_de_tipos, current_var

  # Validate if the ID exists either locally or globally
  if not dir_func.is_variable_declared(current_func, p[-1]):
    raise Exception(f"ERROR: La variable {p[-1]} no está declarada.")

  current_var = p[-1]
  if p[-1] != None:
    id_address = dir_func.get_variable_address(current_func, p[-1])
    stack_de_operandos.append(id_address)
    id_type = dir_func.get_variable_type(current_func, p[-1])
    stack_de_tipos.append(id_type)

# Allows multiple declaration of parameters
def p_func_params_aux(p):
  '''
  func_params_aux : COMMA exp punto_check_param func_params_aux
                  | empty
  '''

# Allows one, none, or multiple declaration of parameters
def p_func_params(p):
  '''
  func_params : exp punto_check_param func_params_aux
              | empty
  '''

# Validates type of param with function's signature, and
# updates the param's global counter.
def p_punto_check_param(p):
  ''' punto_check_param :'''

  global contador_params, stack_de_tipos, stack_de_operandos, lista_de_cuadruplos, called_func

  function_param_signature = dir_func.get_param_types(called_func)
  try:
    param_type = function_param_signature[contador_params]
  except:
    raise Exception(f"ERROR: Se excedió el número de parámetros declarados en la función {called_func}.")

  type_exp = stack_de_tipos.pop()

  if type_exp == param_type:
    operand_exp = stack_de_operandos.pop()
    quadruple = Quadruple(105, operand_exp, None, contador_params)
    lista_de_cuadruplos.append(quadruple.transform_quadruple())
    contador_params+=1
  else:
    raise Exception(f"ERROR: El tipo de los parámetros enviados no coinciden con la función {called_func}.")

# Does not return a value
def p_llamada_func_void(p):
  '''
  llamada_func_void : ID LPAREN punto_func_exists punto_validate_isvoid punto_create_era func_params RPAREN punto_check_total_params punto_create_gosub SEMICOLON
  '''

# Return a value used in expressions
def p_llamada_func_return(p):
  '''
  llamada_func_return : ID LPAREN punto_func_exists punto_validate_isNotvoid meter_fondo_falso punto_create_era func_params RPAREN punto_check_total_params quitar_fondo_falso punto_create_gosub
  '''

# Validates called function exists and updates name of called_func to keep track
def p_punto_func_exists(p):
  '''punto_func_exists :'''

  global dir_func, called_func
  if not dir_func.is_function_declared(p[-2]):
    raise Exception(f"ERROR: La función {p[-2]} no está definida.")

  called_func = p[-2]

def p_punto_validate_isNotvoid(p):
  '''punto_validate_isNotvoid :'''

  func_return_type = dir_func.symbol_table['dir_functions'][called_func]['return_type']
  if (func_return_type == 0):
    raise Exception(f"ERROR: La función {called_func} es de tipo sinregresar.")

# Validate if function is void
def p_punto_validate_isvoid(p):
  '''punto_validate_isvoid :'''

  func_return_type = dir_func.symbol_table['dir_functions'][called_func]['return_type']
  if (func_return_type != 0):
    raise Exception(f"ERROR: La función {called_func} debe ser de tipo sinregresar.")

# Creates ERA quadruple and only if function is not void it stores in stack of operands its global variable
def p_punto_create_era(p):
  '''punto_create_era : ''' 

  global lista_de_cuadruplos, stack_de_operandos, stack_de_tipos

  func_quadruple_pos = dir_func.get_func_quadruple_init(called_func)
  quadruple = Quadruple(100, called_func, None, func_quadruple_pos)
  lista_de_cuadruplos.append(quadruple.transform_quadruple())

def p_punto_check_total_params(p):
  '''punto_check_total_params :'''

  global dir_func, contador_params

  function_param_signature = dir_func.get_param_types(called_func)
  if (len(function_param_signature) != contador_params):
    raise Exception(f"ERROR: La cantidad de parámetros no concuerda con {called_func}.")

  contador_params = 0

# Creates GOSUB quadruple and only if function is not void
def p_punto_create_gosub(p):
  '''punto_create_gosub :'''

  global lista_de_cuadruplos, stack_de_operandos, stack_de_tipos

  func_quadruple_pos = dir_func.get_func_quadruple_init(called_func)
  quadruple = Quadruple(95, called_func, None, func_quadruple_pos)
  lista_de_cuadruplos.append(quadruple.transform_quadruple())

  func_return_type = dir_func.symbol_table['dir_functions'][called_func]['return_type']
  if(func_return_type != 0):
    func_global_var_address = dir_func.get_variable_address('inicio', called_func)
    temp_var = assign_memory_temporal(func_return_type, current_func)
    quadruple = Quadruple(70, func_global_var_address, None , temp_var) #adress of global func variable
    lista_de_cuadruplos.append(quadruple.transform_quadruple())
    
    stack_de_operandos.append(temp_var)
    stack_de_tipos.append(func_return_type)

def p_imprimir(p):
  '''
  imprimir : IMPRIMIR LPAREN imprimir_aux RPAREN SEMICOLON
  imprimir_aux : exp push_imprimir imprimirCycle
              | CTESTRING push_imprimir imprimirCycle
  imprimirCycle : COMMA imprimir_aux
              | empty
  '''

# It created a Quadruple for the print instruction. If there's something left within the
# stack of operands that means it is either a variable, expression or an int/float. If not it means it's
# a constant string. For each it will create the corresponding Quadruple.
def p_push_imprimir(p):
  '''push_imprimir :'''

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
      constant_address = assign_memory_constant(5)
      dir_func.add_constant_variable(5, constant, constant_address)
    quadruple = Quadruple(converted_operador, None, None, constant_address)
    lista_de_cuadruplos.append(quadruple.transform_quadruple())

def p_empty(p):
  '''
  empty : 
  '''
  pass

def p_error(p):
  global error
  error = True

  raise Exception("ERROR: Hay un error de sintaxis en la linea %d" % (p.lineno))

parser = yacc.yacc()
  
def parser(filePath, user_input=None):
  #Testear el parser y léxico juntos
  try:
    file = open(filePath, "r")
    archivo = file.read()
    file.close()
    global input_array
    if user_input != None:
      input_array = user_input.split()

    yacc.parse(archivo)

    if error: 
      return "Hay errores de sintaxis."
    else:
      global current_func, output_array
      current_func = 'inicio'
      return {'data': output_array, 'status': 200}

  except EOFError:
    print('ERROR', EOFError)

if __name__ == '__main__':
	parser()