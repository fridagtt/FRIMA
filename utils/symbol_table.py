class SymbolTable:
  def __init__(self):
    self.symbol_table = {
      'dir_functions': {
        'dir_func_names': set(),
        'programa': {
          'param_types': [],
          'return_type': 'void',
          'kind': 'np', # np -> nombre of program
          'variables': {
            'var_names': set(),
            'vars_info' : [],
          },
        },
      },
      'constant_table': {},
    }

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
    else: 
      raise Exception(f"ERROR: La variable {name} ya está declarada.")
    
  def add_function(self, func_name, return_type): 
    """Adds a function to the function directory if it doesn't exist

    Parameters:
    func_name (string): name of the function to be added
    return_type (int): return type of the function

    Returns:
    void: modified function directory or an error if the function already exists

   """
    access_dict = self.symbol_table["dir_functions"]["dir_func_names"]
    if func_name not in access_dict:
      access_dict.add(func_name)
      self.symbol_table["dir_functions"][func_name] = {
        'param_types': [],
        'return_type': return_type,
        'kind': 'function',
        'variables': {
          'var_names': set(),
          'vars_info' : [],
        },
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
    elif func_name != "programa":
        list_of_variables = self.symbol_table["dir_functions"]['programa']["variables"]['vars_info']
        variable_object = next((variable for variable in list_of_variables if variable['name'] == variable_name),None)
        return variable_object['type']
    
  def get_variable_dir(self, func_name, variable_name) -> int:
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
    elif func_name != "programa":
        list_of_variables = self.symbol_table["dir_functions"]['programa']["variables"]['vars_info']
        variable_object = next((variable for variable in list_of_variables if variable['name'] == variable_name),None)
        return variable_object['memory_dir']

  def is_variable_declared(self, func_name, variable_name) -> bool:
    """Validates if the variables is either declared within the local or global scope

      Parameters:
      func_name (string): name of the function
      variable_name (string): name of the variable

      Returns:
      bool(): whether the variable exists within the local or global scope

    """
    set_of_variables = self.get_function_variables(func_name)
    if variable_name not in set_of_variables and func_name != 'programa':
        return variable_name in self.get_function_variables('programa')
    else:
        return True
    
  def add_constant_variable(self, const_type, const_value, const_memory_dir):
    """Adds the constant and its memory direction to the global variable table

    Parameters:
    const_type (int): type of the constant (int - 1, float - 2, char - 3, string - 5)
    const_value (string): value of the constant to be added
    const_memory_dir (int): assigned memory of the constant

    Returns:
    void: modified global variable table with the constant added.

    """
    self.symbol_table['constant_table'][const_value] = {
      'type': const_type,
      'memory_dir': const_memory_dir,
      'value': const_value,
    }
  
  def get_constant_address(self, const_value)-> int:
    """Fetches the memory address of the requested constant value

    Parameters:
    const_value (string): value of the constant to be fetched

    Returns:
    int(): memory address of the requested constant

    """
    if(const_value in self.symbol_table['constant_table']):
      return self.symbol_table['constant_table'][const_value]['memory_dir']
    else:
      return None

  def delete_function_var_table(self, current_func):
    """Deletes variable table of function received

    Parameters:
    current_func (string): name of the function to delete its variable table

    Returns:
    void: modified variable table

    """
    del self.symbol_table['dir_functions'][current_func]['variables']
  