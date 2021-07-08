"""Pyscaffold

This module contains the main function definitions for the Pyscaffold Program.
"""
import os
import sys
import subprocess
import argparse
from shutil import copyfile
from pathlib import Path, PurePath
from pyscaffold.helpers import conventional_naming, get_file_name, get_func_name
from pyscaffold.fragments import setup_py, readme_md, test_helpers_py, test_project_py, innermodule_py, innerpkg_helper_py, innerpkg_main_py


def activate_virtual_env(root, env_name):
    """Takes an absolute path to the root project directory and the enclosed environment name
    and activates the virtual environment in the current shell. Use CTRL + D to exit when done.
    Thanks to Depado on StackOverflow for the solution: https://stackoverflow.com/a/18037819"""
    
    activate_script = PurePath(root, env_name, "bin", "activate")
    
    if Path(activate_script).is_file():
        try:
            command = f"/bin/bash --rcfile {activate_script}"
            os.chdir(root)
            print("Moving to working directory...", Path.cwd())
            subprocess.run(command.split())
        except Exception as e:
            print(e)


def deploy_virtual_environment(root, env_name):
    """Takes an absolute path to the root project directory and the enclosed environment name
    to deploy the virtual environment"""
    path_to_env = PurePath(root, env_name)
    command = f"/usr/bin/python3 -m virtualenv {path_to_env}"
    try:
        subprocess.run(command.split())
    except Exception as e:
        print(e)


def copy_license(data_dir, dest):
    """Takes an absolute path to a data directory containing the LICENSE file as source
    and copies it to destination
    """
    source = PurePath(Path(data_dir), 'LICENSE')
    destination = PurePath(Path(dest), 'LICENSE')
    copyfile(source, destination)


def copy_gitignore(data_dir, dest):
    """Takes an absolute path to a data directory containing the gitignore-python file as source
    and copies it to destination
    """
    source = PurePath(Path(data_dir), 'gitignore-python')
    destination = PurePath(Path(dest), '.gitignore')
    copyfile(source, destination)


def load_boilerplate_setup(path, project):
    """Takes an absolute pathname to setup.py and a project name loads boilerplate 
    code into the file at that location"""
    Project = conventional_naming(project, is_package=False)
    try:
        Path(path).write_text(setup_py.format(
            project=project, Project=Project))
    except Exception as e:
        print(f"Exception @{get_func_name()} in {get_file_name()}:\n {e}")


def load_boilerplate_readme(path, project):
    """Takes an absolute pathname to README.md and a project name and loads initial
    text into the file at that location"""
    try:
        Path(path).write_text(readme_md.format(project=project))
    except Exception as e:
        print(f"Exception @{get_func_name()}: {e}")


def insert_init_py(dest):
    """Takes an absolute pathname to __init__.py and creates the file at that location"""
    dest = PurePath(dest, '__init__.py')
    try:
        Path(dest).touch()
    except Exception as e:
        print(f"Exception @{get_func_name()}: {e}")


def load_boilerplate_innerpkg_helper(path, project):
    """Takes an absolute pathname to helpers.py and a project name and loads boilerplate
    code into the file at that location"""
    Project = conventional_naming(project, is_package=False)
    try:
        Path(path).write_text(innerpkg_helper_py.format(
            Project=Project, project=project))
    except Exception as e:
        print(f"Exception @{get_func_name()}: {e}")


def load_boilerplate_innerpkg_main(path, project):
    """Takes an absolute pathname to __main__.py and a project name loads boilerplate 
    code into the file at that location"""
    Project = conventional_naming(project, is_package=False)
    try:
        Path(path).write_text(innerpkg_main_py.format(
            Project=Project, project=project))
    except Exception as e:
        print(f"Exception @{get_func_name()}: {e}")


def load_boilerplate_innermodule(path, project):
    """Takes an absolute pathname to <project>.py and a project name and loads boilerplate 
    code into the file at that location"""
    Project = conventional_naming(project, is_package=False)
    try:
        Path(path).write_text(innermodule_py.format(
            Project=Project, project=project))
    except Exception as e:
        print(f"Exception @{get_func_name()}: {e}")


def load_boilerplate_test_helpers(path, project):
    """Takes an absolute pathname to test_helpers.py and a project name and loads boilerplate 
    code into the file at that location"""
    Project = conventional_naming(project, is_package=False)
    try:
        Path(path).write_text(test_helpers_py.format(
            Project=Project, project=project))
    except Exception as e:
        print(f"Exception @{get_func_name()}: {e}")


