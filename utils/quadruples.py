class Quadruple:
  def __init__(self, operator, leftOperand, rightOperand, result):
    self.operator = operator
    self.leftOperand = leftOperand
    self.rightOperand = rightOperand
    self.result = result
  
  def __repr__(self): 
    return f"{self.operator} {self.leftOperand} {self.rightOperand} {self.result}" 