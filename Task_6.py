'''Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
 Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое.'''

list_word = ['сетевое программирование\n', 'сокет\n', 'декоратор\n']
file_name = 'test_file.txt'
file_cr = open(file_name,  mode='w')
for i in list_word:
    file_cr.write(i)
file_cr.close()
print(file_cr)
try:
    with open(file_name, encoding='utf-8') as file_r:
        for line in file_r:
            print(line)
except UnicodeDecodeError:
    print("utf-8' codec can't decode")