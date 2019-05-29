from socket import *
import json
import time
import argparse
from log.log_config import LogLevel


logg = LogLevel(file_name="config_client_logg.ini", rotate_on=False)
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
addr = valid_arg(arg_pars['addr'], 'localhost')
port = valid_arg(arg_pars['port'], 8888)

try:
    s.connect((addr, port))
except ConnectionError as e:
    logg.error_log("No response from server")
    exit(1)

logg.debug_log(f"Client connect address = {addr} port = {port}")
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
logg.debug_log(f"Send JSON to server {msg_json}")
bufsize = 100000024
rd = s.recv(bufsize)
s.close()
logg.debug_log(f'JSON from servev {json.loads(rd.decode("utf-8"))}')
