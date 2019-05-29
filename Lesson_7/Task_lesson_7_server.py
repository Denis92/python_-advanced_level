
import json
import argparse
from Lesson_7.log.log_config import LogLevel
from socket import socket, AF_INET, SOCK_STREAM
import select
import threading


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


addr = valid_arg(arg_pars['addr'], 'localhost')
port = valid_arg(arg_pars['port'], 8888)


with open('user.json', encoding='utf-8') as user_json:
    db_user_json = json.load(user_json)


def resp_build(resp, alert):
    msg_dict = {
        "response": resp,
        "alert": alert
    }
    msg_json = json.dumps(msg_dict)
    return msg_json


def valid_json(client_json):
    dict_action = {'auth': valid_json_auth(client_json), 'msg': valid_json_msg(client_json)}
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
    if 'user' in auth_json and 'time' in auth_json:
        if all(['login' and 'pwd' in auth_json.get('user'),
                type(auth_json.get('time')) == float]):
            return True
    logg.error_log("JSON auth is not valid")
    return False


def valid_json_msg(msg_json):
    if all(['to' and 'time' and 'from' and 'message' in msg_json,
            type(msg_json.get('time')) == float]):
        return True
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

#Декоратор для валидации на будущее
# def valid_decor(valid_func):
#     def decor(func):
#         def wrapper(*args, **kwargs):
#             if valid_func:
#                 return func(*args, **kwargs)
#             else:
#                 return resp_build(400, "BAD JSON")
#         return wrapper
#     return decor


def new_sock(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(5)
    sock.settimeout(0.2)
    logg.info_log(f"Server start on addr = {addr} port = {port}")
    return sock


def write_client(msg_client, clients_w, all_clients):
    for i_cl in clients_w:
        str_cl = resp_build("200", f"{msg_client['from']} say: {msg_client['message']}")
        try:
            i_cl.send(str_cl.encode('utf-8'))
        except Exception as e:
            all_clients.remove(i_cl)
            logg.info_log(f"Client {i_cl} disconnect")


def read_client(clients_msg, clients_r, all_clients):
    for i_cl in clients_r:
        try:
            msg = i_cl.recv(1024)
            msg_recv = json.loads(msg.decode('utf-8'))
            if valid_json(msg_recv):
                if msg_recv.get("message") == "exit":
                    str_cl = resp_build("200", f"Your print 'exit'. Bye")
                    i_cl.send(str_cl.encode('utf-8'))
                    all_clients.remove(i_cl)
                    logg.info_log(f"Client {i_cl} disconnect")
                    continue
                clients_msg.append(msg_recv)
        except Exception as e:
            all_clients.remove(i_cl)
            print(f"Client {i_cl} disconnect")
    return clients_msg


def main_loop(addrr=addr, port=port):
    address = (addrr, port)
    clients = []
    clients_msg = []
    sock = new_sock(address)

    while True:
        try:
            conn, addr = sock.accept()
        except OSError as e:
            pass
        else:
            print(f"{addr}")
            clients.append(conn)
        finally:
            r = []
            w = []
            try:
                r, w, e = select.select(clients, clients, [], 0)
            except Exception as e:
                pass
            read_client(clients_msg, r, clients)
            for i_msg in clients_msg:
                write_client(i_msg, w, clients)
            clients_msg = []

print("Server start")
main_loop()
