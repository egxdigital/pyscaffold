"""Fragments

This module contains format strings used to load boilerplate code in the Pyscaffold program.
"""

pyscaffold_ascii = '\033[36m'  + r"""
                                         ___    ___      ___       __     
                                       /'___\ /'___\    /\_ \     /\ \    
 _____   __  __    ____   ___     __  /\ \__//\ \__/  __\//\ \    \_\ \   
/\ '__`\/\ \/\ \  /',__\ /'___\ /'__`\\ \ ,__\ \ ,__\/ __`\ \ \   /'_` \  
\ \ \L\ \ \ \_\ \/\__, `/\ \__//\ \L\.\\ \ \_/\ \ \_/\ \L\ \_\ \_/\ \L\ \ 
 \ \ ,__/\/`____ \/\____\ \____\ \__/.\_\ \_\  \ \_\\ \____/\____\ \___,_\
  \ \ \/  `/___/> \/___/ \/____/\/__/\/_/\/_/   \/_/ \/___/\/____/\/__,_ /
   \ \_\     /\___/                                                       
    \/_/     \/__/""" + '\033[0m'


setup_py = (
    "\"\"\"{Project} Setup\n"
    "\n"
    "This module contains the setuptools.setup() definition for the {Project} program.\n"
    "\"\"\"\n"
    "\n"
    "from setuptools import setup, find_packages\n"
    "\n"
    "with open('README.md', 'r') as fh:\n"
    "    long_description=fh.read()\n"
    "\n"
    "setup(\n"
    "    name='{Project}',\n"
    "    version='1.0.0',\n"
    "    author='Emille Giddings',\n"
    "    author_email='emilledigital@gmail.com',\n"
    "    description='<enter description here>',\n"
    "    long_description=long_description,\n"
    "    long_description_content_type='text/markdown',\n"
    "    url='',\n"
    "    packages=find_packages(include=['']),\n"
    "    package_data={{'': ['', '']}},\n"
    "    entry_points={{\n"
    "        'console_scripts': ['{project}={project}.__main__:main']\n"
    "    }},\n"
    "    tests_require=[''],\n"
    "    classifiers=[\n"
    "        'Programming Language :: Python :: 3',\n"
    "        'License :: OSI Approved :: MIT License',\n"
    "        'Operating System :: OS Independent',\n"
    "    ],\n"
    "    python_requires='>=3.6'\n"
    ")"
)

readme_md = (
    "# {project}"
)

innerpkg_main_py = (
    "\"\"\"{Project} Main\n"
    "\n"
    "This module contains the entry point code for the {Project} program.\n"
    "\"\"\"\n"
    "\n"
    "from {project}.{project} import main\n"
    "\n"
    "\n"
    "if __name__ == '__main__':\n"
    "    main()"
)

innermodule_py = (
    "\"\"\"{Project}\n"
    "\n"
    "This module contains the main function definitions for the {Project} program.\n"
    "\"\"\"\n"
    "from {project}.helpers import *\n"
    "\n"
    "def main():\n"
    "    my_parser = argparse.ArgumentParser(\n"
    "        prog='{project}',\n"
    "        fromfile_prefix_chars='@',\n"
    "        usage='{project} [options] <command> <arg1>',\n"
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

innerpkg_helper_py = (
    "\"\"\"{Project} Helpers\n"
    "\n"
    "This module contains the helper function definitions for the {Project} program.\n"
    "\"\"\"\n"
)

test_helpers_py = (
    "\"\"\"{Project} Test Helpers\n"
    "\n"
    "This module contains the test case for the {Project} helpers module.\n"
    "\"\"\"\n"
    "import unittest\n"
    "\n"
    "class {Project}HelpersTest(unittest.TestCase):\n"
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

test_project_py = (
    "\"\"\"Test {Project}\n"
    "\n"
    "This module contains the test case for the {Project} program.\n"
    "\"\"\"\n"
    "import unittest"
    "\n"
    "from {project}.helpers import *\n"
    "from {project}.{project} import *\n"
    "\n"
    "\n"
    "class {Project}Test(unittest.TestCase):\n"
    "   def setUp(self):\n"
    "        pass\n"
    "\n"
    "def tearDown(self):\n"
    "    pass\n"
    "\n"
    "if __name__ == '__main__':\n"
    "    unittest.main()"
)