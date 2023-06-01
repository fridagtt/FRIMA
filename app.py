from flask import Flask, request
import ast
import datetime
import os
import json 

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def hello_world():
  return 'Hello, World!'

'''
  Funcion que manda a llamar el compilador con el archivo indicado
'''
@app.route('/compiler', methods=['GET'])
def compiler():
  try:
    usr_input = request.args.get("input")
    file_name = request.args.get("name")
    if usr_input == '':
      return parser(file_name), 200
    else:
      return parser(file_name, usr_input), 200
  except Exception as e:
    return str(e), 400

'''Endpoint para obtener la lista de los archivos guardados'''
@app.route('/files', methods=['GET'])
def get_files():
  with open('files.json') as f:
    data = json.load(f)
  return data, 200

'''Endpoint para leer la información de un archivo'''
@app.route('/readFile', methods=['GET'])
def read_file():
  try:
    file_path = request.args.get("path", "")
    file_path = "{}".format(file_path)
    print("el path del archivo es:", file_path)
    f = open(str(file_path), "r")
    n = f.read()
    return n
  except:
    return 'Error: No se pudo leer el archivo', 400

if __name__ == "__main__":
  app.run(debug=True)
