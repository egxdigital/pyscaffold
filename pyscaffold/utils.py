import os
import argparse
import subprocess
from pathlib import Path

from pyscaffold.config import Config, colors
from pyscaffold.helpers import apply_project_naming_convention

def project_exists(project_name: str, destination: str) -> bool:
    project_path = Path(destination) / project_name
    return project_path.is_dir()

def project_ready(project_path: Path) -> bool:
    setup_file = project_path / 'setup.py'
    env_dir = project_path / 'env'
    venv_dir = project_path / 'venv'
    return setup_file.is_file() and (env_dir.is_dir() or venv_dir.is_dir())

def change_directory(project_path: Path) -> None:
    os.chdir(project_path)

def set_destination(args: argparse.Namespace) -> None:
    config = Config()
    if os.getenv('ON_TEST'):
        projects_directory_setting = config.get_tests_directory_path()
    else:
        projects_directory_setting = config.get_projects_directory_path()
    
    destination = getattr(args, 'destination', None)

    if destination:
        if Path(destination).is_dir():
            args.destination = destination
        else:
            raise ValueError("The provided destination directory is not valid.")
    elif projects_directory_setting and Path(projects_directory_setting).is_dir():
        args.destination = projects_directory_setting
    else:
        raise ValueError("A valid destination directory must be provided either via --destination or by setting the value in config.yaml")

def apply_naming_conventions(args: argparse.Namespace) -> None:
    if hasattr(args, 'project_name'):
        args.project_name = apply_project_naming_convention(args.project_name)
    if hasattr(args, 'project_names'):
        args.project_names = [apply_project_naming_convention(name) for name in args.project_names]

def preprocess_arguments(args: argparse.Namespace) -> None:
    set_destination(args)
    apply_naming_conventions(args)

def execute_command(command: str) -> bool:
    try:
        subprocess.run(command, shell=True, executable='/bin/bash', check=True)
        return True
    except subprocess.CalledProcessError as e:
        #print(f"Error occurred: {e.stderr.decode()}")
        print(e)
        return False

def activate_virtual_env(project_path):
    activate_script = None
    marker_file = project_path / 'venv_activated.marker'

    if (project_path / 'venv' / 'bin' / 'activate').exists():
        activate_script = project_path / 'venv' / 'bin' / 'activate'
    elif (project_path / 'env' / 'bin' / 'activate').exists():
        activate_script = project_path / 'env' / 'bin' / 'activate'

    if activate_script:
        change_directory(project_path)

        if os.getenv('ON_TEST'):
            command = f"source {activate_script} && touch {marker_file} && exit"
        else:
            os.system('clear')
            print(f"{colors.WARNING}To{colors.ENDC} {colors.OKCYAN}DEACTIVATE{colors.ENDC} use {colors.OKGREEN}CTRL + D{colors.ENDC}")
            command = f"/bin/bash --rcfile {activate_script}"
        
        return execute_command(command)

    else:
        print(f"Could not find the virtual environment activation script for '{project_path.name}'.")
        return False