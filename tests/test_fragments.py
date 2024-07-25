"""
Test Fragments

This module contains tests for the format strings used by the Pyscaffold program.

"""
import pytest
from pyscaffold import fragments

@pytest.fixture(scope='function')
def setup():
    """
    Sets up two variables for use throughout the fragment tests.

    Returns:
        _Tuple_: a Tuple containing the project name and package name
    """
    project_name = "TestProject"
    package_name = "test_project"
    return project_name, package_name

def test_pkg_config_py(setup):
    """
    Tests pkg_config_py
    """
    project_name, package_name = setup

    expected = (
        "\"\"\"\n"
        "TestProject Config\n"
        "\n"
        "This module contains configuration definitions for the TestProject application.\n"
        "\n"
        "\"\"\"\n"
        "import yaml\n"
        "from pathlib import Path\n"
        "\n"
        "class colors():\n"
        "    HEADER     = '\\033[95m'\n"
        "    OKBLUE     = '\\033[94m'\n"
        "    OKCYAN     = '\\033[96m'\n"
        "    OKGREEN    = '\\033[92m'\n"
        "    WARNING    = '\\033[93m'\n"
        "    FAIL       = '\\033[91m'\n"
        "    ENDC       = '\\033[0m'\n"
        "    BOLD       = '\\033[1m'\n"
        "    UNDERLINE  = '\\033[4m'\n"
        "\n"    
        "class Config():\n"
        "    def __init__(self, config_path=None):\n"
        "        self.settings = {}\n"
        "        if config_path is None:\n"
        "            config_path = Path(__file__).resolve().parent.parent / 'config.yaml'\n"
        "        self.load_from_file(config_path)\n"
        "\n"
        "    def load_from_file(self, config_path):\n"
        "        \"\"\"\n"
        "        Load configuration settings from a YAML file.\n"
                
        "        Args:\n"
        "            config_path (str): Path to the YAML configuration file.\n"
        "        \"\"\"\n"
        "        with open(config_path, 'r') as file:\n"
        "            self.settings = yaml.safe_load(file)\n"
        "\n"
        "    def get(self, key, default=None):\n"
        "        \"\"\"\n"
        "        Retrieve a configuration value by its key.\n"
        "\n"            
        "        Args:\n"
        "            key (str): The key to look up in the configuration.\n"
        "            default: The default value to return if the key is not found.\n"
        "\n"            
        "        Returns:\n"
        "            The value associated with the key, or the default value.\n"
        "        \"\"\"\n"
        "        keys = key.split('.')\n"
        "        value = self.settings\n"
        "        for k in keys:\n"
        "            if isinstance(value, dict):\n"
        "                value = value.get(k, default)\n"
        "            else:\n"
        "                return default\n"
        "        return value\n"
        "\n"
        "    def add_setting(self, name, **kwargs):\n"
        "        \"\"\"\n"
        "        Add a new setting to the configuration.\n"
        "\n"            
        "        Args:\n"
        "            name (str): The name of the new setting.\n"
        "            kwargs: The key-value pairs for the new setting.\n"
        "\n"            
        "        Returns:\n"
        "            self\n"
        "        \"\"\"\n"
        "        self.settings[name] = kwargs\n"
        "        return self\n"
        "\n"
        "    def update_setting(self, name, **kwargs):\n"
        "        \"\"\"\n"
        "        Update an existing setting in the configuration.\n"
        "\n"            
        "        Args:\n"
        "            name (str): The name of the setting to update.\n"
        "            kwargs: The key-value pairs to update the setting with.\n"
        "\n"            
        "        Returns:\n"
        "            self\n"
        "        \"\"\"\n"
        "        if name in self.settings:\n"
        "            self.settings[name].update(kwargs)\n"
        "        else:\n"
        "            self.settings[name] = kwargs\n"
        "        return self\n"
        "\n"
        "    def display(self):\n"
        "        \"\"\"\n"
        "        Display all configuration settings.\n"
        "        \"\"\"\n"
        "        from pprint import pprint\n"
        "        pprint(self.settings)\n"
        "\n"
        "    def get_tests_directory_path(self, abs=False) -> Path:\n"   
        "        \"\"\"\n"
        "        Retrieve the path to the test projects directory.\n"
        "\n"
        "        Args:\n"
        "            abs (bool): If True, returns the absolute path.\n"
        "\n"
        "        Returns:\n"
        "            Path: The resolved test projects directory pathname.\n"
        "\n"            
        "        Raises:\n"
        "            ValueError: If the resolved path does not exist.\n"
        "        \"\"\"\n"
        "        path = Path(self.get('settings.DUMMY_DIR'))\n"
        "        if abs:\n"
        "            path = Path(__file__).resolve().parent.parent / path\n"
        "\n"            
        "        if not path.exists():\n"
        "            raise ValueError('Tests directory does not exist.')\n"
        "\n"            
        "        return path\n"
    )

    result = fragments.PKG_CONFIG_PY.format(
        packagename = package_name,
        ProjectName = project_name
    )

    assert result == expected

