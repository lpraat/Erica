import unittest


class TestErica(unittest.TestCase):
    def test_foo(self):
        code_red = 500
        self.assertEqual(500, code_red)