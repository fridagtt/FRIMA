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
    """ Add variables to variables table of the corresponding function """
    access_dict = self.symbol_table["dir_functions"][func_name]["variables"]
    if name not in access_dict["var_names"]:
      access_dict["var_names"].add(name)
      access_dict['vars_info'].append({'name': name, 'type': type, 'dimension': dimension, 'size': size})
    else: 
      return ("ERROR: La variable {name} ya está declarada")
    
  def add_function(self, func_name, return_type): 
    """ Add functions to the function directory if it doesn't exist """
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
    """ Add parameters to the variables table of the corresponding function """
    self.symbol_table["dir_functions"][func_name]["param_types"].append(param_type)
    self.symbol_table["dir_functions"][func_name]["variables"]['var_names'].add(param_name)
    self.symbol_table["dir_functions"][func_name]["variables"]['vars_info'].append({'name': param_name, 'type': param_type})
    
  