def test_pkg_helpers_py(setup):
    """
    Tests pkg_helpers_py
    """
    project_name, package_name = setup

    expected = (
        "\"\"\"\n"
        "TestProject Helpers\n"
        "\n"
        "This module contains helper function definitions for the TestProject application.\n"
        "\"\"\"\n"
    )

    result = fragments.PKG_HELPERS_PY.format(
        packagename = package_name,
        ProjectName = project_name
    )

    assert result == expected

def test_pkg_utils_py(setup):
    """
    Tests pkg_utils_py
    """
    project_name, package_name = setup

    expected = (
        "\"\"\"\n"
        "TestProject Utilities\n"
        "\n"
        "This module contains utility function definitions for the TestProject application.\n"
        "\n"
        "\"\"\"\n"
        "import argparse\n"
        "\n"
        "def do_something(args: argparse.Namespace):\n"
        "    return args\n"
        "\n"
        "def do_something_else(args: argparse.Namespace):\n"
        "    return args\n"
        "\n"
        "def do_another_thing(args: argparse.Namespace):\n"
        "    return args\n"
        "\n"
        "def preprocess_arguments(args: argparse.Namespace) -> None:\n"
        "    do_something(args)\n"
        "    do_something_else(args)\n"
        "    do_another_thing(args)\n"
        "\n"
    )

    result = fragments.PKG_UTILS_PY.format(
        packagename = package_name,
        ProjectName = project_name
    )

    assert result == expected

def test_pkg_module_py(setup):
    """
    Tests pkg_module_py
    """
    project_name, package_name = setup

    expected = (
        "\"\"\"\n"
        "TestProject\n"
        "\n"
        "This module contains the class definition for the TestProject class.\n"
        "\n"
        "\"\"\"\n"
        "class TestProject():\n"
        "    @staticmethod\n"
        "    def subcommand1(*args, **kwargs):\n"
        "        print('In test_project -> args: ', args)\n"
        "        print('In test_project -> kwargs: ', kwargs)\n"
        "        return\n"
        "\n"
        "    @staticmethod\n"
        "    def subcommand2(*args, **kwargs):\n"
        "        print('In test_project -> args: ', args)\n"
        "        print('In test_project -> kwargs: ', kwargs)\n"
        "        return\n"
        "\n"
        "    @staticmethod\n"
        "    def subcommand3(*args, **kwargs):\n"
        "        print('In test_project -> args: ', args)\n"
        "        print('In test_project -> kwargs: ', kwargs)\n"
        "        return\n"
        "\n"
    )

    result = fragments.PKG_MODULE_PY.format(
        packagename = package_name,
        ProjectName = project_name
    )

    assert result == expected

