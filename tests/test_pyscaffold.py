"""Test Pyscaffold

Usage
   python -m unittest tests.test_pyscaffold
"""
import shutil
import argparse
import unittest
from pathlib import Path, PurePath
from pyscaffold.pyscaffold import *
from pyscaffold.helpers import *
from pyscaffold.fragments import *


class TestPyscaffold(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.projects_folder = '/home/engineer/source/python/projects'
        self.project_dest = PurePath(self.projects_folder, 'Deleteme')
        self.directories = ['bin', 'docs', 'data', 'tests', 'deleteme']
        self.files = ['README.md', 'LICENSE', '.gitignore', 'setup.py']

        self.file_create_error = "File not created"
        self.file_content_error = "Invalid file contents"
        self.dir_create_error = "Directory not created"
        self.dir_content_error = "Directory content mismatch"
        
        self.base_path = Path.cwd()
        self.data = PurePath(self.base_path, 'data')
        self.tests = PurePath(self.base_path, 'tests')
        self.test_output = PurePath(self.tests, 'test_output')
        self.test_project = PurePath(self.test_output, 'Deleteme')
        self.env = PurePath(self.test_project, 'env')
        
        self.args = argparse.Namespace()
        self.args.classic = False
        self.args.commands = ['start', 'deletemeA']
        self.args.destination = None

        self.content_innerpkg_helper = (
            "\"\"\"Deleteme Helpers\n"
            "\n"
            "This module contains the helper function definitions for the Deleteme program.\n"
            "\"\"\"\n"
        )

        self.content_innerpkg_main = (
            "\"\"\"Deleteme Main\n"
            "\n"
            "This module contains the entry point code for the Deleteme program.\n"
            "\"\"\"\n"
            "\n"
            "from deleteme.deleteme import main\n"
            "\n"
            "\n"
            "if __name__ == '__main__':\n"
            "    main()"
        )

        self.content_inner_module = (
            "\"\"\"Deleteme\n"
            "\n"
            "This module contains the main function definitions for the Deleteme program.\n"
            "\"\"\"\n"
            "from deleteme.helpers import *\n"
            "\n"
            "def main():\n"
            "    my_parser = argparse.ArgumentParser(\n"
            "        prog='deleteme',\n"
            "        fromfile_prefix_chars='@',\n"
            "        usage='deleteme [options] <command> <arg1>',\n"
            "        description='<desc>',\n"
            "        epilog='Build it!')\n"
            "\n"
            "    # Add arguments here\n"
            "\n"
            "    my_parser.add_argument('-d', '--detail',\n"
            "                           action='store',\n"
            "                           type=str,\n"
            "                           required=False,\n"
            "                           help='modifies something')\n"
            "    my_parser.add_argument('commands',\n"
            "                           nargs='+',\n"
            "                           help=\"use a command eg. init or start\")\n"
            "\n"
            "    args = my_parser.parse_args()\n"
        )

        self.content_test_deleteme = (
            "\"\"\"Test Deleteme\n"
            "\n"
            "This module contains the test case for the Deleteme program.\n"
            "\"\"\"\n"
            "import unittest"
            "\n"
            "from deleteme.helpers import *\n"
            "from deleteme.deleteme import *\n"
            "\n"
            "\n"
            "class DeletemeTest(unittest.TestCase):\n"
            "   def setUp(self):\n"
            "        pass\n"
            "\n"
            "def tearDown(self):\n"
            "    pass\n"
            "\n"
            "if __name__ == '__main__':\n"
            "    unittest.main()"
        )

        self.content_test_helpers = (
            "\"\"\"Deleteme Test Helpers\n"
            "\n"
            "This module contains the test case for the Deleteme helpers module.\n"
            "\"\"\"\n"
            "import unittest\n"
            "\n"
            "class DeletemeHelpersTest(unittest.TestCase):\n"
            "    def setUp(self):\n"
            "        pass\n"
            "\n"
            "\n"
            "    def tearDown(self):\n"
            "        pass\n"
            "\n"
            "\n"
            "if __name__ == '__main__':\n"
            "   unittest.main()"
        )

        self.content_setup_py = (
            "\"\"\"Deleteme Setup\n"
            "\n"
            "This module contains the setuptools.setup() definition for the Deleteme program.\n"
            "\"\"\"\n"
            "\n"
            "from setuptools import setup, find_packages\n"
            "\n"
            "with open('README.md', 'r') as fh:\n"
            "    long_description=fh.read()\n"
            "\n"
            "setup(\n"
            "    name='Deleteme',\n"
            "    version='1.0.0',\n"
            "    author='Emille Giddings',\n"
            "    author_email='emilledigital@gmail.com',\n"
            "    description='<enter description here>',\n"
            "    long_description=long_description,\n"
            "    long_description_content_type='text/markdown',\n"
            "    url='',\n"
            "    packages=find_packages(include=['']),\n"
            "    package_data={'': ['', '']},\n"
            "    entry_points={\n"
            "        'console_scripts': ['deleteme=deleteme.__main__:main']\n"
            "    },\n"
            "    tests_require=[''],\n"
            "    classifiers=[\n"
            "        'Programming Language :: Python :: 3',\n"
            "        'License :: OSI Approved :: MIT License',\n"
            "        'Operating System :: OS Independent',\n"
            "    ],\n"
            "    python_requires='>=3.6'\n"
            ")"
        )

        try:
            Path(self.test_output).mkdir()
        except Exception as e:
            print(e)

        try:
            Path(self.test_project).mkdir()
        except Exception as e:
            print(e)

        try:
            Path(self.project_dest).mkdir()
        except Exception as e:
            print(e)

    def tearDown(self):
        if Path(self.test_output).is_dir():
            # Path(self.dest).rmdir()
            shutil.rmtree(Path(self.test_output))

        if Path(self.project_dest).is_dir():
            # Path(self.dest).rmdir()
            shutil.rmtree(Path(self.project_dest))
    
    def test_create_project_root(self):
        dummy_proj = PurePath(self.test_output, 'DummyProj')
        create_project_root(dummy_proj)
        self.assertTrue(Path(dummy_proj).is_dir(), 'Project root not created')

    def test_create_innerpkg(self):
        create_innerpkg(self.test_project, 'deleteme')
        innerpkg = PurePath(self.test_project, 'deleteme')
        init_py = PurePath(innerpkg, '__init__.py')
        self.assertTrue(Path(innerpkg).is_dir(), self.dir_create_error)
        self.assertTrue(Path(init_py).is_file(), self.file_create_error)

    def test_load_project(self):
        load_project(self.test_project, 'deleteme')
        directories = [_.name for _ in Path(
            self.test_project).iterdir() if _.is_dir()]
        files = [_.name for _ in Path(
            self.test_project).iterdir() if _.is_file()]
        self.assertEqual(set(directories), set(
            self.directories), self.dir_content_error)
        self.assertEqual(set(files), set(self.files), self.dir_content_error)

    def test_insert_init_py(self):
        insert_init_py(self.test_project)
        init_py = PurePath(self.test_project, '__init__.py')
        self.assertTrue(Path(init_py).is_file(), self.file_create_error)

    def test_load_boilerplate_innerpkg_main(self):
        innerpkg_main = PurePath(self.test_project, '__main__.py')
        load_boilerplate_innerpkg_main(innerpkg_main, 'deleteme')
        content = return_file_content_as_string(Path(innerpkg_main))
        self.assertTrue(Path(innerpkg_main).is_file(),
                        self.file_create_error)
        self.assertEqual(content, self.content_innerpkg_main,
                         self.file_content_error)

    def test_load_boilerplate_innerpkg_helper(self):
        innerpkg_helper = PurePath(self.test_project, 'helpers.py')
        load_boilerplate_innerpkg_helper(innerpkg_helper, 'deleteme')
        content = return_file_content_as_string(Path(innerpkg_helper))
        self.assertTrue(Path(innerpkg_helper).is_file(),
                        self.file_create_error)
        self.assertEqual(content, self.content_innerpkg_helper,
                         self.file_content_error)

    def test_load_boilerplate_innermodule(self):
        innermodule = PurePath(self.test_output, 'deleteme.py')
        load_boilerplate_innermodule(innermodule, 'deleteme')
        content = return_file_content_as_string(Path(innermodule))
        self.assertTrue(Path(innermodule).is_file(),
                        self.file_create_error)
        self.assertEqual(content, self.content_inner_module,
                         self.file_content_error)

    def test_load_boilerplate_test_helpers(self):
        test_pkg = PurePath(self.test_project, 'tests')
        Path(test_pkg).mkdir()
        test_helpers = PurePath(test_pkg, 'test_helpers.py')
        load_boilerplate_test_helpers(test_helpers, 'deleteme')
        content = return_file_content_as_string(Path(test_helpers))
        self.assertTrue(Path(test_helpers).is_file(),
                        self.file_create_error)
        self.assertEqual(content, self.content_test_helpers,
                         self.file_content_error)

    def test_load_boilerplate_test_innerpkg(self):
        test_pkg = PurePath(self.test_project, 'tests')
        Path(test_pkg).mkdir()
        test_innerpkg = PurePath(test_pkg, 'test_deleteme.py')        
        load_boilerplate_test_innerpkg(test_innerpkg, 'deleteme')
        content = return_file_content_as_string(Path(test_innerpkg))
        self.assertTrue(Path(test_innerpkg).is_file(),
                        self.file_create_error)
        self.assertEqual(content, self.content_test_deleteme,
                         self.file_content_error)

    def test_load_boilerplate_setup(self):
        setup_py = PurePath(self.test_project, 'setup.py')
        load_boilerplate_setup(setup_py, 'deleteme')
        self.assertTrue(Path(setup_py).is_file(), self.file_create_error)
        contents = return_file_content_as_string(Path(setup_py))
        self.assertEqual(contents, self.content_setup_py,
                         self.file_content_error)

    def test_load_boilerplate_readme(self):
        readme = PurePath(self.test_project, 'README.md')
        load_boilerplate_readme(readme, 'deleteme')
        self.assertTrue(Path(readme).is_file(), self.file_create_error)

    def test_copy_license(self):
        copy_license(self.data, self.test_project)
        lic = PurePath(self.test_project, 'LICENSE')
        self.assertTrue(Path(lic).is_file(), self.file_create_error)

    def test_copy_gitignore(self):
        copy_gitignore(self.data, self.test_project)
        gitignore = PurePath(self.test_project, '.gitignore')
        self.assertTrue(Path(gitignore).is_file(), self.file_create_error)

    def test_deploy_virtual_env(self):
        deploy_virtual_environment(self.project_dest, 'env')
        env = PurePath(self.project_dest, 'env')
        contents = [_.name for _ in Path(env).iterdir() if _.is_dir()]
        self.assertEqual(set(contents), set(['bin', 'include', 'lib']))

if __name__ == '__main__':
    unittest.main()
