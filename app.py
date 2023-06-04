from flask import Flask, request
from parser_frima import parser
import ast
import os
import json 
import datetime

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def hello_world():
  return 'Hello, World!'

'''Endpoint que manda a llamar al compilador'''
@app.route('/compiler', methods=['GET'])
def compiler():
  try:
    user_input = request.args.get("input")
    file_path = request.args.get("path")
    if user_input == '':
      return parser(file_path), 200
    else:
      return parser(file_path, user_input), 200
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
    f = open(str(file_path), "r")
    n = f.read()
    return n
  except:
    return 'Error: No se pudo leer el archivo', 400

'''Endpoint para crear un nuevo archivo'''   
@app.route('/createFile')
def create_File():
  param_name = request.args.get("file", "")
  name = param_name.replace(" ", "")
  file_name = "tests/"+ name + ".txt"
  open(file_name, "w+")
      
  new_file = {
    "name": param_name,
    "createdAt": str(datetime.datetime.now().strftime("%x")),
    "path": file_name            
  }
  n = None
  data = None
  
  with open('files.json') as f:
    data = json.load(f)
    data['files'].append(new_file)
    n = data
    p_json = json.dumps(n)
    print(p_json, file=open("files.json", "w"))
      
  return {"data": n}

'''Endpoint para eliminar un archivo'''   
@app.route('/deleteFile')
def delete_file():
  get_name = request.args.get("file", "")
  with open('files.json') as f:
    data = json.load(f)
    for i, value in enumerate( data['files']):
      if value['name'] == get_name:
        data['files'].pop(i)
            
    n = data
    p_json = json.dumps(n)
    print(p_json, file=open("files.json", "w"))
  return 'deleted'

'''Endpoint para guardar contenido de un archivo'''
@app.route('/saveFile', methods=['POST'])
def save_file():
  try:
    req_data = request.get_json()
    file_content = req_data['fileContent']
    file_path = req_data['filePath']

    with open(file_path, 'w') as file:
      file.write(file_content)
      
    return 'Archivo guardado!', 200
  except:
    return 'Error: No se pudo guardar el archivo', 400

if __name__ == "__main__":
  app.run(debug=True)
