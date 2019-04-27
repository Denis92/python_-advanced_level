'''Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в байтовое
 и выполнить обратное преобразование (используя методы encode и decode)'''

list_word = ['разработка', 'администрирование', 'protocol', 'standard']
list_word_b = [i.encode() for i in list_word]
print(f'Байтовое представление {list_word_b}')
list_word_s = [i.decode() for i in list_word_b]
print(f'Строковое представление {list_word_s}')