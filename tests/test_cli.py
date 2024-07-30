"""
Pyscaffold Test CLI

This module contains tests for the `Pyscaffold` command-line interface (CLI). The tests cover various CLI commands and options to ensure the correctness and reliability of the CLI functionality.

Tests:
- test_cli_help: Verifies that the `--help` option displays the help message and that there are no errors.
- test_cli_version: Checks that the `--version` option displays the correct version number and that there are no errors.
- test_start_command_with_one_project: Tests the `start` command with a single project name and ensures it correctly starts the project in the specified destination.
- test_start_command_two_projects: Tests the `start` command with two project names and verifies that both projects are started correctly in the specified destination.
- test_start_command_with_good_explicit_destination: Validates that the `start` command works correctly with an explicitly specified destination directory.
- test_start_command_with_bad_explicit_destination: Ensures that the `start` command fails with an invalid explicitly specified destination directory.
- test_resume_existing_project: Tests the `resume` command for an existing project. It sets up a dummy project, initializes a virtual environment, and verifies that the project is resumed correctly. It also checks for the presence of a marker file to indicate successful resume.

"""

import shutil
import subprocess
from pathlib import Path

import pytest

from pyscaffold.config import Config

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    """
    Fixture for setting up and tearing down the test environment.

    Creates a temporary directory for storing test projects before each test and cleans it up after the test finishes.
    """
    # Setup: Ensure the test directory exists
    config = Config()
    dummy_projects_dir = config.get_tests_directory_path()
    Path(dummy_projects_dir).mkdir(parents=True, exist_ok=True)
    
    yield dummy_projects_dir
    
    # Teardown: Clean up the test directory
    for item in Path(dummy_projects_dir).iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

@pytest.mark.script_launch_mode('subprocess')
def test_cli_help(script_runner):
    """
    Test the `--help` option of the `Pyscaffold` CLI.

    Verifies that the help message is displayed and there are no errors in the output.

    Args:
        script_runner (pytest.ScriptRunner): The pytest fixture to run CLI commands.
    """
    result = script_runner.run(['pyscaffold', '--help'])
    assert result.success
    assert 'usage' in result.stdout
    assert result.stderr == ''

@pytest.mark.script_launch_mode('subprocess')
def test_cli_version(script_runner):
    """
    Test the `--version` option of the `Pyscaffold` CLI.

    Ensures that the correct version number is displayed and there are no errors in the output.

    Args:
        script_runner (pytest.ScriptRunner): The pytest fixture to run CLI commands.
    """
    result = script_runner.run(['pyscaffold', '--version'])
    assert result.success
    assert '1.0.0' in result.stdout  # Adjust based on your actual version
    assert result.stderr == ''

@pytest.mark.script_launch_mode('subprocess')
def test_start_command_with_one_project(script_runner, setup_and_teardown):
    """
    Test the `start` command with a single project name.

    Verifies that the project is started correctly in the specified destination directory.

    Args:
        script_runner (pytest.ScriptRunner): The pytest fixture to run CLI commands.
        setup_and_teardown (Path): The temporary directory for test projects.
    """
    dummy_projects_dir = setup_and_teardown
    ret = script_runner.run(['pyscaffold', 'start', 'project_a', '--destination', str(dummy_projects_dir)])
    assert ret.success
    assert f"Starting project: ProjectA at {dummy_projects_dir}" in ret.stdout

@pytest.mark.script_launch_mode('subprocess')
def test_start_command_two_projects(script_runner, setup_and_teardown):
    """
    Test the `start` command with two project names.

    Ensures that both projects are started correctly in the specified destination directory.

    Args:
        script_runner (pytest.ScriptRunner): The pytest fixture to run CLI commands.
        setup_and_teardown (Path): The temporary directory for test projects.
    """
    dummy_projects_dir = setup_and_teardown
    ret = script_runner.run(['pyscaffold', 'start', 'projectA', 'projectB', '--destination', str(dummy_projects_dir)])
    assert ret.success
    assert f"Starting project: Projecta at {dummy_projects_dir}/Projecta" in ret.stdout
    assert f"Starting project: Projectb at {dummy_projects_dir}/Projectb" in ret.stdout

@pytest.mark.script_launch_mode('subprocess')
def test_start_command_with_good_explicit_destination(script_runner):
    """
    Test the `start` command with a valid explicitly specified destination directory.

    Verifies that the project is started correctly in the provided destination directory.

    Args:
        script_runner (pytest.ScriptRunner): The pytest fixture to run CLI commands.
    """
    EXPLICIT = '/home/engineer/source/python/projects/Pyscaffold/tests/dummyprojects'
    ret = script_runner.run(['pyscaffold', 'start', 'projectA', '--destination', EXPLICIT])
    assert ret.success
    assert f"Starting project: Projecta at {EXPLICIT}" in ret.stdout

@pytest.mark.script_launch_mode('subprocess')
def test_start_command_with_bad_explicit_destination(script_runner):
    """
    Test the `start` command with an invalid explicitly specified destination directory.

    Ensures that an appropriate error message is displayed when the destination directory is not valid.

    Args:
        script_runner (pytest.ScriptRunner): The pytest fixture to run CLI commands.
    """
    BAD = '/mnt/c/Users/engineer/Document'
    ret = script_runner.run(['pyscaffold', 'start', 'projectA', '--destination', BAD])
    assert not ret.success
    assert "The provided destination directory is not valid." in ret.stderr

@pytest.mark.script_launch_mode('subprocess')
def test_resume_existing_project(script_runner, monkeypatch):
    """
    Test the `resume` command for an existing project.

    Sets up a dummy project, initializes a virtual environment, and verifies that the project is resumed correctly.
    Checks for the presence of a marker file indicating the successful resume of the project.

    Args:
        script_runner (pytest.ScriptRunner): The pytest fixture to run CLI commands.
        monkeypatch (pytest.MonkeyPatch): The pytest fixture to modify environment variables.
    """
    # this test requires the absolute path to the tests directory
    dummy_projects_dir = Config().get_tests_directory_path()
    
    project_name = "TestProject"
    project_path = Path(dummy_projects_dir) / project_name

    # Setup: Create a dummy project directory with setup.py and venv
    project_path.mkdir(parents=True, exist_ok=True)
    (project_path / 'setup.py').touch()

    # Turn on test mode to get marker file
    monkeypatch.setenv('ON_TEST', '1')
    import os
    assert os.getenv('ON_TEST') is not None

    # Initialize virtual environment for testing
    subprocess.run(["python3", "-m", "venv", project_path / 'venv'], check=True)

    activate_script = project_path / 'venv' / 'bin' / 'activate'
    assert activate_script.exists(), f"Expected activate script at {activate_script} not found."

    ret = script_runner.run(['pyscaffold', 'resume', "test_project", '--destination', str(dummy_projects_dir)])
    monkeypatch.delenv('ON_TEST', raising=False)
    assert os.getenv('ON_TEST') is None
    assert ret.success

    # Check if the marker file is created
    marker_file = project_path / 'venv_activated.marker'
    assert marker_file.exists()