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

    def test_capitalize_first_letter(self):
        err = "Only first letter should be capitalized"
        a = capitalize_first_letter("testA")
        self.assertEqual(a, "TestA", err)
        b = capitalize_first_letter("testInTheWaters")
        self.assertEqual(b, "TestInTheWaters", err)
    
    def test_lower_first_letter(self):
        err = "Only first letter should be lowered"
        a = lower_first_letter("TestA")
        self.assertEqual(a, "testA", err)
        b = lower_first_letter("TestInTheWaters")
        self.assertEqual(b, "testInTheWaters", err)
    
    def test_get_func_name(self):
        def func():
            return get_func_name()
        name = func()
        self.assertEqual(name, 'func', "Should return name of calling function")
    
    def test_get_file_name(self):
        name = get_file_name()
        self.assertEqual(
            name, 'test_helpers.py', "Should return name of enclosing file")

if __name__ == '__main__':
    unittest.main()