def load_boilerplate_test_innerpkg(path, project):
    """Takes an absolute pathname to test_<project>.py and a project name and loads boilerplate 
    code into the file at that location"""
    Project = conventional_naming(project, is_package=False)
    try:
        Path(path).write_text(test_project_py.format(
            Project=Project, project=project))
    except Exception as e:
        print(f"Exception @{get_func_name()}:\n {e}")


def create_innerpkg(root, name):
    """Takes an absolute pathname representing a project root and a name
    and creates a Python package at that location"""
    innerpkg = PurePath(root, name)
    try:
        Path(innerpkg).mkdir()
    except Exception as e:
        print(f"Exception @{get_func_name()}:\n {e}")

    insert_init_py(innerpkg)


def load_project(path, name):
    """Takes an absolute pathname representing a project root and a name 
    and loads the project with subdirectories and boilerplate"""
    
    data = PurePath(Path(__file__).parent.parent, 'data')

    make_dirs = {
        'bin': PurePath(path, 'bin'),
        'data': PurePath(path, 'data'),
        'docs': PurePath(path, 'docs'),
        'tests': PurePath(path, 'tests'),
        name: PurePath(path, name)
    }

    for dir in make_dirs.values():
        try:
            Path(dir).mkdir()
        except FileExistsError as fee:
            print(f"Directory already exists @{path}")
            #print(f"Exception @{get_func_name()}: {fee}")

    contents = {
        'tests': {
            'innerpkg': PurePath(make_dirs['tests'], f"test_{name}.py"),
            'helpers': PurePath(make_dirs['tests'], "test_helpers.py")
        },
        name: {
            'innermodule': PurePath(make_dirs[name], f"{name}.py"),
            'main': PurePath(make_dirs[name], "__main__.py"),
            'helpers': PurePath(make_dirs[name], "helpers.py")
        },
        'readme': PurePath(path, 'README.md'),
        'setup': PurePath(path, 'setup.py')
    }

    test_innerpkg = contents['tests']['innerpkg']
    test_helpers = contents['tests']['helpers']
    innerpkg_main = contents[name]['main']
    innermodule = contents[name]['innermodule']
    innerpkg_helper = contents[name]['helpers']
    readme = contents['readme']
    setup = contents['setup']

    insert_init_py(make_dirs[name])

    load_boilerplate_test_innerpkg(test_innerpkg, name)
    load_boilerplate_test_helpers(test_helpers, name)
    load_boilerplate_innermodule(innermodule, name)
    load_boilerplate_innerpkg_helper(innerpkg_helper, name)
    load_boilerplate_innerpkg_main(innerpkg_main, name)
    load_boilerplate_readme(readme, name)
    load_boilerplate_setup(setup, name)

    copy_license(data, path)
    copy_gitignore(data, path)


def create_project_root(path):
    """Takes an absolute path and makes a directory at that location"""
    try:
        Path(path).mkdir(parents=True, exist_ok=False)
    except FileExistsError as e:
        print(f"Directory already exists @ {path}")
        sys.exit()
        #print(f"Exception @{get_func_name()}: {e}")


def main():
    my_parser = argparse.ArgumentParser(
        prog='pyscaffold',
        fromfile_prefix_chars='@',
        usage='%(prog)s start [OPTION] project_name',
        description='Scaffold Python applications',
        epilog='Build it! :)')

    my_parser.add_argument('-d', '--destination',
                           action='store',
                           type=str,
                           required=False,
                           help='valid directory pathname as project directory')

    my_parser.add_argument('arguments',
                           nargs='+',
                           help="pyscaffold [start, resume] <project>[, <projectA>, ...]")

    args = my_parser.parse_args()

    valid_commands = ['start', 'resume']

    projects_folder = os.getenv('python', default=Path.cwd())

    options = vars(args)

    arguments = options['arguments']
    dest = options['destination']

    command = arguments[0]

    if dest is not None:
        projects_folder = dest

    if command not in valid_commands:
        print(f"Error: invalid command - {command}")
        sys.exit()
    
    proj_names = [conventional_naming(name) for name in arguments[1:]]

    if command == 'start':        
        projects = {name : PurePath(projects_folder, conventional_naming(name, is_package=False))
                    for name in proj_names}

        for name, path in projects.items():
            create_project_root(path)
            load_project(path=path, name=name)
            deploy_virtual_environment(path, 'env')
        
        if len(projects) == 1:
            activate_virtual_env(projects[proj_names[0]], 'env')

    if command == 'resume':
        if len(proj_names) > 1:
            print("For now, resume only one project")
            sys.exit()
        
        proj = proj_names[0]

        path_to_proj = PurePath(projects_folder, conventional_naming(proj, is_package=False))

        activate_virtual_env(path_to_proj, 'env')