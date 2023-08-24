import re


file = 'modules/modulesecond.py'

func_list = []
is_function = False
for line in open(file, 'r').readlines():
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
    print(func['name'])
    str_body = func['body'].replace('\n', '')
    docstring = re.search(r'(\'{3}|\"{3}).+(\'{3}|\"{3})', str_body)
    if docstring is not None:
        func['docstring'] = ' '.join(docstring[0][3:-3].split())
    else:
        func['docstring'] = ''
    print(func['docstring'])
print(func_list)