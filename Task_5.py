'''Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового
 в строковый тип на кириллице'''
import subprocess

args = ['ping', 'yandex.ru']
ping = subprocess.Popen(args, stdout=subprocess.PIPE)
for i in ping.stdout:
    print(i.decode('cp866'))
