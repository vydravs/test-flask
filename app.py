# coding=utf8
import ast
import json
import importlib
from os import listdir
from os.path import isfile
from flask import Flask, request, jsonify, render_template


module_package = 'modules'


def top_level_functions(body):
    '''Возвращает список объектов функций из объекта ast '''
    return (f for f in body if isinstance(f, ast.FunctionDef))

def parse_ast(filename):
    '''Возвращает объект ast из файла .py '''
    with open(filename, "rt") as f:
        return ast.parse(f.read(), filename=filename)

def get_modules_list(module_package):
    '''Возвращает список файлов, в папке с модулями '''
    files_list = []
    for fl in listdir(module_package): 
        if isfile(f"{module_package}/{fl}"):
            files_list.append(fl)
    return files_list


app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Hello, World!</h1>'

@app.route('/json', methods = ['POST', 'GET'])
def route_json():
    '''Принимает JSON методом POST.
    Проверяет наличие модуля и функции из JSON.
    При наличии, передаёт JSON функции, возвращает результат.
    '''
    if request.method == 'POST':
        content = request.get_json(silent=True)
        if type(content) is dict:
            # Moduele name in package mast starts with dot
            m_name = f".{content['module']}"
            try:
                module_name = importlib.import_module(m_name,
                                                      package=module_package)
            except Exception as e:
                return f"Unknown module {content['module']}\n{e}", 500
            try:
                func_name = getattr(module_name, content['function'])(content)
            except Exception as e:
                return f"Unknown function {content['function']}\n{e}", 500
            return json.dumps(content), 200, {'ContentType':'application/json'}
        else:
            return '<h1>POST data must be JSON</h1>'
    else:
        return '<h1>Route /json/ apply only POST request</h1>'

@app.route('/html', methods = ['GET'])
def route_html():
    '''Отображает таблицу с доступными модулями и функциями.'''
    table_list = []
    for filename in get_modules_list(module_package):
        tree = parse_ast(f"{module_package}/{filename}")
        func_dict = {}
        for func in top_level_functions(tree.body):
            func_dict['module'] = filename[:-3]
            func_dict['f_name'] = func.name
            func_dict['docstring'] = ast.get_docstring(func).replace('\n', ' ')
            table_list.append(func_dict)
    return render_template('index.html', table_list=table_list), 200


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)