def test_pkg_arg_parser_py(setup):
    """
    Tests pkg_arg_parser_py
    """
    project_name, package_name = setup

    expected = (
        "\"\"\"\n"
        "TestProject Argument Parser\n"
        "\n"
        "This module contains the argument parsing functionality of the TestProject application.\n"
        "\n"
        "\"\"\"\n"
        "import argparse\n"
        "from test_project.config import colors\n"
        "\n"
        "def create_parser():\n"
        "    parser = argparse.ArgumentParser(\n"
        "        prog='test_project',\n"
        "        fromfile_prefix_chars='@',\n"
        "        usage=(\n"
        "            f'{colors.BOLD}%(prog)s{colors.ENDC} '\n"
        "            f'{colors.OKCYAN}COMMAND{colors.ENDC} '\n"
        "            f'{colors.WARNING}[{colors.ENDC}OPTION{colors.WARNING}]{colors.ENDC} '\n"
        "            f'{colors.OKBLUE}PROJECTA{colors.ENDC} '\n"
        "            f'{colors.WARNING}[{colors.ENDC}{colors.OKBLUE}PROJECTB{colors.ENDC} ...{colors.WARNING}]{colors.ENDC}'\n"
        "        ),\n"
        "        formatter_class=argparse.RawDescriptionHelpFormatter,\n"
        "    )\n"
        "\n"    
        "    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')\n"
        "\n"      
        "    subparsers = parser.add_subparsers(dest='command', required=True)\n"
        "\n"
        "    subcommand_1_parser = subparsers.add_parser('subcommand1', help='subcommand1')\n"
        "    subcommand_1_parser.add_argument('-d', '--destination', type=str, help='Valid directory pathname as destination directory')\n"
        "\n"
        "    subcommand_2_parser = subparsers.add_parser('subcommand2', help='subcommand2')\n"
        "    subcommand_2_parser.add_argument('listedargs', nargs='+', type=str, help='list of args for subcommand2')\n"
        "    subcommand_2_parser.add_argument('-o', '--opt', type=str, help='modifier for subcommand2')\n"
        "\n"
        "    subcommand_3_parser = subparsers.add_parser('subcommand3', help='subcommand3')\n"
        "    subcommand_3_parser.add_argument('arg', type=str, help='arg for subcommand 3')\n"
        "    subcommand_3_parser.add_argument('-o', '--opt', type=str, help='modifier for subcommand3')\n"
        "\n"  
        "    return parser\n"
    )

    result = fragments.PKG_ARG_PARSER_PY.format(
        packagename = package_name,
        ProjectName = project_name
    )

    assert result == expected

def test_pkg_main_py(setup):
    """
    Tests pkg_main_py
    """
    project_name, package_name = setup

    expected = (
        "\"\"\"\n"
        "Entry point for the TestProject application.\n"
        "\n"    
        "This script serves as the main entry point for the TestProject application. \n"
        "It initializes the application, processes command-line arguments, and \n"
        "starts the main functionality of the project.\n"
        "\n"
        "Usage:\n"
        "    test_project subcommand1 <argument> [options]\n"
        "    test_project subcommand2 <argument> [options]\n"
        "    test_project subcommand3 <argument> [options]\n"
        "\n"
        "Arguments:\n"
        "    -h, --help      Show this help message and exit.\n"
        "    -v, --version   Show the version of the application and exit.\n"
        "\n"
        "Functions:\n"
        "    main()      The main function that initializes and runs the application.\n"
        "    execute()   The function that invokes the subcommand passed to the application.\n"
        "\n"
        "\"\"\"\n"
        "\n"
        "from test_project.test_project import TestProject\n"
        "from test_project.arg_parser import create_parser\n"
        "from test_project.utils import preprocess_arguments\n"
        "\n"
        "SUBCOMMANDS = {\n"
        "    'subcommand1': TestProject.subcommand1,\n"
        "    'subcommand2': TestProject.subcommand2,\n"
        "    'subcommand3': TestProject.subcommand3\n"
        "}\n"
        "\n"
        "def execute(command, args):\n"
        "    func = SUBCOMMANDS[command]\n"
        "    try:\n"
        "        result = func(**vars(args))\n"
        "    except Exception as e:\n"
        "        print(f'Error: {e}\')\n"
        "    else:\n"
        "        return result\n"
        "\n"
        "def main():\n"
        "    parser = create_parser()\n"
        "    args = parser.parse_args()\n"
        "    preprocess_arguments(args)\n"
        "    execute(args.command, args)\n"
        "\n"
    )

    result = fragments.PKG_MAIN_PY.format(
        packagename = package_name,
        ProjectName = project_name
    )

    assert result == expected

