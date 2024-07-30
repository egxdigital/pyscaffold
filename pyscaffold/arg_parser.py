"""
Pyscaffold Argument Parser

This module contains the argument parsing functionality of the Pyscaffold application.
It defines the command-line interface (CLI) for the application using argparse,
enabling users to list, start, and resume projects with various options.

Functions:
    create_parser: Creates and configures the argument parser for the Pyscaffold CLI.
"""

import argparse
from pyscaffold.config import colors
from pyscaffold.fragments import pyscaffold_ascii

def create_parser() -> argparse.ArgumentParser:
    """
    Creates and configures the argument parser for the Pyscaffold CLI.

    This function sets up the argument parser with commands and options for the Pyscaffold application.
    It includes commands for listing projects, starting new projects, and resuming existing projects,
    each with their respective arguments and options.

    Returns:
        argparse.ArgumentParser: The configured argument parser.
    """
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
    
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    
    subparsers = parser.add_subparsers(dest='command', required=True)

    list_parser = subparsers.add_parser('list', help='List projects')
    list_parser.add_argument('-d', '--destination', type=str, help='Valid directory pathname as project directory')

    start_parser = subparsers.add_parser('start', help='Start a project')
    start_parser.add_argument('project_names', nargs='+', type=str, help='Name(s) of the project to start')
    start_parser.add_argument('-p', '--python-version', type=str, default='3.11', help='Python version to use on start')
    start_parser.add_argument('-d', '--destination', type=str, help='Valid directory pathname as project directory')

    resume_parser = subparsers.add_parser('resume', help='Resume a project')
    resume_parser.add_argument('project_name', type=str, help='Name of the project to resume')
    resume_parser.add_argument('-d', '--destination', type=str, help='Valid directory pathname as project directory')
    
    return parser