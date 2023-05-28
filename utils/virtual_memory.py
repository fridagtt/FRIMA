# memory for global variables
global_int = 2000 
global_float = 4000
# memory for local variables
local_int = 8000
local_float = 10000
# memory for global temp variables
global_temp_int = 14000
global_temp_float = 16000
global_temp_bool = 20000
# memory for local temp variables
local_temp_int = 22000
local_temp_float = 24000
local_temp_bool = 28000
# memory for constant variables
const_string = 30000
const_int = 32000
const_float = 34000
# memory for dimensional variables
dim_pointer = 38000

#Add global_int
def get_dim_pointer():
  global dim_pointer
  if dim_pointer < 40000:
    prev_cont = dim_pointer
    dim_pointer += 1
    return prev_cont
  else: 
    raise Exception("ERROR: No hay memoria disponible para almacenar variables dimensionales")

#Add global_int
def add_global_int(size):
  global global_int
  if global_int < 4000:
    prev_cont = global_int
    global_int += size
    return prev_cont
  else: 
    raise Exception("ERROR: No hay memoria disponible para Enteros Globales")
    
#Add global_float
def add_global_float(size):
  global global_float

  if global_float < 6000:
    prev_cont = global_float
    global_float += size
    return prev_cont
  else: 
    raise Exception("ERROR: No hay memoria disponible para Decimales Globales")
    
    
#Add local_int
def add_local_int(size):
  global local_int 

  if local_int < 10000:
    prev_cont = local_int
    local_int += size
    return prev_cont
  else: 
    raise Exception("ERROR: No hay memoria disponible para Enteros Locales")
    
#Add local_float
def add_local_float(size):
  global local_float
  
  if local_float < 12000:
    prev_cont = local_float
    local_float += size
    return prev_cont
  else: 
    raise Exception("ERROR: No hay memoria disponible para Decimales Locales")


#Add global temp int 
def add_global_temp_int():
  global global_temp_int 

  if global_temp_int < 16000:
    prev_cont = global_temp_int
    global_temp_int += 1
    return prev_cont
  else: 
    raise Exception("ERROR: No hay memoria disponible para Enteros Temporales Globales") 

#Add global temp float 
def add_global_temp_float():
  global global_temp_float
  
  if global_temp_float < 18000:
    prev_cont = global_temp_float
    global_temp_float += 1
    return prev_cont
  else: 
    raise Exception("ERROR: No hay memoria disponible para Decimales Temporales Globales") 
    

#Add global temp bool
def add_global_temp_bool():
  global global_temp_bool 

  if global_temp_bool < 22000:
    prev_cont = global_temp_bool
    global_temp_bool += 1
    return prev_cont
  else: 
    raise Exception("ERROR: No hay memoria disponible para Booleanos Temporales Globales") 

#Add local temp int 
def add_local_temp_int():
  global local_temp_int 

  if local_temp_int < 24000:
    prev_cont = local_temp_int
    local_temp_int += 1
    return prev_cont
  else: 
    raise Exception("ERROR: No hay memoria disponible para Enteros Temporales Locales") 

#Add local temp float 
def add_local_temp_float():
  global local_temp_float 

  if local_temp_float < 26000:
    prev_cont = local_temp_float
    local_temp_float += 1
    return prev_cont
  else: 
    raise Exception("ERROR: No hay memoria disponible para Decimales Temporales Locales") 
    

#Add local temp bool
def add_local_temp_bool():
  global local_temp_bool

  if local_temp_bool < 30000:
    prev_cont = local_temp_bool
    local_temp_bool += 1
    return prev_cont
  else: 
    raise Exception("ERROR: No hay memoria disponible para Booleanos Temporales Globales")  

#Add const string
def add_const_string():
  global const_string 

  if const_string < 32000:
    prev_cont = const_string
    const_string += 1
    return prev_cont
  else: 
    raise Exception("ERROR: No hay memoria disponible para los Letreros")  
    
#Add const int
def add_const_int():
  global const_int 

  if const_int < 34000:
    prev_cont = const_int
    const_int += 1
    return prev_cont
  else: 
    raise Exception("ERROR: No hay memoria disponible para Enteros Constantes")  
    
#Add const float
def add_const_float():
  global const_float

  if const_float < 36000:
    prev_cont = const_float
    const_float += 1
    return prev_cont
  else: 
    raise Exception("ERROR: No hay memoria disponible para Decimales Constantes")  
    

#Borra las direcciones locales
def reset_dir_local():
  global local_int, local_float
  local_int = 8000
  local_float = 10000
  

#Borra las direcciones locales temporales
def reset_local_temp():
  global local_temp_int, local_temp_float, local_temp_bool
  local_temp_int = 22000
  local_temp_float = 24000

  local_temp_bool = 28000

def assign_memory_constant(var_type):
  if var_type == 1:
    return add_const_int()
  elif var_type == 2:
    return add_const_float()
  elif var_type == 5: # Add string to global constant memory
    return add_const_string()
       
def assign_memory_temporal(var_type, func_name):
  if var_type == 1:
    if func_name == "inicio": # Add int to global memory
      return add_global_temp_int()
    else: # Add int to local memory
      return add_local_temp_int()
  elif var_type == 2:
    if func_name == "inicio": # Add float to  global memory
      return add_global_temp_float()
    else: # Add float to local memory
      return add_local_temp_float()
  elif var_type == 4:
    if func_name == "inicio": # Add bool to global memory
      return add_global_temp_bool()
    else: # Add bool to local memory
      return add_local_temp_bool()
    
# Only global variables; not const nor temp
def assign_memory_global_local(var_type, func_name, size): 
  if var_type == 1:
    if func_name == "inicio": # Add int to global memory
      return add_global_int(size)
    else: # Add int to local memory
      return add_local_int(size)
  elif var_type == 2:
    if func_name == "inicio": # Add float to  global memory
      return add_global_float(size)
    else: # Add float to local memory
      return add_local_float(size)