from socket import *
import json
import argparse
from Lesson_5.log.log_config import LogLevel


logg = LogLevel(file_name="config_server_logg.ini", rotate_on=True)
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
s.bind((addr, port))
logg.info_log(f"Server start on addr = {addr} port = {port}")
s.listen(5)

with open('user.json', encoding='utf-8') as user_json:
    db_user_json = json.load(user_json)


def resp_build(resp, alert):
    msg_dict = {
        "response": resp,
        "alert": alert
    }
    msg_json = json.dumps(msg_dict)
    return client.send(msg_json.encode('utf-8'))

def valid_json(client_json):
    dict_action = {'auth': valid_json_auth(client_json), 'msg': True}
    if 'action' in client_json:
        action = client_json['action']
        if action in dict_action:
            logg.debug_log("JSON is valid")
            return dict_action[action]
        logg.error_log(f"action fail: action = {action}")
    else:
        logg.error_log(f"Action fail")
        return False


def valid_json_auth(auth_json):
    if all(['user' and 'time' in auth_json,
            'login' and 'pwd' in auth_json['user'],
            type(auth_json['time']) == float]):
        return True
    logg.error_log("JSON auth is not valid")
    return False


def valid_auth(client_json, db_json):
    login = client_json['user']['login']
    pwd = client_json['user']['pwd']
    if login in db_json['user']:
        if db_json['user'][login] == pwd:
            logg.debug_log(f"valid auth {client_json}")
            return True
    else:
        logg.error_log(f"Auth is not valid {client_json}")
        return False


def valid_decor(valid_func):
    def decor(func):
        def wrapper(*args, **kwargs):
            if valid_func:
                return func(*args, **kwargs)
            else:
                return resp_build(400, "BAD JSON")
        return wrapper
    return decor


while True:
    client, addr = s.accept()
    logg.info_log(f'Connection request received {addr}')
    bufsize = 100000024
    data_r = client.recv(bufsize)
    try:
        data_json = json.loads(data_r.decode('utf-8'))
        logg.debug_log("GOOD JSON")
    except Exception as e:
        print(e)
        logg.error_log("BAD JSON")
        resp_build(400, "BAD JSON")
        continue


    @valid_decor(valid_json(data_json))
    def auth_f(client_json, db_json):
        if valid_auth(client_json, db_json):
            logg.debug_log(f"Send to client: Hello, {client_json['user']['login']}")
            resp_build(200, f"Hello, {client_json['user']['login']}")
        else:
            logg.error_log("Wrong login or password")
            resp_build(402, 'Wrong login or password')


    auth_f(data_json, db_user_json)
    client.close()
