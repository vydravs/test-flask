# coding=utf8
import re
import json
import importlib
from os import listdir
from os.path import isfile
from flask import Flask, request, jsonify, render_template


module_package = 'modules'


def get_modules_list(module_package):
    '''Возвращает список файлов, из папки с модулями.'''
    files_list = []
    for fl in listdir(module_package): 
        if isfile(f"{module_package}/{fl}"):
            files_list.append(fl)
    return files_list

def get_func_list(file_with_path):
    '''Возвращает список функций(имя, докстринг, тело).'''
    func_list = []
    is_function = False
    for line in open(file_with_path, 'r').readlines():
        if re.search(r'^def \w+\(', line):
            if is_function:
                func_list.append(func_dict)
            func_dict = {}
            func_dict['name'] = line
            func_dict['body'] = line
            is_function = True
            continue
        if re.search(r'^    .+', line) and is_function:
            func_dict['body'] += line
            continue
        if re.search(r'^\w.+', line) and is_function:
            func_list.append(func_dict)
            is_function = False
            continue
    if is_function:
        func_list.append(func_dict)
    for func in func_list:
        f_name = re.search(r'def \w+\(', func['name'])
        func['name'] = f_name[0][4:-1]
        str_body = func['body'].replace('\n', '')
        docstring = re.search(r'(\'{3}|\"{3}).+(\'{3}|\"{3})', str_body)
        if docstring is not None:
            func['docstring'] = ' '.join(docstring[0][3:-3].split())
        else:
            func['docstring'] = ''
    return func_list


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
        func_list = get_func_list(f"{module_package}/{filename}")
        for func in func_list:
            func_dict = {}
            func_dict['module'] = filename[:-3]
            func_dict['f_name'] = func['name']
            func_dict['docstring'] = func['docstring']
            func_dict['body'] = func['body']
            table_list.append(func_dict)
    return render_template('index.html', table_list=table_list), 200


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)