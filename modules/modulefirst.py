# coding=utf8
def sort_func_first(js_dict):
    '''Преобразует входящий словарь.
    Сортирует версии из поля ident.
    Меняет value из строки на массив из слов.
    '''
    err_list = []
    for key in js_dict['data'].items():
        err_list.append(key)
    err_list.sort(key=lambda s: [int(u) for u in s[1]['ident'].split('.')])
    data_dict = {}
    for i in err_list:
        data_dict[i[0]] = i[1]
        value_str = data_dict[i[0]]['value']
        # Remove extra spaces
        value_str = value_str.strip()
        # Make list by spaces
        value_list = value_str.split()
        data_dict[i[0]]['value'] = value_list
    js_dict['data'] = data_dict
    return js_dict