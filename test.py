import re


file = 'modules/modulesecond.py'

func_list = []
is_function = False
for line in open(file, 'r').readlines():
    print(line)
    if re.search(r'^def \w+\(', line):
        print('Found ^dev')
        if is_function:
            print('Old func steel present, close')
            func_list.append(func_dict)
        print('Start new func')
        func_dict = {}
        f_name = re.search(r'def \w+\(', line)
        func_dict['name'] = f_name[0][3:-1]
        func_dict['body'] = line
        is_function = True
        continue
    if re.search(r'^    .+', line) and is_function:
        print('Its func body')
        func_dict['body'] += line
        continue
    if re.search(r'^\w.+', line) and is_function:
        print('Seems like end of prefious func, close')
        func_list.append(func_dict)
        is_function = False
        continue
if is_function:
    func_list.append(func_dict)
print(func_list)