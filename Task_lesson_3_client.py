from socket import *
import json
import time
import argparse

parse = argparse.ArgumentParser()
parse.add_argument('-a', '--addr', action='store')
parse.add_argument('-p', '--port', action='store', type=int)
arg_pars = vars(parse.parse_args())
s = socket(AF_INET, SOCK_STREAM)
s.connect((arg_pars['addr'], arg_pars['port']))
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
rd = s.recv(100000024)
s.close()
print(f'{json.loads(rd.decode("utf-8"))}')
