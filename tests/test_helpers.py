"""Test Pyscaffold Helpers

Usage
    (env) python -m unittest tests.test_helpers
"""
import shutil
import unittest
from pathlib import Path, PurePath
from collections import OrderedDict
from pyscaffold.config import *
from pyscaffold.helpers import *


class TestHelpers(unittest.TestCase):
    def setUp(self):
        self.dummy_project = Path( PurePath(TESTS, 'Dummyproject') )

    def tearDown(self):
        if self.dummy_project.is_dir():
            shutil.rmtree(Path(self.dummy_project))
        pass

    def test_message(self):
        cases = OrderedDict({
            ("bread", "loaf"): "bread: loaf",
            ("bread", "loaf", "slice"): "bread: loaf: slice",
            ("bread", "loaf", "slice", "bite"): "bread: loaf: slice: bite",
            ("bread", "loaf", "slice", "bite", "crumb"): "bread: loaf: slice: bite: crumb"
        })
        for no, case in cases.items():
            self.assertEqual(message(*no), case)
        self.assertEqual(message("bread"), "bread")
          
    def test_error(self):
        a = f"{colors.BOLD}bread{colors.ENDC}: {colors.FAIL}loaf{colors.ENDC}"
        b = f"{colors.WARNING}slice{colors.ENDC}"
        c = f"{colors.WARNING}bite{colors.ENDC}"
        d = f"{colors.WARNING}crumb{colors.ENDC}"
        cases = OrderedDict({
            ("bread", "loaf"): a,
            ("bread", "loaf", "slice"): f"{a}: {b}",
            ("bread", "loaf", "slice", "bite"): f"{a}: {b}: {c}",
            ("bread", "loaf", "slice", "bite", "crumb"):  f"{a}: {b}: {c}: {d}"
        })
        for no, case in cases.items():
            self.assertEqual(error(no[0], *no[1:]), case)
   
    def test_delete_directory(self):
        deleteme = PurePath(Path().cwd(), 'tests', 'deleteme')
        Path(deleteme).mkdir()
        self.assertTrue(Path(deleteme).is_dir())
        delete_directory(deleteme)
        self.assertFalse(Path(deleteme).is_dir())
         
    def test_is_tool(self):
        existing_linux_tools = [
            'python',
            'cat'
        ]
        for tool in existing_linux_tools:
            self.assertTrue(is_tool(tool), f"{tool} not installed!")

    def test_project_root_exists(self):
        project = self.dummy_project
        self.dummy_project.mkdir(exist_ok=True)
        self.assertFalse(project_root_exists('Dummyproject', TESTS))
        Path(PurePath(project, 'setup.py')).touch()
        self.assertTrue(project_root_exists('Dummyproject', TESTS))
       
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
        self.assertTrue(_testme_)

    def test_conventional_naming(self):
        test_cases = [
            "CaMeLcAsE",
            "camelCase",
            "CamelCase",
            "CAMELcase",
            "camelCASE",
            "CAMELCASE",
            "camel_case"
        ]
        for s in test_cases:
            self.assertEqual(conventional_naming(s), "camelcase")
            self.assertEqual(conventional_naming(s, False), "Camelcase")

    def test_get_file_name(self):
        name = get_file_name()
        self.assertEqual(
            name, 'test_helpers.py', "Should return name of enclosing file")
    
    def test_get_func_name(self):
        def func():
            return get_func_name()
        name = func()
        self.assertEqual(name, 'func', "Should return name of calling function")    


if __name__ == '__main__':
    unittest.main()
