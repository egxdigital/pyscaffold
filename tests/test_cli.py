import subprocess
import shutil
from pathlib import Path

import pytest

from pyscaffold.config import Config

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    # Setup: Ensure the test directory exists
    dummy_projects_dir = Config.get_config_value_by_variable_name('TEST_PROJECTS')
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
    assert f"Starting project: Projecta at {dummy_projects_dir}\nStarting project: Projectb at {dummy_projects_dir}" in ret.stdout

@pytest.mark.script_launch_mode('subprocess')
def test_start_command_with_good_explicit_destination(script_runner):
    EXPLICIT = '/mnt/c/Users/engineer/Documents'
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
def test_resume_existing_project(script_runner, setup_and_teardown, monkeypatch):
    dummy_projects_dir = setup_and_teardown
    project_name = "TestProject"
    project_path = Path(dummy_projects_dir) / project_name

    # Setup: Create a dummy project directory with setup.py and venv
    project_path.mkdir(parents=True, exist_ok=True)
    (project_path / 'setup.py').touch()
    (project_path / 'venv').mkdir(parents=True, exist_ok=True)

    # Turn on test mode to get marker file
    monkeypatch.setenv('ON_TEST', '1')

    # Initialize virtual environment for testing
    subprocess.run(["python3", "-m", "venv", project_path / 'venv'], check=True)

    ret = script_runner.run(['pyscaffold', 'resume', project_name, '--destination', str(dummy_projects_dir)])
    monkeypatch.delenv('ON_TEST', raising=False)
    import os
    assert os.getenv('ON_TEST') == None
    assert ret.success

    # Check if the marker file is created
    marker_file = project_path / 'venv_activated.marker'
    assert marker_file.exists()