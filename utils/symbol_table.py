class SymbolTable:
  def __init__(self):
    self.symbol_table = {
      'dir_functions': {
        'dir_func_names': set(),
        'inicio': {
          'param_types': [], # en inicio este siempre estará vacío
          'return_type': 0,
          'variables': {
            'var_names': set(),
            'vars_info' : [],
          },
          'initial_quadruple': 0,
          'cont_temp': [0,0,0,0],
          'cont_var': [0,0,0],
        },
      },
      'constant_table': {},
    }
  
  def add_cont_temp(self, type, func_name):
    """Adds 1 to the temporal counter of variables of the type received

    Parameters:
    type (int): type of the temporal variable (int - 1, float - 2, char - 3)
    func_name (string): current function where the temporal counter is going to be added

    Returns:
    void: modified temporal counter of each type of variable

    """
    if type == 1:
      self.symbol_table["dir_functions"][func_name]['cont_temp'][0] += 1 # enteros
    elif type == 2:
      self.symbol_table["dir_functions"][func_name]['cont_temp'][1] += 1 # flotantes
    elif type == 3:
      self.symbol_table["dir_functions"][func_name]['cont_temp'][2] += 1 # chars
    elif type == 4:
      self.symbol_table["dir_functions"][func_name]['cont_temp'][3] += 1 # booleans

  def add_cont_var(self, type, func_name):
    """Adds 1 to the counter of variables of the type received

    Parameters:
    type (int): type of the variable (int - 1, float - 2, char - 3)
    func_name (string): current function where the counter is going to be added

    Returns:
    void: modified counter of each type of variable

    """
    if type == 1:
      self.symbol_table["dir_functions"][func_name]['cont_var'][0] += 1 # enteros
    elif type == 2:
      self.symbol_table["dir_functions"][func_name]['cont_var'][1] += 1 # flotantes
    elif type == 3:
      self.symbol_table["dir_functions"][func_name]['cont_var'][2] += 1 # chars
    
  def add_variable(self, type, name, func_name, memory_dir, dimension=0, size=0):
    """Adds the variable to the variable table of the corresponding function

    Parameters:
    type (int): type of the variable (int - 1, float - 2, char - 3)
    name (string): name of the variable to be added
    func_name (string): current function where the variable is going to be added
    dimension (int): dimension of the variable (0 - simple_var, 1 - array, 2 - matrix)
    size (int): size of the variable (0 - simple_var, n - array, (n,m) - matrix)
    memory_dir (int): assigned memory of the variable

    Returns:
    void: modified variable table for the corresponding function or an error if the variable already exists.

    """
    access_dict = self.symbol_table["dir_functions"][func_name]["variables"]
    if name not in access_dict["var_names"]:
      access_dict["var_names"].add(name)
      access_dict['vars_info'].append({'name': name, 'type': type, 'dimension': dimension, 'size': size, 'memory_dir': memory_dir})
      self.add_cont_var(type, func_name)
    else: 
      raise Exception(f"ERROR: La variable {name} ya está declarada.")
    
  def add_function(self, func_name, return_type, position): 
    """Adds a function to the function directory if it doesn't exist, with its corresponding
    initial quadruple position.

    Parameters:
    func_name (string): name of the function to be added
    return_type (int): return type of the function
    position (int): quadruple position for the function

    Returns:
    void: modified function directory or an error if the function already exists

   """
    access_dict = self.symbol_table["dir_functions"]["dir_func_names"]
    if func_name not in access_dict:
      access_dict.add(func_name)
      self.symbol_table["dir_functions"][func_name] = {
        'param_types': [],
        'return_type': return_type,
        'variables': {
          'var_names': set(),
          'vars_info' : [],
        },
        'initial_quadruple': position,
        'cont_temp': [0,0,0,0],
        'cont_var': [0,0,0],
      }
    else:
      raise Exception(f"ERROR: La función {func_name} ya está declarada.")

  def add_function_params(self, func_name, param_type, param_name, memory_dir):
    """Add parameters/variables to the variable table of the corresponding function

      Parameters:
      func_name (string): name of the function where the parameter will be added
      param_type (int): type of the parameter/variable
      param_name (string): name of the parameter/variable
      memory_dir (int): assigned memory of the function parameter

      Returns:
      void: modified variable directory of the corresponding function

    """
    self.symbol_table["dir_functions"][func_name]["param_types"].append(param_type)
    self.symbol_table["dir_functions"][func_name]["variables"]['var_names'].add(param_name)
    self.symbol_table["dir_functions"][func_name]["variables"]['vars_info'].append({'name': param_name, 'type': param_type, 'memory_dir': memory_dir})
  
  def get_function_variables(self, func_name) -> set():
    """Returns the variables of the requested function

      Parameters:
      func_name (string): name of the function

      Returns:
      set(): set of the variables the requested function has

    """
    return self.symbol_table["dir_functions"][func_name]["variables"]['var_names']

  def get_variable_type(self, func_name, variable_name) -> int:
    """Returns the requested variable type. If the variable is not found within the local scope of the
      function, it looks it up within the global variable table (unless you already are within the global scope).

      Parameters:
      func_name (string): name of the function
      variable_name (string): name of the variable

      Returns:
      int(): type of the requested variable

    """
    set_of_variables = self.get_function_variables(func_name)
    if variable_name in set_of_variables:
        list_of_variables = self.symbol_table["dir_functions"][func_name]["variables"]['vars_info']
        variable_object = next((variable for variable in list_of_variables if variable['name'] == variable_name),None)
        return variable_object['type']
    elif func_name != "inicio":
        list_of_variables = self.symbol_table["dir_functions"]['inicio']["variables"]['vars_info']
        variable_object = next((variable for variable in list_of_variables if variable['name'] == variable_name),None)
        return variable_object['type']
    
  def get_variable_address(self, func_name, variable_name) -> int:
    """Returns the requested variable direction. If the variable is not found within the local scope of the
      function, it looks it up within the global variable table (unless you already are within the global scope).

      Parameters:
      func_name (string): name of the function
      variable_name (string): name of the variable

      Returns:
      int(): direction of the requested variable

    """
    set_of_variables = self.get_function_variables(func_name)
    if variable_name in set_of_variables:
        list_of_variables = self.symbol_table["dir_functions"][func_name]["variables"]['vars_info']
        variable_object = next((variable for variable in list_of_variables if variable['name'] == variable_name),None)
        return variable_object['memory_dir']
    elif func_name != "inicio":
        list_of_variables = self.symbol_table["dir_functions"]['inicio']["variables"]['vars_info']
        variable_object = next((variable for variable in list_of_variables if variable['name'] == variable_name),None)
        return variable_object['memory_dir']

  def get_param_types(self, func_name) -> list:
     """Returns the param signature array of the requested function.

      Parameters:
      func_name (string): name of the function to return its param types

      Returns:
      list(): function's param types

    """
     return self.symbol_table["dir_functions"][func_name]["param_types"]
  
  def is_variable_declared(self, func_name, variable_name) -> bool:
    """Validates if the variables is either declared within the local or global scope

      Parameters:
      func_name (string): name of the function
      variable_name (string): name of the variable

      Returns:
      bool(): whether the variable exists within the local or global scope

    """
    set_of_variables = self.get_function_variables(func_name)
    if variable_name not in set_of_variables and func_name != 'inicio':
        return variable_name in self.get_function_variables('inicio')
    else:
        return True

  def is_function_declared(self, func_name) -> bool:
    """Validates if the function requested exists in the symbol table

      Parameters:
      func_name (string): name of the function to be found

      Returns:
      bool(): whether the function exists in the symbol table

    """
    return func_name in self.symbol_table['dir_functions']
    
  def get_func_quadruple_init(self, func_name) -> int:
    """Returns function's quadruple initial position

      Parameters:
      func_name (string): name of the function requested

      Returns:
      int(): function's quadruple initial position

    """
    return self.symbol_table['dir_functions'][func_name]['initial_quadruple']
  
  def add_constant_variable(self, const_type, const_value, const_memory_dir):
    """Adds the constant variable and its memory direction to the global variable table

    Parameters:
    const_type (int): type of the constant (int - 1, float - 2, char - 3, string - 5)
    const_value (string): value of the constant to be added
    const_memory_dir (int): assigned memory of the constant

    Returns:
    void: modified global variable table with the constant added.

    """
    self.symbol_table['constant_table'][const_memory_dir] = {
      'type': const_type,
      'memory_dir': const_memory_dir,
      'value': const_value,
    }
  
  def get_constant_address(self, const_value)-> int:
    """Fetches the memory address of the requested constant value.
    It double checks the type to avoid collisions between doubles and integers e.g. 3 or 3.0

    Parameters:
    const_value (string): value of the constant to be fetched

    Returns:
    int(): memory address of the requested constant

    """
    for key, values in self.symbol_table['constant_table'].items():
      if values["value"] == const_value and type(values["value"]) == type(const_value): 
        return key
    return None

  def delete_function_var_table(self, current_func):
    """Deletes variable table of function received

    Parameters:
    current_func (string): name of the function to delete its variable table

    Returns:
    void: modified variable table

    """
    del self.symbol_table['dir_functions'][current_func]['variables']
  