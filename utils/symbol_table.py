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
      }
    }

  def add_variable(self, type, name, func_name, dimension=0, size=0):
    """ Add variables to the variable table of the corresponding function """
    access_dict = self.symbol_table["dir_functions"][func_name]["variables"]
    if name not in access_dict["var_names"]:
      access_dict["var_names"].add(name)
      access_dict['vars_info'].append({'name': name, 'type': type, 'dimension': dimension, 'size': size})
    else: 
      return ("ERROR: La variable {name} ya está declarada")
    
  def add_function(self, func_name, return_type): 
    """ Add functions to the function directory if the don't exist """
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
      return ("ERROR: La función {func_name} ya está declarada")

  def add_function_params(self, func_name, param_type, param_name):
    """ Add parameters to the variable table of the corresponding function """
    self.symbol_table["dir_functions"][func_name]["param_types"].append(param_type)
    self.symbol_table["dir_functions"][func_name]["variables"]['var_names'].add(param_name)
    self.symbol_table["dir_functions"][func_name]["variables"]['vars_info'].append({'name': param_name, 'type': param_type})
  
  def get_function_variables(self, func_name) -> set():
    """ Returns function variables """
    return self.symbol_table["dir_functions"][func_name]["variables"]['var_names']

  def get_variable_type(self, func_name, variable_name) -> int:
    """ Returns variable type """
    set_of_variables = self.get_function_variables(func_name)
    if variable_name in set_of_variables:
        list_of_variables = self.symbol_table["dir_functions"][func_name]["variables"]['vars_info']
        variable_object = next((variable for variable in list_of_variables if variable['name'] == variable_name),None)
        return variable_object['type']
    else:
        list_of_variables = self.symbol_table["dir_functions"]['programa']["variables"]['vars_info']
        variable_object = next((variable for variable in list_of_variables if variable['name'] == variable_name),None)
        return variable_object['type']

  def is_variable_declared(self, func_name, variable_name) -> bool:
    """ Returns if variable is neither declared within the local or global scope """
    set_of_variables = self.get_function_variables(func_name)
    if variable_name not in set_of_variables:
        return variable_name in self.get_function_variables('programa')
    else:
        return True
  