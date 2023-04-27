def convert_type(type):
  match type:
    case 'sinregresar':
      return 0
    case 'entero':
      return 1
    case 'decimal':
      return 2
    case 'char':
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
    case 'GOTOF':
      return 70
    case 'GOTO':
      return 75
    case 'GOTOV':
      return 80
    case _:
      return -1