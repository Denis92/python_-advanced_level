import unittest


class TestValidArg(unittest.TestCase):
    def test_input_arg_none(self):
        self.assertEqual(valid_arg(None, 'localhost'), 'localhost')

    def test_input_arg(self):
        self.assertEqual(valid_arg('127.0.0.1', 'localhost'), '127.0.0.1')

    def test_input_arg_neq(self):
        self.assertNotEqual(valid_arg('127.0.0.1', 'localhost'), 'localhost')

    def test_input_arg_p(self):
        self.assertEqual(valid_arg(9999, 7777), 9999)

    def test_input_arg_pn(self):
        self.assertEqual(valid_arg(None, 7777), 7777)

def valid_arg(arg, default_arg):
    if arg == None:
        return default_arg
    else:
        return arg

if __name__ == '__main__':
    unittest.main()