"""Pyscaffold

This module contains the main function definitions for the Pyscaffold Program.

Examples:
    pyscaffold start project projecta projectb
    pyscaffold start project -p 3.9
    pyscaffold resume projecta
"""
import os
import argparse
import subprocess
from shutil import copyfile
from pathlib import Path, PurePath
from pyscaffold.config import colors, ERROR, PROJECTS_FOLDER, PYTHON_VERSION
from pyscaffold.helpers import conventional_naming, delete_directory, get_file_name, get_func_name, is_tool, error
from pyscaffold.fragments import config_py, pyscaffold_ascii, setup_py, readme_md, test_helpers_py, test_project_py, innermodule_py, innerpkg_helper_py, innerpkg_main_py


class Pyscaffold():
    def __init__(self, parser, options: dict):
        self.switches = [
            'repository'
            'python',
            'destination'
        ]

        self.valid_commands = {
            'start': self.start,
            'resume': self.resume,
            'deploy': self.deploy,
            'upgrade': self.upgrade
        }

        self.options = options
        self.command = ''
        self.destination = ''
        self.python_version = PYTHON_VERSION
        self.projects = []
        self.payloads = []

        self.parser = parser
        self.set_directory(self.options)
        self.set_command(self.options)
        self.set_python_version(self.options)
        self.set_projects(self.options)
        self.valid_commands[self.command]()

    def __str__(self):
        return (
            'command: {}\n'
            'directory: {}\n'
            'projects: {}\n'
            'python version: {}\n'
        ).format(
            self.command,
            self.destination,
            self.projects,
            self.python_version
        )

    def set_directory(self, argv):
        destination = argv['destination']

        if destination is not None:
            if not Path(destination).is_dir():
                self.parser.error(ERROR.bad_directory)
            self.destination = destination

        if destination is None:
            self.destination = PROJECTS_FOLDER

    def set_command(self, argv):
        command = argv['arguments'][0]
        if command not in self.valid_commands.keys():
            self.parser.error(ERROR.bad_command)
        self.command = command

    def set_projects(self, argv):
        arguments = argv['arguments'][1:]
        if arguments == []:
            self.parser.error(ERROR.no_projects)

        if len(arguments) == 1:
            if ',' in arguments[0]:
                self.parser.error(ERROR.bad_project_list)

        self.projects = arguments

    def set_python_version(self, argv):
        version = argv['python']

        if version is not None:
            self.python_version = version

        if not is_tool(f'python{self.python_version}'):
            self.parser.error(
                error(self.command, ERROR.bad_python_version, self.python_version))

    def start(self):
        os.system('clear')
        projects = {name: PurePath(self.destination, conventional_naming(name, is_package=False))
                    for name in self.projects}

        for name, path in projects.items():
            self.create_project_root(path)
            self.load_project(path=path, name=name, ver=self.python_version)
            self.deploy_virtual_environment(path, 'env', self.python_version)

        if len(projects) == 1:
            self.activate_virtual_env(projects[self.projects[0]], 'env')

    def resume(self):
        if len(self.projects) > 1:
            self.parser.error(error(self.command, ERROR.resume_only_one))

        proj = self.projects[0]

        path_to_proj = PurePath(
            self.destination, conventional_naming(proj, is_package=False))

        if Path(path_to_proj).is_dir():
            self.activate_virtual_env(Path(path_to_proj), 'env')

        if not Path(path_to_proj).is_dir():
            self.parser.error(
                error(self.command, ERROR.project_not_found, proj))

    def deploy(self, *objects):
        print("Time to insert something.")

        target_repo = self.projects[0]

        if target_repo is not None:
            repo_name_proper = conventional_naming(
                target_repo, is_package=False)
            print(repo_name_proper)

    def upgrade(self):
        if len(self.projects) > 1:
            self.parser.error(error(self.command, ERROR.more_than_one))
        if len(self.projects) == 1:
            project = self.projects[0]
            self.replace_env(project)

    def create_project_root(self, path):
        """Takes an absolute path and makes a directory at that location"""
        try:
            Path(path).mkdir(parents=True, exist_ok=False)
        except FileExistsError as e:
            self.parser.error(error(self.command, ERROR.project_exists, path))

    def load_project(self, path, name, ver=3.9):
        """Takes an absolute pathname representing a project root and a name 
        and loads the project with subdirectories and boilerplate.

        Parameters
        ----------
        path : [type]
            [description]
        name : [type]
            [description]
        """

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
                print(
                    f"{colors.WARNING}directory already exists{colors.ENDC} @ {colors.OKBLUE}{path}{colors.ENDC}")
                #print(f"Exception @{get_func_name()}: {fee}")

        contents = {
            'tests': {
                'innerpkg': PurePath(make_dirs['tests'], f"test_{name}.py"),
                'helpers': PurePath(make_dirs['tests'], "test_helpers.py")
            },
            name: {
                'config': PurePath(make_dirs[name], "config.py"),
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
        innerpkg_config = contents[name]['config']
        readme = contents['readme']
        setup = contents['setup']

        self.insert_init_py(make_dirs[name])

        self.load_boilerplate_test_innerpkg(test_innerpkg, name)
        self.load_boilerplate_test_helpers(test_helpers, name)
        self.load_boilerplate_innermodule(innermodule, name)
        self.load_boilerplate_innerpkg_helper(innerpkg_helper, name)
        self.load_boilerplate_innerpkg_main(innerpkg_main, name)
        self.load_boilerplate_innerpkg_config(innerpkg_config, name)
        self.load_boilerplate_readme(readme, name)
        self.load_boilerplate_setup(setup, name, ver=ver)

        self.copy_license(data, path)
        self.copy_gitignore(data, path)

    def activate_virtual_env(self, root, env_name):
        """Takes an absolute path to the root project directory and the enclosed environment name
        and activates the virtual environment in the current shell. Use CTRL + D to exit when done.
        Thanks to Depado on StackOverflow for the solution: https://stackoverflow.com/a/18037819"""

        activate_script = PurePath(root, env_name, "bin", "activate")

        if Path(activate_script).is_file():
            try:
                command = f"/bin/bash --rcfile {activate_script}"
                os.chdir(root)
                print(
                    f"{colors.WARNING}moving to{colors.ENDC} {colors.OKBLUE}{Path.cwd()}{colors.ENDC}")
                print(
                    f"{colors.WARNING}to{colors.ENDC} {colors.OKCYAN}DEACTIVATE{colors.ENDC} use {colors.OKGREEN}CTRL + D {colors.ENDC}")
                subprocess.run(command.split())
            except Exception as e:
                print(e)

    def deploy_virtual_environment(self, root, env_name, ver=PYTHON_VERSION):
        """Takes an absolute path to the root project directory and the enclosed environment name
        to deploy the virtual environment"""

        path_to_env = PurePath(root, env_name)
        command = f"/usr/bin/python{ver} -m virtualenv {path_to_env} --python=python{ver}"

        try:
            subprocess.run(command.split())
        except Exception as e:
            print(e)
        else:
            os.system('clear')
            print(f"{colors.OKCYAN}virtual environment installed{colors.ENDC}: {colors.OKGREEN}{ver}{colors.ENDC}")

    def copy_license(self, data_dir, dest):
        """Takes an absolute path to a data directory containing the LICENSE file as source
        and copies it to destination
        """
        source = PurePath(Path(data_dir), 'LICENSE')
        destination = PurePath(Path(dest), 'LICENSE')
        copyfile(source, destination)

    def copy_gitignore(self, data_dir, dest):
        """Takes an absolute path to a data directory containing the gitignore-python file as source
        and copies it to destination
        """
        source = PurePath(Path(data_dir), 'gitignore-python')
        destination = PurePath(Path(dest), '.gitignore')
        copyfile(source, destination)

    def load_boilerplate_setup(self, path, project, ver=3.9):
        """Takes an absolute pathname to setup.py and a project name loads boilerplate 
        code into the file at that location"""
        Project = conventional_naming(project, is_package=False)
        try:
            Path(path).write_text(setup_py.format(
                project=project,
                Project=Project,
                version=ver,
                newline='\n'.encode('unicode_escape').decode('utf-8')))
        except Exception as e:
            print(f"Exception @{get_func_name()} in {get_file_name()}:\n {e}")

    def load_boilerplate_readme(self, path, project):
        """Takes an absolute pathname to README.md and a project name and loads initial
        text into the file at that location"""
        try:
            Path(path).write_text(readme_md.format(project=project))
        except Exception as e:
            print(f"Exception @{get_func_name()}: {e}")

    def insert_init_py(self, dest):
        """Takes an absolute pathname to __init__.py and creates the file at that location"""
        dest = PurePath(dest, '__init__.py')
        try:
            Path(dest).touch()
        except Exception as e:
            print(f"Exception @{get_func_name()}: {e}")

    def load_boilerplate_innerpkg_helper(self, path, project):
        """Takes an absolute pathname to helpers.py and a project name and loads boilerplate
        code into the file at that location"""
        Project = conventional_naming(project, is_package=False)
        try:
            Path(path).write_text(innerpkg_helper_py.format(
                Project=Project, project=project))
        except Exception as e:
            print(f"Exception @{get_func_name()}: {e}")

    def load_boilerplate_innerpkg_main(self, path, project):
        """Takes an absolute pathname to __main__.py and a project name loads boilerplate 
        code into the file at that location"""
        Project = conventional_naming(project, is_package=False)
        try:
            Path(path).write_text(innerpkg_main_py.format(
                Project=Project, project=project))
        except Exception as e:
            print(f"Exception @{get_func_name()}: {e}")

    def load_boilerplate_innermodule(self, path, project):
        """Takes an absolute pathname to <project>.py and a project name and loads boilerplate 
        code into the file at that location"""
        Project = conventional_naming(project, is_package=False)
        try:
            Path(path).write_text(innermodule_py.format(
                Project=Project, project=project))
        except Exception as e:
            print(f"Exception @{get_func_name()}: {e}")

    def load_boilerplate_innerpkg_config(self, path, project):
        Project = conventional_naming(project, is_package=False)
        try:
            Path(path).write_text(config_py.format(
                Project=Project))
        except Exception as e:
            print(f"Exception @{get_func_name()}: {e}")
    
    def load_boilerplate_test_helpers(self, path, project):
        """Takes an absolute pathname to test_helpers.py and a project name and loads boilerplate 
        code into the file at that location"""
        Project = conventional_naming(project, is_package=False)
        try:
            Path(path).write_text(test_helpers_py.format(
                Project=Project, project=project))
        except Exception as e:
            print(f"Exception @{get_func_name()}: {e}")

    def load_boilerplate_test_innerpkg(self, path, project):
        """Takes an absolute pathname to test_<project>.py and a project name and loads boilerplate 
        code into the file at that location"""
        Project = conventional_naming(project, is_package=False)
        try:
            Path(path).write_text(test_project_py.format(
                Project=Project, project=project))
        except Exception as e:
            print(f"Exception @{get_func_name()}:\n {e}")

    def create_innerpkg(self, root, name):
        """Takes an absolute pathname representing a project root and a name
        and creates a Python package at that location"""
        innerpkg = PurePath(root, name)
        try:
            Path(innerpkg).mkdir()
        except Exception as e:
            print(f"Exception @{get_func_name()}:\n {e}")

        self.insert_init_py(innerpkg)

    def replace_env(self, project):
        target_repo = PurePath(
            self.destination, conventional_naming(project, is_package=False))

        target_env = PurePath(target_repo, 'env')

        if not Path(target_env).is_dir():
            print(f"{colors.WARNING}{ERROR.no_env_found}{colors.ENDC}")
            self.deploy_virtual_environment(
                target_repo, 'env', self.python_version)

        print('Python virtual environment found!')

        try:
            delete_directory(target_env)
        except Exception as e:
            print(e)
        else:
            print('installing new python version')
            self.deploy_virtual_environment(
                target_repo, 'env', self.python_version)


def main():
    parser = argparse.ArgumentParser(
        prog='pyscaffold',
        fromfile_prefix_chars='@',
        usage=(
            f'{colors.BOLD}%(prog)s{colors.ENDC} '
            f'{colors.OKCYAN}COMMAND{colors.ENDC} '
            f'{colors.WARNING}[{colors.ENDC}OPTION{colors.WARNING}]{colors.ENDC} '
            f'{colors.OKBLUE}PROJECTA{colors.ENDC} '
            f'{colors.WARNING}[{colors.ENDC}{colors.OKBLUE}PROJECTB{colors.ENDC} ...{colors.WARNING}]{colors.ENDC}'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=pyscaffold_ascii,
        epilog='Build it! :)')

    parser.add_argument('-r', '--repository',
                        action='store',
                        type=str,
                        required=False,
                        help='project repository name')

    parser.add_argument('-p', '--python',
                        action='store',
                        type=float,
                        required=False,
                        help='python version')

    parser.add_argument('-d', '--destination',
                        action='store',
                        type=str,
                        required=False,
                        help='valid directory pathname as project directory')

    parser.add_argument('arguments',
                        nargs='+',
                        help="pyscaffold [start, resume] <project>[, <projectA>, ...]")

    args = parser.parse_args()

    options = vars(args)

    scaffold = Pyscaffold(parser, options)