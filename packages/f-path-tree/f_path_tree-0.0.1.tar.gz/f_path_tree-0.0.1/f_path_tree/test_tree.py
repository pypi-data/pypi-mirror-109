import libtree
import unittest
import sys
from libtree import tree

log_tests = open('log_tests.txt', 'w+', encoding='utf-8')
expected = open('expected.txt', 'r', encoding='utf-8')

class TestTree(unittest.TestCase):

    sys.stdout = open('log_tests.txt', 'w+', encoding='utf-8')
    direct = r'C:\Windows\winhlp32.exe'
    tree(direct)
    sys.stdout.close()

    def test_tree(self):
        self.assertEqual(log_tests.read(), expected.read())
        log_tests.close()
        expected.close()
