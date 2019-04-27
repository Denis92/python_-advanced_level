'''Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе'''
list_word = ['attribute', 'класс', 'функция', 'type']

for i in list_word:
    byte_i = i.encode()
    if str(byte_i).replace("b'", '').replace("'", '') == i:
        print(f'{i} - можно записать в байтовом типе')
    else:
        print(f'{i} - нельзя записать в байтовом типе')