class SymbolTable:
  def __init__(self):
    self.symbol_table = {
      'dir_functions': {
        'dir_func_names': set(),
        'programa': {
          'param_types': [],
          'return_type': 'void',
          'kind': 'np', # np -> nombre de programa
          'variables': {
            'var_names': set(),
            'vars_info' : [],
          },
        },
      }
    }

  def add_variable(self, type, name, func_name): 
    if name not in self.symbol_table["dir_functions"][func_name]["variables"]["var_names"]:
      self.symbol_table["dir_functions"][func_name]["variables"]["var_names"].add(name)
      self.symbol_table["dir_functions"][func_name]["variables"]['vars_info'].append({'name': name, 'type': type})
    else: 
      return ("ERROR: Variable {name} ya declarada")
    
  def add_function(self, return_type, func_name, param_types, param_names): 
    if func_name not in self.symbol_table["dir_functions"]["dir_func_names"]:
      self.symbol_table["dir_functions"]["dir_func_names"].add(func_name)
      self.symbol_table["dir_functions"][func_name]
    else: 
      return ("ERROR: Variable {name} ya declarada")
    
  