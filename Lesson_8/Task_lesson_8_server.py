from socket import *
import json
import argparse
import time
from Lesson_8.log.log_config import LogLevel
import select


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
s.settimeout(0.2)
logg.info_log(f"Server start on addr = {addr} port = {port}")
s.listen(5)




def resp_build(resp, alert, client):
    msg_dict = {
        "response": resp,
        "alert": alert
    }
    msg_json = json.dumps(msg_dict)
    return client.send(msg_json.encode('utf-8'))


client_list = []
while True:
    try:
        client, addr = s.accept()
    except OSError as e:
        pass
    else:
        client_list.append(client)
        logg.info_log(f'Connection {client}, {time.time()}')
    finally:
        write_list = []
        try:
            read_list, write_list, expection_list = select.select([], client_list, [], 0)
        except Exception as e:
            pass
            # logg.warning_log(f'Disconnection')
        else:
            expected_customers = 2
            if len(write_list) == expected_customers:
                for i in range(len(write_list)):
                    try:
                        get_port = 1
                        timestr = f'{write_list[(len(write_list) - 1) - i].getpeername()[get_port]}'
                        write_list[i].send(timestr.encode('utf-8'))
                    except:
                        logg.warning_log(f'Disconnection {i}')
                        client_list.remove(write_list[i])
                        break
                for i in client_list:
                    i.close()
                    logg.info_log(f'Disconnection {i}')
                exit(0)
