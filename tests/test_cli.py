"""
Pyscaffold Test CLI

This module contains tests for the Pyscaffold CLI.

"""
import shutil
import subprocess
from pathlib import Path

import pytest

from pyscaffold.config import Config

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
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
    result = script_runner.run(['pyscaffold', '--help'])
    assert result.success
    assert 'usage' in result.stdout
    assert result.stderr == ''

@pytest.mark.script_launch_mode('subprocess')
def test_cli_version(script_runner):
    result = script_runner.run(['pyscaffold', '--version'])
    assert result.success
    assert '1.0.0' in result.stdout  # Adjust based on your actual version
    assert result.stderr == ''

@pytest.mark.script_launch_mode('subprocess')
def test_start_command_with_one_project(script_runner, setup_and_teardown):
    dummy_projects_dir = setup_and_teardown
    ret = script_runner.run(['pyscaffold', 'start', 'project_a', '--destination', str(dummy_projects_dir)])
    assert ret.success
    assert f"Starting project: ProjectA at {dummy_projects_dir}" in ret.stdout

@pytest.mark.script_launch_mode('subprocess')
def test_start_command_two_projects(script_runner, setup_and_teardown):
    dummy_projects_dir = setup_and_teardown
    ret = script_runner.run(['pyscaffold', 'start', 'projectA', 'projectB', '--destination', str(dummy_projects_dir)])
    assert ret.success
    assert f"Starting project: Projecta at {dummy_projects_dir}" in ret.stdout
    assert f"Starting project: Projectb at {dummy_projects_dir}" in ret.stdout

@pytest.mark.script_launch_mode('subprocess')
def test_start_command_with_good_explicit_destination(script_runner):
    EXPLICIT = '/mnt/c/Users/engineer/source/python/Pyscaffold/tests/dummyprojects'
    ret = script_runner.run(['pyscaffold', 'start', 'projectA', '--destination', EXPLICIT])
    assert ret.success
    assert f"Starting project: Projecta at {EXPLICIT}" in ret.stdout

@pytest.mark.script_launch_mode('subprocess')
def test_start_command_with_bad_explicit_destination(script_runner):
    BAD = '/mnt/c/Users/engineer/Document'
    ret = script_runner.run(['pyscaffold', 'start', 'projectA', '--destination', BAD])
    assert not ret.success
    assert "The provided destination directory is not valid." in ret.stderr

@pytest.mark.script_launch_mode('subprocess')
def test_resume_existing_project(script_runner, monkeypatch):
    # this test requires the absolute path to the tests directory
    dummy_projects_dir = Config().get_tests_directory_path(abs=True)
    
    project_name = "TestProject"
    project_path = Path(dummy_projects_dir) / project_name

    # Setup: Create a dummy project directory with setup.py and venv
    project_path.mkdir(parents=True, exist_ok=True)
    (project_path / 'setup.py').touch()
    #(project_path / 'venv').mkdir(parents=True, exist_ok=True)

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