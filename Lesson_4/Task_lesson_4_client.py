from socket import *
import json
import time
import argparse

parse = argparse.ArgumentParser()
parse.add_argument('-a', '--addr', action='store')
parse.add_argument('-p', '--port', action='store', type=int)
arg_pars = vars(parse.parse_args())

def valid_arg(arg, default_arg):
    if arg == None:
        return default_arg
    else:
        return arg

s = socket(AF_INET, SOCK_STREAM)
s.connect((valid_arg(arg_pars['addr'], 'localhost'), (valid_arg(arg_pars['port'], 8888))))
login = 'Denis'
msg_dict = {
    "action": "auth",
    "time": time.time(),
    "user": {
        "login": "Denis",
        "pwd": "1234"
    }
}
msg_json = json.dumps(msg_dict)
s.send(msg_json.encode('utf-8'))

bufsize = 100000024
rd = s.recv(bufsize)
s.close()
print(f'{json.loads(rd.decode("utf-8"))}')
