from socket import *
import json
import time
import argparse
from Lesson_7.log.log_config import LogLevel
from threading import Thread

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


def get_customer_information():
    s = socket(AF_INET, SOCK_STREAM)
    addr = valid_arg(arg_pars['addr'], 'localhost')
    port = valid_arg(arg_pars['port'], 8888)

    try:
        s.connect((addr, port))
        logg.info_log(s.getsockname())
    except ConnectionError as e:
        logg.error_log("No response from server")
        exit()
    buf_size = 1024
    rd = s.recv(buf_size)
    logg.debug_log(f'JSON from servev {(rd.decode("ascii"))}')
    port = 1
    port_serv = s.getsockname()[port]
    s.close()
    port_cl = int(rd.decode("ascii"))
    customer_information = ("localhost", port_serv, port_cl)
    return customer_information


addr, port_serv, port_cl = get_customer_information()


def server_run(addr=addr, port=port_serv):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((addr, port))
    logg.info_log(f"Server start on addr = {addr} port = {port}")
    sock.listen(5)
    try:
        client, addr = sock.accept()
        logg.info_log(f'Connection {client}, {time.time()}')
    except Exception as e:
        pass
    while True:
        msg_cl = input("")
        client.send(msg_cl.encode("utf-8"))


def client_run(addr=addr, port=port_cl):
    s = socket(AF_INET, SOCK_STREAM)
    try:
        s.connect((addr, port))
        logg.info_log(s.getsockname())
    except ConnectionError as e:
        logg.error_log("No response from server")
    while True:
        buf_size = 1024
        rd = s.recv(buf_size)
        logg.info_log(f"127.0.0.1:{port_cl} say: {rd.decode('utf-8')}")


if __name__ == '__main__':
    t1 = Thread(target=server_run)
    t2 = Thread(target=client_run)

    t1.start()
    t2.start()

    t1.join()
    t2.join()