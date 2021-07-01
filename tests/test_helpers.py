"""Test Pyscaffold Helpers

Usage
   python -m unittest tests.test_helpers
"""
import unittest
from pyscaffold.helpers import *


class TestHelpers(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_func_name(self):
        def func():
            return get_func_name()
        name = func()
        self.assertEqual(name, 'func', "Should return name of calling function")
    
    def test_get_file_name(self):
        name = get_file_name()
        self.assertEqual(
            name, 'test_helpers.py', "Should return name of enclosing file")

    def test_is_camel_case(self):
        test = is_camel_case('test')
        testme = is_camel_case('testme')
        TestMe = is_camel_case('TestMe')
        testMe = is_camel_case('testMe')
        TESTME = is_camel_case('TESTME')
        TESTme = is_camel_case('TESTme')
        test_me = is_camel_case('test_me')

        self.assertFalse(test)
        self.assertFalse(testme)
        self.assertTrue(TestMe)
        self.assertTrue(testMe)
        self.assertFalse(TESTME)
        self.assertTrue(TESTme)
        self.assertFalse(test_me)

    def test_contains_hyphen(self):
        test = contains_hyphen('test')
        test_me = contains_hyphen('test_me')
        _testme = contains_hyphen('_testme')
        _testme_ = contains_hyphen('_testme_')

        self.assertFalse(test)
        self.assertTrue(test_me)     
        self.assertTrue(_testme)
        self.assertTrue(_testme)

    def conventional_naming(self):
        test_cases = [
            "CaMeLcAsE"
            "camelCase",
            "CamelCase",
            "CAMELcase",
            "camelCASE",
            "CAMELCASE",
            "camel_case"
        ]
        for s in test_cases:
            self.assertEqual(conventional_naming(test_cases[s]), "camelcase")
            self.assertEqual(conventional_naming(test_cases[s], False), "Camelcase")


if __name__ == '__main__':
    unittest.main()
