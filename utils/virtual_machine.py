from collections import deque
from copy import deepcopy,copy

class Memory:
  def __init__(self, func_name, func_info):
    self.func_info = func_info
    self.function_name = func_name
    self.vars_int = dict()
    self.vars_float = dict()
    self.vars_bool = dict()
    self.vars_string = dict()
  
  def init_constant_memory(self):
    """The constant variables are initialized with its corresponding value.

    Returns:
    void: modified constant memory

    """ 
    for memory_address in self.func_info:
      # const strings
      if memory_address >= 30000 and memory_address < 32000:
        self.vars_string[memory_address] = self.func_info[memory_address]['value']
      # const ints
      elif memory_address >= 32000 and memory_address < 34000:
        self.vars_int[memory_address] = self.func_info[memory_address]['value']
      # const floats
      elif memory_address >= 34000 and memory_address < 36000:
        self.vars_float[memory_address] = self.func_info[memory_address]['value']

  def init_global_memory(self):
    """Splits global variables into its types and initializes them in empty values.

    Returns:
    void: modified global memory

    """
    for var in self.func_info['variables']['vars_info']:
      memory_address = var['memory_dir']
      # global ints
      if memory_address >= 2000 and memory_address < 4000:
        self.vars_int[memory_address] = None
      # global floats
      elif memory_address >= 4000 and memory_address < 6000:
        self.vars_float[memory_address] = None

  def get_value(self, memory_address):
    if (memory_address >= 8000 and memory_address < 10000) or (memory_address >= 22000 and memory_address < 24000)	or (memory_address >= 2000 and memory_address < 4000) or (memory_address >= 14000 and memory_address < 16000) or (memory_address >= 32000 and memory_address < 34000):
      if memory_address in self.vars_int:
        return self.vars_int[memory_address]
    elif (memory_address >= 4000 and memory_address < 6000) or (memory_address >= 16000 and memory_address < 18000) or (memory_address >= 8000 and memory_address < 10000) or (memory_address >= 24000 and memory_address < 26000) or (memory_address >= 34000 and memory_address < 36000):
      if memory_address in self.vars_float:
        return self.vars_float[memory_address]
    elif (memory_address >= 28000 and memory_address < 30000) or (memory_address >= 20000 and memory_address < 22000):
      if memory_address in self.vars_bool:
        return self.vars_bool[memory_address]
    elif (memory_address >= 30000 and memory_address < 32000):
      if memory_address in self.vars_string:
        return self.vars_string[memory_address]
  
  def set_value(self, memory_address, value):
    if (memory_address >= 8000 and memory_address < 10000) or (memory_address >= 22000 and memory_address < 24000)	or (memory_address >= 2000 and memory_address < 4000) or (memory_address >= 14000 and memory_address < 16000) or (memory_address >= 32000 and memory_address < 34000):
      self.vars_int[memory_address] = value
    elif (memory_address >= 4000 and memory_address < 6000) or (memory_address >= 16000 and memory_address < 18000) or (memory_address >= 8000 and memory_address < 10000) or (memory_address >= 24000 and memory_address < 26000) or (memory_address >= 34000 and memory_address < 36000):
      self.vars_float[memory_address] = value
    elif (memory_address >= 28000 and memory_address < 30000) or (memory_address >= 20000 and memory_address < 22000):
      self.vars_bool[memory_address] = value
    elif (memory_address >= 30000 and memory_address < 32000):
      self.vars_string[memory_address] = value
  
  def add_params_to_function(self, params_list):
    for index, value in enumerate(params_list):
      if type(value[0]) is int:
        if self.func_info['param_types'][index] != 1:
          self.vars_int[value[1]] = value
        else:
          print("Error - El parámetro #", index +1, "en", self.function_name, "no es del tipo esperado.")
      elif type(value[0]) is float:
        if self.param_types['param_types'][index] != 2:
          self.vars_float[value[1]] = value
        else:
          print("Error - El parámetro #", index +1, "en", self.function_name, "no es del tipo esperado.")

  def add_return_value(self, value, return_type, function_name_address):
    if return_type == 1:
      self.vars_int[function_name_address] = value
    elif return_type == 2:
      self.vars_float[function_name_address] = value
    
