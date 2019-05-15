import unittest
import json

class TestValid(unittest.TestCase):

    def test_valid_auth(self):
        msg_dict = {
            "action": "auth",
            "time": 111111.111,
            "user": {
                "login": "Denis",
                "pwd": "1234"
            }
        }
        with open('user.json', encoding='utf-8') as user_json:
            db_user_json = json.load(user_json)
        self.assertTrue(valid_auth(msg_dict, db_user_json))

def valid_auth(client_json, db_json):
    login = client_json['user']['login']
    pwd = client_json['user']['pwd']
    if all([login in db_json['user'], db_json['user'][login] == pwd]):
        return True
    else:
        return False

if __name__ == '__main__':

    unittest.main()