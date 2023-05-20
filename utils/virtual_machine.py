from collections import deque

class Memory:
  def __init__(self, func_name, dir_func):
    self.dir_func = dir_func
    self.function_name = func_name
    self.type_int = dict()
    self.type_float = dict()
    self.type_char = dict()
    self.type_bool = dict()
    self.type_string = dict() 
    self.init_quadruple = None
    self.param_types = None 
    self.return_type = None

  def init_global_memory(self):
    for var in self.dir_func['dir_functions']['inicio']['variables']['vars_info']:
      memory_dir = var['memory_dir']
      # global ints
      if memory_dir >= 2000 and memory_dir < 4000:
        self.type_int[memory_dir] = {
          'value': None
        }
      # global floats
      elif memory_dir >= 4000 and memory_dir < 6000:
        self.type_int[memory_dir] = {
          'value': None
        }
      # global chars
      elif memory_dir >= 6000 and memory_dir < 8000:
        self.type_int[memory_dir] = {
          'value': None
        }

    for key in self.dir_func['dir_functions']['constant_table']:
      # const strings
      if key >= 30000 and key < 32000:
        self.type_int[memory_dir] = {
          'value': key['value']
        }
      # const ints
      elif key >= 32000 and key < 34000:
        self.type_int[memory_dir] = {
          'value': key['value']
        }
      # const floats
      elif key >= 34000 and key < 36000:
        self.type_int[memory_dir] = {
          'value': key['value']
        }
      # const chars
      elif key >= 36000 and key < 38000:
        self.type_int[memory_dir] = {
          'value': key['value']
        }
  
  def get_value(self, memory_address):
    if (memory_address >= 8000 and memory_address < 10000) or (memory_address >= 22000 and memory_address < 24000)	or (memory_address >= 2000 and memory_address < 4000) or (memory_address >= 14000 and memory_address < 16000) or (memory_address >= 32000 and memory_address < 34000):
      if memory_address in self.type_int:
        return self.type_int[memory_address]['value']
      else:
        return self.new_int(memory_address)
    elif (memory_address >= 4000 and memory_address < 6000) or (memory_address >= 16000 and memory_address < 18000) or (memory_address >= 8000 and memory_address < 10000) or (memory_address >= 24000 and memory_address < 26000) or (memory_address >= 34000 and memory_address < 36000):
      if memory_address in self.type_float:
        return self.type_float[memory_address]['value']
      else:
        return self.new_float(memory_address)
    elif (memory_address >= 12000 and memory_address < 14000) or (memory_address >= 26000 and memory_address < 28000) or ( memory_address >= 36000 and memory_address < 38000) or (memory_address >= 6000 and memory_address < 8000) or (memory_address >= 18000 and memory_address < 20000):
      if memory_address in self.type_char:
        return self.type_char[memory_address]['value']
      else:
        return self.new_char(memory_address)
    elif (memory_address >= 28000 and memory_address < 30000) or (memory_address >= 20000 and memory_address < 22000):
      if memory_address in self.type_bool:
        return self.type_bool[memory_address]['value']
      else:
        return self.new_bool(memory_address)
    elif (memory_address >= 30000 and memory_address < 32000):
      if memory_address in self.type_str:
        return self.type_str[memory_address]['value']
      else:
        return self.new_str(memory_address)

class VirtualMachine:
  def __init__(self, quadruples, dir_func):
    self.list_quadruples = quadruples
    self.dir_func = dir_func
    self.global_memory = Memory('inicio', dir_func)
    self.execution_stack = deque()
    self.local_memory = Memory('local', dir_func)

  def process_quadruples(self):
    current_quad = 0
    while (current_quad < len(self.list_quadruples)):
      print("CURRENT QUADRUPLE: ", self.list_quadruples[current_quad])
      
      if self.list_quadruples[current_quad][0] == 10:
        try:
          left_value = self.get_memory(self.arr_quadruples[current_quad][1]).get_value(self.arr_quadruples[current_quad][1])
          right_value = self.get_memory(self.arr_quadruples[current_quad][2]).get_value(self.arr_quadruples[current_quad][2])
          result = left_value + right_value
          self.get_memory(self.arr_quadruples[current_quad][3]).set_value(self.arr_quadruples[current_quad][3], result)
          current_quad += 1
        except:
          raise Exception("Error: Variable sin valor")
				
      elif self.arr_quadruples[current_quad][0] == '-':
        try:
          left_value = self.get_memory(self.arr_quadruples[current_quad][1]).get_value(self.arr_quadruples[current_quad][1])
          right_value =  self.get_memory(self.arr_quadruples[current_quad][2]).get_value(self.arr_quadruples[current_quad][2])
          result = left_value - right_value
          self.get_memory(self.arr_quadruples[current_quad][3]).set_value(self.arr_quadruples[current_quad][3], result)
          current_quad += 1
        except:
          raise Exception("ERROR: Variable sin valor")
				
      elif self.arr_quadruples[current_quad][0] == '=':
        try:
          value = self.get_memory(self.arr_quadruples[current_quad][1]).get_value(self.arr_quadruples[current_quad][1])
          if type(self.arr_quadruples[current_quad][3]) == str:
            self.local_memory.set_value(self.arr_quadruples[current_quad][3], value)
          else:
            self.get_memory(self.arr_quadruples[current_quad][3]).set_value(self.arr_quadruples[current_quad][3], value)
          current_quad += 1
        except:
          raise Exception("ERROR: Variable sin valor")

      elif self.arr_quadruples[current_quad][0] == '*':
        try:
          left_value = self.get_memory(self.arr_quadruples[current_quad][1]).get_value(self.arr_quadruples[current_quad][1])
          right_value =  self.get_memory(self.arr_quadruples[current_quad][2]).get_value(self.arr_quadruples[current_quad][2])
          result = left_value * right_value
          self.get_memory(self.arr_quadruples[current_quad][3]).set_value(self.arr_quadruples[current_quad][3], result)
          current_quad += 1
        except:
          raise Exception("ERROR: Variable sin valor")
        
      elif self.arr_quadruples[current_quad][0] == '/':
        try:
          left_value = self.get_memory(self.arr_quadruples[current_quad][1]).get_value(self.arr_quadruples[current_quad][1])
          right_value = self.get_memory(self.arr_quadruples[current_quad][2]).get_value(self.arr_quadruples[current_quad][2])
          if right_value == 0:
            raise Exception("ERROR: No se pueden hacer divisiones entre 0")
          result = left_value / right_value
          self.get_memory(self.arr_quadruples[current_quad][3]).set_value(self.arr_quadruples[current_quad][3], result)
          current_quad += 1
        except:
          raise Exception("ERROR: Variable sin valor")
				
  def get_memory(self, memory_address):
    # global, global temps, and constants
    if (memory_address >= 2000 and memory_address < 8000) or (memory_address >= 14000 and memory_address < 22000) or (memory_address >= 30000 and memory_address < 38000):
      return self.global_memory
    # local and local temps
    elif (memory_address >= 8000 and memory_address < 14000) or (memory_address >= 22000 and memory_address < 30000):
      return self.local_memory
    
  def execute(self):
    print("-------------------MAQUINA--VIRTUAL-----------------------")
    self.global_memory.init_global_memory()
    self.process_quadruples()
