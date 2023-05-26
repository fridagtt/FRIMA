def convert_type(type):
  """Returns the numeric value of the string received

    Parameters:
    type (string): string to be converted into a number

    Returns:
    int: numeric value of the string

   """
  match type:
    case 'sinregresar':
      return 0
    case 'entero':
      return 1
    case 'decimal':
      return 2
    case 'letra':
      return 3
    case 'bool':
      return 4
    case 'letrero':
      return 5
    case '+':
      return 10
    case '-':
      return 15
    case '*':
      return 20
    case '/':
      return 25
    case '>':
      return 30
    case '<':
      return 35
    case '>=':
      return 40
    case '<=':
      return 45
    case '!=':
      return 50
    case '==':
      return 55
    case 'y':
      return 60
    case 'o':
      return 65
    case '=':
      return 70
    case 'GOTOF':
      return 75
    case 'GOTO':
      return 80
    case 'ENDFUNC':
      return 85
    case 'imprimir':
      return 90
    case 'GOSUB':
      return 95
    case 'ERA':
      return 100
    case 'PARAM':
      return 105
    case 'RET':
      return 110
    case 'leer':
      return 115
    case 'VER':
      return 120
    case _:
      return -1

def fill(end, cont, lista_de_cuadruplos) -> list:
  """Returns the list of quadruples updated with the jump of every missing GOTO, GOTOF, GOTOV

    Parameters:
    end (int): position of Quadruple to be completed
    cont (int): position that will be assigned to the incomplete Quadruple
    lista_de_cuadruplos (list): the list of Quadruples

    Returns:
    list: updated list of quadruples

   """
  cuadruplo_pendiente = lista_de_cuadruplos[end]
  lista_de_cuadruplos[end] = (cuadruplo_pendiente[0], cuadruplo_pendiente[1], cuadruplo_pendiente[2], cont)
  return lista_de_cuadruplos