"""
Pyscaffold Test Arg Parser

This module contains tests for the `Pyscaffold` argument parser functionality. It verifies that the argument parser correctly 
handles various command-line options and commands, including version information, different commands, and the help option.

Tests:
- test_version_option: Ensures that the `--version` option prints the version information and exits.
- test_list_command: Verifies that the `list` command parses and stores the destination directory argument correctly.
- test_start_command: Validates that the `start` command correctly parses multiple project names, the destination directory, 
  and the Python version.
- test_resume_command: Tests that the `resume` command correctly parses the project name and destination directory arguments.
- test_no_command: Checks that no command raises a `SystemExit` exception when no arguments are provided.
- test_help_option: Ensures that the `--help` option prints the help message and exits.
"""

import pytest
from pyscaffold.arg_parser import create_parser

def test_version_option(capsys):
    """
    Test the `--version` option of the argument parser.

    Ensures that the `--version` option prints the version information and exits the program.

    Args:
        capsys (pytest.Capsys): The pytest fixture to capture output to sys.stdout and sys.stderr.
    """
    parser = create_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(['--version'])
    captured = capsys.readouterr()
    assert 'pyscaffold 1.0.0' in captured.out

def test_list_command():
    """
    Test the `list` command of the argument parser.

    Verifies that the `list` command correctly parses and stores the destination directory argument.

    Args:
        None
    """
    parser = create_parser()
    args = parser.parse_args(['list', '--destination', 'some/directory'])
    assert args.command == 'list'
    assert args.destination == 'some/directory'

def test_start_command():
    """
    Test the `start` command of the argument parser.

    Validates that the `start` command correctly parses multiple project names, the destination directory, and the Python version.

    Args:
        None
    """
    parser = create_parser()
    args = parser.parse_args(['start', 'ProjectA', 'ProjectB', '--destination', 'some/other/directory', '--python-version', '3.10'])
    assert args.command == 'start'
    assert args.project_names == ['ProjectA', 'ProjectB']
    assert args.python_version == '3.10'
    assert args.destination == 'some/other/directory'

def test_resume_command():
    """
    Test the `resume` command of the argument parser.

    Ensures that the `resume` command correctly parses the project name and destination directory arguments.

    Args:
        None
    """
    parser = create_parser()
    args = parser.parse_args(['resume', 'ProjectA', '--destination', 'yet/another/directory'])
    assert args.command == 'resume'
    assert args.project_name == 'ProjectA'
    assert args.destination == 'yet/another/directory'

def test_no_command():
    """
    Test the absence of a command.

    Checks that no command provided to the argument parser raises a `SystemExit` exception.

    Args:
        None
    """
    parser = create_parser()
    with pytest.raises(SystemExit):
        parser.parse_args([])

def test_help_option(capsys):
    """
    Test the `--help` option of the argument parser.

    Ensures that the `--help` option prints the help message and exits the program.

    Args:
        capsys (pytest.Capsys): The pytest fixture to capture output to sys.stdout and sys.stderr.
    """
    parser = create_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(['--help'])
    captured = capsys.readouterr()
    assert 'usage:' in captured.out