def test_test_config_py(setup):
    """
    Test test_config_py
    """
    project_name, package_name = setup

    expected = (
        "\"\"\"\n"
        "TestProject Test Configuration\n"
        "\n"
        "This module contains tests for the TestProject configuration settings.\n"
        "\n"
        "\"\"\"\n"
        "\n"
        "import pytest\n"
        "from test_project.config import Config\n"
        "\n"
        "sample_config = \"\"\"\n"
        "collection:\n"
        "  VAR1: value1\n"
        "  VAR2: value2\n"
        "\"\"\"\n"
        "\n"
        "@pytest.fixture(scope='module')\n"
        "def config_file(tmp_path_factory):\n"
        "    config_path = tmp_path_factory.mktemp('data') / 'config.yaml'\n"
        "    with open(config_path, 'w') as f:\n"
        "        f.write(sample_config)\n"
        "    return config_path\n"
        "\n"
        "def test_load_from_file(config_file):\n"
        "    config = Config(config_file)\n"
        "    assert config.get('collection.VAR1') == 'value1'\n"
        "    assert config.get('collection.VAR2') == 'value2'\n"
        "\n"
        "def test_get_existing_key(config_file):\n"
        "    config = Config(config_file)\n"
        "    assert config.get('collection.VAR1') == 'value1'\n"
        "\n"
        "def test_get_non_existing_key(config_file):\n"
        "    config = Config(config_file)\n"
        "    assert config.get('non.existing.key') is None\n"
        "    assert config.get('non.existing.key', 'default_value') == 'default_value'\n"
        "\n"
        "def test_add_setting(config_file):\n"
        "    config = Config(config_file)\n"
        "    config.add_setting('new_setting', key1='value1', key2='value2')\n"
        "    assert config.get('new_setting.key1') == 'value1'\n"
        "    assert config.get('new_setting.key2') == 'value2'\n"
        "\n"
        "def test_update_setting(config_file):\n"
        "    config = Config(config_file)\n"
        "    config.add_setting('update_setting', key1='value1')\n"
        "    config.update_setting('update_setting', key1='new_value', key2='value2')\n"
        "    assert config.get('update_setting.key1') == 'new_value'\n"
        "    assert config.get('update_setting.key2') == 'value2'\n"
    )

    result = fragments.TEST_CONFIG_PY.format(
        ProjectName=project_name,
        packagename=package_name
    )

    assert result == expected

def test_test_helpers_py(setup):
    """
    Test test_helpers_py
    """
    project_name, package_name = setup

    expected = (
        "\"\"\"\n"
        "TestProject Test Helpers\n"
        "\n"
        "This module contains tests for the TestProject helper functions.\n"
        "\n"
        "\"\"\"\n"
        "import pytest\n"
        "from test_project.helpers import * # Use explicit imports\n"
    )

    result = fragments.TEST_HELPERS_PY.format(
        ProjectName=project_name,
        packagename=package_name
    )

    assert result == expected

def test_test_utils_py(setup):
    """
    Test test_utils_py
    """
    project_name, package_name = setup

    expected = (
        "\"\"\"\n"
        "TestProject Test Utilities\n"
        "\n"
        "This module contains tests for the TestProject utility functions.\n"
        "\n"
        "\"\"\"\n"
        "import shutil\n"
        "from pathlib import Path\n"
        "from argparse import Namespace\n"
        "\n"
        "import pytest\n"
        "\n"
        "from test_project.config import Config\n"
        "from test_project.utils import *\n"
        "\n"
        "@pytest.fixture(scope='function')\n"
        "def setup_and_teardown():\n"
        "    config = Config()\n"
        "    dummy_dir = config.get_tests_directory_path()\n"
        "    Path(dummy_dir).mkdir(parents=True, exist_ok=True)\n"
        "\n"
        "    yield dummy_dir, config\n"
        "\n"
        "    for item in dummy_dir.iterdir():\n"
        "        if item.is_dir():\n"
        "            shutil.rmtree(item)\n"
        "        else:\n"
        "            item.unlink()\n"
        "\n"
        "def test_do_something():\n"
        "    pass\n"
        "\n"
        "def test_do_something_else():\n"
        "    pass\n"
        "\n"
        "def test_do_another_thing():\n"
        "    pass\n"
        "\n"
        "def test_preprocess_arguments():\n"
        "    pass\n"
    )

    result = fragments.TEST_UTILS_PY.format(
        ProjectName=project_name,
        packagename=package_name
    )

    assert result == expected

def test_test_package_module_py(setup):
    """
    Test test_package_module_py
    """
    project_name, package_name = setup

    expected = (
        "\"\"\"\n"
        "TestProject Tests\n"
        "\n"
        "This module contains tests for the TestProject class.\n"
        "\n"
        "\"\"\"\n"
        "import shutil\n"
        "\n"
        "import pytest\n"
        "\n"
        "from test_project.config import Config\n"
        "from test_project.test_project import TestProject\n"
        "\n"
        "@pytest.fixture(scope='function')\n"
        "def setup_and_teardown():\n"
        "    config = Config()\n"
        "    dummy_dir = config.get_tests_directory_path()\n"
        "\n"
        "    yield dummy_dir, config\n"
        "\n"
        "    for item in dummy_dir.iterdir():\n"
        "        if item.is_dir():\n"
        "            shutil.rmtree(item)\n"
        "        else:\n"
        "            item.unlink()\n"
        "\n"
        "def test_subcommand1(setup_and_teardown):\n"
        "    dummy_dir, config = setup_and_teardown\n"
        "    assert TestProject.subcommand1 == True\n"
        "\n"
        "def test_subcommand2(setup_and_teardown):\n"
        "    dummy_dir, config = setup_and_teardown\n"
        "    assert TestProject.subcommand2 == True\n"
        "\n"
        "def test_subcommand3(setup_and_teardown):\n"
        "    dummy_dir, config = setup_and_teardown\n"
        "    assert TestProject.subcommand3 == True\n"
        "\n"
    )

    result = fragments.TEST_PACKAGE_MODULE_PY.format(
        ProjectName=project_name,
        packagename=package_name
    )

    assert result == expected

