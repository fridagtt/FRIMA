class SemanticCube:
  def __init__(self):
    self.semantic_cube = {
      'int': {
        'int': {
          '+': 'int',
          '-': 'int',
          '*': 'int',
          '/': 'float',
          '>': 'bool',
          '<': 'bool',
          '>=': 'bool',
          '<=': 'bool',
          '!=': 'bool',
          '==': 'bool',
          'y': 'error',
          'o': 'error',
          '=': 'int',
        },
        'float': {},
      },
      'float': {
        
      },
    }

  def get_type(self, leftType, rightType, op):
    """ Returns the data type expected from performing the operation """
    return self.semantic_cube[leftType][rightType][op]