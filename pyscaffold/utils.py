"""
Pyscaffold Utilities

This module contains utility functions for managing Python projects, including 
checking project existence, validating project readiness, changing directories, 
setting destination directories, applying naming conventions, preprocessing arguments, 
executing shell commands, and activating virtual environments.

"""
import os
import argparse
import subprocess
from pathlib import Path

from pyscaffold.config import Config, colors
from pyscaffold.helpers import apply_project_naming_convention

def project_exists(project_name: str, destination: str) -> bool:
    """
    Check if a project directory exists.

    Args:
        project_name (str): The name of the project directory.
        destination (str): The path where the project directory is expected to be located.

    Returns:
        bool: True if the project directory exists, otherwise False.
    """
    project_path = Path(destination) / project_name
    return project_path.is_dir()

def project_ready(project_path: Path) -> bool:
    """
    Check if a project is ready by verifying the presence of required files and directories.

    Args:
        project_path (Path): The path to the project directory.

    Returns:
        bool: True if the project has a 'setup.py' file and at least one virtual environment directory, otherwise False.
    """
    setup_file = project_path / 'setup.py'
    env_dir = project_path / 'env'
    venv_dir = project_path / 'venv'
    return setup_file.is_file() and (env_dir.is_dir() or venv_dir.is_dir())

def change_directory(project_path: Path) -> None:
    """
    Change the current working directory to the specified project path.

    Args:
        project_path (Path): The path to the directory to change to.
    """
    os.chdir(project_path)

def set_destination(args: argparse.Namespace) -> None:
    """
    Set the destination directory for project creation based on arguments or configuration.

    Args:
        args (argparse.Namespace): The arguments namespace containing the 'destination' attribute.

    Raises:
        ValueError: If the provided destination directory is invalid or not set.
    """
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
    """
    Apply naming conventions to project names provided in the arguments.

    Args:
        args (argparse.Namespace): The arguments namespace containing 'project_name' or 'project_names' attributes.
    """
    if hasattr(args, 'project_name'):
        args.project_name = apply_project_naming_convention(args.project_name)
    if hasattr(args, 'project_names'):
        args.project_names = [apply_project_naming_convention(name) for name in args.project_names]

def preprocess_arguments(args: argparse.Namespace) -> None:
    """
    Preprocess command-line arguments by setting the destination and applying naming conventions.

    Args:
        args (argparse.Namespace): The arguments namespace to preprocess.
    """
    set_destination(args)
    apply_naming_conventions(args)

def execute_command(command: str) -> bool:
    """
    Execute a shell command and check its success.

    Args:
        command (str): The shell command to execute.

    Returns:
        bool: True if the command was executed successfully, otherwise False.
    """
    try:
        subprocess.run(command, shell=True, executable='/bin/bash', check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr.decode()}")
        return False

def activate_virtual_env(project_path):
    """
    Activate the virtual environment for the specified project directory.

    Args:
        project_path (Path): The path to the project directory.

    Returns:
        bool: True if the virtual environment was successfully activated, otherwise False.
    """
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