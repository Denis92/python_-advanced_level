from socket import *
import json
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
s.bind((valid_arg(arg_pars['addr'], 'localhost'), (valid_arg(arg_pars['port'], 8888))))
s.listen(5)

with open('user.json', encoding='utf-8') as user_json:
    db_user_json = json.load(user_json)
print(db_user_json)


def resp_build(resp, alert):
    msg_dict = {
        "response": resp,
        "alert": alert
    }
    msg_json = json.dumps(msg_dict)
    print(msg_json)
    return client.send(msg_json.encode('utf-8'))


def valid_json_auth(auth_json):
    if all(['user' and 'time' in auth_json,
            'login' and 'pwd' in auth_json['user'],
            type(auth_json['time']) == float]):
        return True
    return False


def valid_json(client_json):
    dict_action = {'auth': valid_json_auth(client_json), 'msg': True}
    if 'action' in client_json:
        action = client_json['action']
        if action in dict_action:
            return dict_action[action]
    return False


def valid_auth(client_json, db_json):
    login = client_json['user']['login']
    pwd = client_json['user']['pwd']
    if all([login in db_json['user'], db_json['user'][login] == pwd]):
        return True
    else:
        return False


def valid_decor(valid_func):
    def decor(func):
        def wrapper(*args, **kwargs):
            print(valid_func)
            if valid_func:
                return func(*args, **kwargs)
            else:
                return resp_build(400, "BAD JSON")
        return wrapper
    return decor


while True:
    client, addr = s.accept()
    print(f'Получен запрос на соединение {addr}')
    bufsize = 100000024
    data_r = client.recv(bufsize)
    print(data_r)
    try:
        data_json = json.loads(data_r.decode('utf-8'))
    except Exception as e:
        print(e)
        resp_build(400, "BAD JSON")
        continue


    @valid_decor(valid_json(data_json))
    def auth_f(client_json, db_json):
        if valid_auth(client_json, db_json):
            resp_build(200, f"Hello, {client_json['user']['login']}")
        else:
            resp_build(402, 'Wrong login or password')


    auth_f(data_json, db_user_json)
    client.close()
