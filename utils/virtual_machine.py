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

class Virtual_Machine:
  def __init__(self, quadruples, dir_func):
    print("")