def test_arg_parser_py(setup):
    """
    Test TEST_ARG_PARSER_PY
    """
    project_name, package_name = setup

    expected = (
        "\"\"\"\n"
        "TestProject Test Arg Parser\n"
        "\n"
        "This module contains tests for the TestProject argument parser functionality.\n"
        "\n"
        "\"\"\"\n"
        "import pytest\n"
        "from test_project.arg_parser import create_parser\n"
        "\n"
        "def test_version_option(capsys):\n"
        "    parser = create_parser()\n"
        "    with pytest.raises(SystemExit):\n"
        "        parser.parse_args(['--version'])\n"
        "    captured = capsys.readouterr()\n"
        "    assert 'test_project 1.0.0' in captured.out\n"
        "\n"
        "def test_subcommand1():\n"
        "    parser = create_parser()\n"
        "    args = parser.parse_args(['subcommand1', '--destination', 'some/directory'])\n"
        "    assert args.command == 'subcommand1'\n"
        "    assert args.destination == 'some/directory'\n"
        "\n"
        "def test_subcommand2():\n"
        "    parser = create_parser()\n"
        "    args = parser.parse_args(['subcommand2', 'arg1', 'arg2', '--opt', 'optval'])\n"
        "    assert args.command == 'subcommand2'\n"
        "    assert args.listedargs == ['arg1', 'arg2']\n"
        "    assert args.opt == 'optval'\n"
        "\n"
        "def test_subcommand3():\n"
        "    parser = create_parser()\n"
        "    args = parser.parse_args(['subcommand3', 'arg1', '--opt', 'optval'])\n"
        "    assert args.command == 'subcommand3'\n"
        "    assert args.arg == 'arg1'\n"
        "    assert args.opt == 'optval'\n"
    )

    result = fragments.TEST_PKG_ARG_PARSER_PY.format(
        ProjectName=project_name,
        packagename=package_name
    )

    assert result == expected

def test_test_cli_py(setup):
    """
    Test test_config_py
    """
    project_name, package_name = setup

    expected = (
        "\"\"\"\n"
        "TestProject Test CLI\n"
        "\n"
        "This module contains tests for the TestProject CLI.\n"
        "\n"
        "\"\"\"\n"
        "import shutil\n"
        "import subprocess\n"
        "from pathlib import Path\n"
        "\n"
        "import pytest\n"
        "\n"
        "from test_project.config import Config\n"
        "\n"
        "@pytest.fixture(scope='function', autouse=True)\n"
        "def setup_and_teardown():\n"
        "    # Setup: Ensure the test directory exists\n"
        "    config = Config()\n"
        "    dummy_dir = config.get_tests_directory_path()\n"
        "    Path(dummy_dir).mkdir(parents=True, exist_ok=True)\n"
        "\n"        
        "    yield dummy_dir\n"
        "\n"        
        "    # Teardown: Clean up the test directory\n"
        "    for item in Path(dummy_dir).iterdir():\n"
        "        if item.is_dir():\n"
        "            shutil.rmtree(item)\n"
        "        else:\n"
        "            item.unlink()\n"
        "\n"
        "REASON = 'Skipping for now. Assumes application is not installed.'\n"
        "@pytest.mark.skip(reason=REASON)\n"
        "@pytest.mark.script_launch_mode('subprocess')\n"
        "def test_cli_help(script_runner):\n"
        "    result = script_runner.run(['test_project', '--help'])\n"
        "    assert result.success\n"
        "    assert 'usage' in result.stdout\n"
        "    assert result.stderr == ''\n"
        "\n"
        "@pytest.mark.skip(reason=REASON)\n"
        "@pytest.mark.script_launch_mode('subprocess')\n"
        "def test_cli_version(script_runner):\n"
        "    result = script_runner.run(['test_project', '--version'])\n"
        "    assert result.success\n"
        "    assert '0.1.0' in result.stdout  # Adjust based on your actual version\n"
        "    assert result.stderr == ''\n"
        "\n"
        "@pytest.mark.skip(reason=REASON)\n"
        "@pytest.mark.script_launch_mode('subprocess')\n"
        "def test_subcommand1(script_runner, setup_and_teardown):\n"
        "    dummy_projects_dir = setup_and_teardown\n"
        "    ret = script_runner.run(['test_project', 'subcommand1', 'arg1', '--option1', 'optval'])\n"
        "    assert ret.success\n"
    )

    result = fragments.TEST_CLI_PY.format(
        ProjectName=project_name,
        packagename=package_name
    )

    assert result == expected

