import json
import time
import argparse
from Lesson_7.log.log_config import LogLevel
from socket import socket, AF_INET, SOCK_STREAM
import threading

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

addr = valid_arg(arg_pars['addr'], 'localhost')
port = valid_arg(arg_pars['port'], 8888)

login = 'Denis'
msg_login_dict = {
    "action": "auth",
    "time": time.time(),
    "user": {
        "login": "Denis",
        "pwd": "1234"
    }
}
def creat_msg(name, message):
    msg_dict = {
        "action": "msg",
        "time": time.time(),
        "to": "#room_name",
        "from": name,
        "message": message
    }
    msg_json = json.dumps(msg_dict)
    return msg_json


def valid_server_json(server_json):
    if all(["response" and "alert" in server_json]):
        if server_json.get("response") == "200":
            return True
    else:
        return False


def send_msg(sock, name):
    while True:
        try:
            str_cl = input("")
            sock.send(creat_msg(name, str_cl).encode("utf-8"))
        except Exception as e:
            print("Except")
            pass


def read_msg(sock):
    while True:
        try:
            msg = sock.recv(1024)
            msg_recv = json.loads(msg.decode('utf-8'))
            if valid_server_json(msg_recv):
                print(f"{msg_recv['alert']}")
        except Exception as e:
            pass

if __name__ == '__main__':
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect((addr, port))
        name = input("Input your name: ")
        t2 = threading.Thread(target=send_msg, args=(sock, name))
        t1 = threading.Thread(target=read_msg, args=(sock,))
        t1.daemon = True
        t2.daemon = True
        t1.start()
        t2.start()

        print(threading.active_count())

        t1.join()
        t2.join()
