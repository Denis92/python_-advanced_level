import unittest


class TestValid(unittest.TestCase):
    def test_valid_json_auth(self):
        msg_dict = {
            "action": "auth",
            "time": 111111.111,
            "user": {
                "login": "Denis",
                "pwd": "1234"
            }
        }
        self.assertTrue(valid_json_auth(msg_dict))

    def test_valid_json(self):
        msg_dict = {
            "action": "auth",
            "time": 111111.111,
            "user": {
                "login": "Denis",
                "pwd": "1234"
            }
        }
        self.assertTrue(valid_json(msg_dict))

def valid_json_auth(auth_json):
    if all(['user' and 'time' in auth_json, 'login' and 'pwd' in auth_json['user'], type(auth_json['time']) == float]):
        return True
    return False


def valid_json(client_json):
    dict_action = {'auth': valid_json_auth(client_json), 'msg': True}
    if 'action' in client_json:
        action = client_json['action']
        if action in dict_action:
            return dict_action[action]
    return False

if __name__ == '__main__':
    unittest.main()