def test_project_setup_py(setup):
    """
    Test PROJECT_SETUP_PY
    """
    project_name, package_name = setup

    expected = (
        "\"\"\"\n"
        "TestProject Setup\n"
        "\n"
        "This module contains the setuptools.setup() definition for the TestProject program.\n"
        "\n"
        "Usage\n"
        "    pipx install --editable .\n"
        "    pipx inject test_project -r requirements.txt\n"
        "\"\"\"\n"
        "from setuptools import setup, find_packages\n"
        "\n"
        "with open('README.md', 'r') as fh:\n"
        "    long_description = fh.read()\n"
        "\n"
        "setup(\n"
        "    name='TestProject',\n"
        "    version='0.1.0',\n"
        "    author='Emille Giddings',\n"
        "    author_email='emilledigital@gmail.com',\n"
        "    description='<description>',\n"
        "    long_description=long_description,\n"
        "    long_description_content_type='text/markdown',\n"
        "    packages=find_packages(),\n"
        "    include_package_data=True,\n"
        "    package_data={\n"
        "        '': ['config.yaml', 'data/gitignore-python', 'data/LICENSE']\n"
        "    },\n"
        "    entry_points={\n"
        "        'console_scripts': ['test_project=test_project.__main__:main']\n"
        "    },\n"
        "    tests_require=['pytest'],\n"
        "    classifiers=[\n"
        "        'Programming Language :: Python :: 3',\n"
        "        'Programming Language :: Python :: 3.11',\n"
        "        'License :: OSI Approved :: MIT License',\n"
        "        'Operating System :: POSIX',\n"
        "        'Operating System :: POSIX :: Linux',\n"
        "        'Development Status :: 3 - Alpha',\n"
        "        'Intended Audience :: Developers',\n"
        "        'Topic :: Software Development :: Libraries :: Python Modules',\n"
        "        'Natural Language :: English',\n"
        "    ],\n"
        "    python_requires='>=3.11',\n"
        ")\n"
    )

    result = fragments.PROJECT_SETUP_PY.format(
        ProjectName=project_name,
        packagename=package_name
    )

    assert result == expected

def test_project_readme_md(setup):
    """
    Test PROJECT_README_MD
    """
    project_name, _ = setup

    expected = (
        "# TestProject"
    )

    result = fragments.PROJECT_README_PY.format(
        ProjectName=project_name,
    )

    assert result == expected

def test_project_manifest_in(setup):
    """
    Test PROJECT_MANIFEST_IN
    """
    _, package_name = setup

    expected = (
        "include test_project/config.yaml\n"
        "include test_project/data/gitignore-python\n"
        "include test_project/data/LICENSE"
    )

    result = fragments.PROJECT_MANIFEST_IN.format(
        packagename=package_name,
    )

    assert result == expected

def test_project_pytest_ini():
    """
    Test PROJECT_PYTEST_INI
    """
    expected = (
        "[pytest]\n"
        "testpaths = tests/test_config.py tests/test_helpers.py tests/test_utils.py tests/test_arg_parser.py tests/test_cli.py\n"
        "addopts = --ignore=env --ignore=.venv -sv\n"
    )

    result = fragments.PROJECT_PYTEST_INI

    assert result == expected

def test_project_license():
    """
    Test PROJECT_LICENSE
    """
    expected = (
        "Copyright 2021 Emille Giddings\n"
        "\n"
        "Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the \"Software\"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n"
        "\n"
        "The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n"
        "\n"
        "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n"
    )

    result = fragments.PROJECT_LICENSE

    assert result == expected

def test_project_config_yaml():
    """
    Test PROJECT_CONFIG_YAML
    """
    expected = (
        "settings:\n"
        "  DUMMY_DIR: tests/dummy\n"
        "  VAR2: VAL2\n"
    )

    result = fragments.PROJECT_CONFIG_YAML

    assert result == expected