import unittest
from str_srch import searcher

class test_searcher(unittest.TestCase):

    mp_compares = {
        'input': ['2', 'd23', 'Sizix', 'qw', 'fd'],
        'output': {
            'files': ['first.txt', 'second.txt', 'third.txt'],
            'matches': [['2', 'fd', 'qw'], ['2', 'd23', 'fd'], ['Sizix', 'fd']]
        }
    }

    test_path = 'C:/Users/V/PycharmProjects/str_srch/tests/srch_dir/'

    def test_matchP(self):
        self.assertEqual(searcher.matchP(self.mp_compares['input'], self.test_path), self.mp_compares['output'])