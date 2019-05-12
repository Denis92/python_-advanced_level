from socket import *
import json
import argparse

parse = argparse.ArgumentParser()
parse.add_argument('-a', '--addr', action='store')
parse.add_argument('-p', '--port', action='store', type=int)
arg_pars = vars(parse.parse_args())

s = socket(AF_INET, SOCK_STREAM)
s.bind((arg_pars['addr'], arg_pars['port']))
s.listen(5)

def resp_build(resp, alert):
    msg_dict = {
        "response": resp,
        "alert": alert
    }
    msg_json = json.dumps(msg_dict)
    return client.send(msg_json.encode('utf-8'))

while True:
    client, addr = s.accept()
    print(f'Получен запрос на соединение {addr}')
    data_r = client.recv(1000024)
    try:
        data_json = json.loads(data_r.decode('utf-8'))
    except Exception as e:
        print(e)
        resp_build(400, "BAD JSON")

    if 'action' not in data_json:
        resp_build(400, "BAD JSON")
    elif 'auth' in data_json['action']:
        if 'Denis' in data_json['user']['login'] and '1234' in data_json['user']['pwd']:
            resp_build(200, "Hello, Denis")
        else:
            resp_build(402, 'Wrong login or password')
    client.close()