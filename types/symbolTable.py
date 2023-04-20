class SymbolTable:
  def __init__(self):
    self.symbol_table = {
      'dir_functions': {
        'dir_func_names': set(), #set('main')
        'main': {
          'param_types': [],
          'return_type': 'void',
          'kind': 'np', # np -> nombre de programa
          'variables': {
            'var_names': set(),
            'vars_info' : [
              {
                'name': None,
                'type': None,
                'scope': None, # to which function the variable belongs
                'value': None,
                'kind': None,
              },
            ],
          },
        },
      }
    }