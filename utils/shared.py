def convert_type(type):
  """Returns the numeric value of the string received

    Parameters:
    type (string): String to be converted into a number

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
    case 'GOTOV':
      return 85
    case 'imprimir':
      return 90
    case _:
      return -1