class VirtualMachine:
  def __init__(self, quadruples, dir_func):
    self.list_quadruples = quadruples
    self.dir_func = dir_func
    self.global_memory = Memory('inicio', dir_func['dir_functions']['inicio'])
    self.constant_memory = Memory('constants', dir_func['constant_table'])
    self.local_memory = Memory(None, None)
    self.execution_stack = deque()
    self.stack_pointers = deque()

  def get_memory(self, memory_address) -> Memory:
    """According to the memory address received, it returns either the vm's local or global memory

    Parameters:
    memory_address (int): memory address stored in the quadruple.

    Returns:
    Memory: either a global, constant, or local memory

    """
    # global, global temps
    if (memory_address >= 2000 and memory_address < 8000) or (memory_address >= 14000 and memory_address < 22000):
      return self.global_memory
    # constants
    elif (memory_address >= 30000 and memory_address < 38000):
      return self.constant_memory
    # local and local temps
    elif (memory_address >= 8000 and memory_address < 14000) or (memory_address >= 22000 and memory_address < 30000):
      return self.local_memory

  def set_memory_value(self, memory_address, value):
    print("set_memory_value", memory_address, value)
    self.get_memory(memory_address).set_value(memory_address, value)

  def get_memory_value(self, memory_address):
    return self.get_memory(memory_address).get_value(memory_address)

  def get_quadruple_values(self, quadruple):
    return quadruple[0], quadruple[1], quadruple[2], quadruple[3]
    
  def read_quadruples(self):
    instruction_pointer = 0
    params_list = []
    while (instruction_pointer < len(self.list_quadruples)):
      operator, left_operand, right_operand, quad_res = self.get_quadruple_values(self.list_quadruples[instruction_pointer])
      if operator == 10: # Add
        try:
          left_value = self.get_memory_value(left_operand)
          right_value = self.get_memory_value(right_operand)
          result = left_value + right_value
          self.set_memory_value(quad_res, result)
          instruction_pointer += 1
        except:
          raise Exception("Error: Variable sin valor")
      elif operator == 15: # Substract
        try:
          left_value = self.get_memory_value(left_operand)
          right_value = self.get_memory_value(right_operand)
          result = left_value - right_value
          self.set_memory_value(quad_res, result)
          instruction_pointer += 1
        except:
          raise Exception("ERROR: Variable sin valor")
      elif operator == 20: # Multiply
        try:
          left_value = self.get_memory_value(left_operand)
          right_value = self.get_memory_value(right_operand)
          result = left_value * right_value
          self.set_memory_value(quad_res, result)
          instruction_pointer += 1
        except:
          raise Exception("ERROR: Variable sin valor")
      elif operator == 25: # Divide
        try:
          left_value = self.get_memory_value(left_operand)
          right_value = self.get_memory_value(right_operand)
          if right_value == 0:
            raise Exception("ERROR: No se pueden hacer divisiones entre 0")
          result = left_value / right_value
          self.set_memory_value(quad_res, result)
          instruction_pointer += 1
        except:
          raise Exception("ERROR: Variable sin valor")
      elif operator == 30: # >
        try:
          left_value = self.get_memory_value(left_operand)
          right_value = self.get_memory_value(right_operand)
          result = left_value > right_value
          self.set_memory_value(quad_res, result)
          instruction_pointer += 1
        except:
          raise Exception("ERROR: Variable sin valor")
      elif operator == 35: # <
        try:
          left_value = self.get_memory_value(left_operand)
          right_value = self.get_memory_value(right_operand)
          result = left_value < right_value
          self.set_memory_value(quad_res, result)
          instruction_pointer += 1
        except:
          raise Exception("ERROR: Variable sin valor")
      elif operator == 40: # >=
        try:
          left_value = self.get_memory_value(left_operand)
          right_value = self.get_memory_value(right_operand)
          result = left_value >= right_value
          self.set_memory_value(quad_res, result)
          instruction_pointer += 1
        except:
          raise Exception("ERROR: Variable sin valor")
      elif operator == 45: # <=
        try:
          left_value = self.get_memory_value(left_operand)
          right_value = self.get_memory_value(right_operand)
          result = left_value <= right_value
          self.set_memory_value(quad_res, result)
          instruction_pointer += 1
        except:
          raise Exception("ERROR: Variable sin valor")
      elif operator == 50: # !=
        try:
          left_value = self.get_memory_value(left_operand)
          right_value = self.get_memory_value(right_operand)
          result = left_value != right_value
          self.set_memory_value(quad_res, result)
          instruction_pointer += 1
        except:
          raise Exception("ERROR: Variable sin valor")
      elif operator == 55: # ==
        try:
          left_value = self.get_memory_value(left_operand)
          right_value = self.get_memory_value(right_operand)
          result = left_value == right_value
          self.set_memory_value(quad_res, result)
          instruction_pointer += 1
        except:
          raise Exception("ERROR: Variable sin valor")
      elif operator == 60: # y
        try:
          left_value = self.get_memory_value(left_operand)
          right_value = self.get_memory_value(right_operand)
          result = left_value and right_value
          self.set_memory_value(quad_res, result)
          instruction_pointer += 1
        except:
          raise Exception("ERROR: Variable sin valor")
      elif operator == 65: # o
        try:
          left_value = self.get_memory_value(left_operand)
          right_value = self.get_memory_value(right_operand)
          result = left_value or right_value
          self.set_memory_value(quad_res, result)
          instruction_pointer += 1
        except:
          raise Exception("ERROR: Variable sin valor")
      elif operator == 70: # Assign
        try:
          value = self.get_memory_value(left_operand)
          self.set_memory_value(quad_res, value)
          instruction_pointer += 1
        except:
          raise Exception("ERROR: Variable sin valor")
      elif operator == 80: # GOTO
        instruction_pointer = quad_res
      elif operator == 90: # IMPRIMIR
        try:
          if type(quad_res) is str:
            value_memory =  self.global_memory.get_memory_value(quad_res)
          else:
            value_memory = self.get_memory_value(quad_res)
          print("ARITMETICA -> ", value_memory)
          instruction_pointer += 1
        except:
          raise Exception("ERROR: Variable sin valor")
      elif operator == 95: # GOSUB
        self.stack_pointers.append(instruction_pointer + 1) # guardar migajita de pan
        instruction_pointer = quad_res # quadruple where the next function starts
        self.local_memory.add_params_to_function(params_list)
        params_list = []
      elif operator == 100: # ERA
        self.prev_memory = deepcopy(self.local_memory)
        if (len(self.execution_stack) < 100):
          self.execution_stack.append(self.prev_memory)
          self.prev_memory = None
        else:
          raise Exception("ERROR: Stack Overflow")
        self.local_memory = Memory(left_operand, self.dir_func['dir_functions'][left_operand])
        instruction_pointer +=1
      elif operator == 105: # PARAM
        value = self.get_memory_value(left_operand)
        params_list.append((value, left_operand)) # save (value, address)
        instruction_pointer +=1
      elif operator == 110: # RET
        value = self.get_memory_value(quad_res)
        print("value", value)
        print("value", right_operand)
        print("operator", quad_res, value, right_operand)
        self.set_memory_value(quad_res, value)
        self.global_memory.add_return_value(value, self.local_memory.func_info['return_type'], right_operand) # right_operand -> func_name_address
        instruction_pointer += 1
      elif operator == 85: # END FUNC
        if(len(self.execution_stack)!=0):
          self.local_memory = self.execution_stack.pop()
          instruction_pointer = self.stack_pointers.pop()

  def execute(self):
    print("-------------------CORRIENDO MAQUINA VIRTUAL-----------------------")
    self.constant_memory.init_constant_memory()
    self.global_memory.init_global_memory()
    self.read_quadruples()
    print("global_memory", self.global_memory.vars_int, self.global_memory.vars_float)
