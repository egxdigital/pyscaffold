import shutil
from argparse import Namespace

import pytest
from unittest import mock

from pyscaffold.config import Config
from pyscaffold.utils import (
    activate_virtual_env, 
    project_exists, 
    project_ready, 
    change_directory,
    set_destination, 
    apply_naming_conventions,
    preprocess_arguments
)

@pytest.fixture(scope="function")
def setup_and_teardown():
    dummy_projects_dir = Config.get_config_value_by_variable_name('TEST_PROJECTS')

    project_path =  dummy_projects_dir / "TestProject"

    # Setup: Create a dummy project directory with setup.py and venv
    project_path.mkdir(parents=True, exist_ok=True)
    (project_path / 'setup.py').touch()
    (project_path / 'venv').mkdir(parents=True, exist_ok=True)
    (project_path / 'venv' / 'bin').mkdir(parents=True, exist_ok=True)
    (project_path / 'venv' / 'bin' / 'activate').touch()

    yield dummy_projects_dir, project_path

    # Teardown: Clean up the dummy project directory    
    for item in project_path.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()
    
    project_path.rmdir()

def test_project_exists(setup_and_teardown):
    dummy_projects_dir, project_path = setup_and_teardown
    assert project_exists("TestProject", dummy_projects_dir) == True
    assert project_exists("nonexistent_project", dummy_projects_dir) == False

def test_project_ready(setup_and_teardown):
    dummy_projects_dir, project_path = setup_and_teardown
    assert project_ready(project_path) == True
    (project_path / 'setup.py').unlink()
    assert project_ready(project_path) == False

def test_change_directory(setup_and_teardown):
    dummy_projects_dir, project_path = setup_and_teardown
    with mock.patch('os.chdir') as mock_chdir:
        change_directory(project_path)
        mock_chdir.assert_called_once_with(project_path)


def test_set_destination_with_valid_destination(setup_and_teardown):
    dummy_projects_dir, project_path = setup_and_teardown
    args = Namespace(destination=str(project_path))
    set_destination(args)
    assert args.destination == str(project_path)

def test_set_destination_with_invalid_destination():
    args = Namespace(destination='/invalid/path')

    with pytest.raises(ValueError, match="The provided destination directory is not valid."):
        set_destination(args)

def test_set_destination_with_no_destination_and_on_test(monkeypatch, setup_and_teardown):
    dummy_projects_dir, project_path = setup_and_teardown
    monkeypatch.setenv('ON_TEST', '1')
    args = Namespace(destination=None)
    assert args.destination == None
    set_destination(args)
    monkeypatch.delenv('ON_TEST', raising=False)
    assert args.destination == dummy_projects_dir

def test_set_destination_with_no_destination_and_not_on_test(monkeypatch, setup_and_teardown):
    dummy_projects_dir, project_path = setup_and_teardown
    monkeypatch.delenv('ON_TEST', raising=False)
    args = Namespace(destination=None)
    set_destination(args)
    assert args.destination == Config.get_config_value_by_variable_name('PROJECTS')

def test_set_destination_with_no_valid_destination(monkeypatch):
    monkeypatch.delenv('ON_TEST', raising=False)
    invalid_projects_dir = '/invalid/projects/path'
    monkeypatch.setattr(Config, 'EXPLICIT_STRING_DEFS', {
        'PROJECTS': {
            'pathname': invalid_projects_dir,
            'description': 'Invalid projects directory',
            'is_relative': False
        }
    })
    args = Namespace(destination=None)

    with pytest.raises(ValueError, match=f"Pathname setting for PROJECTS is not valid: {invalid_projects_dir}"):
        set_destination(args)

def test_apply_naming_conventions_single_name():
    args = Namespace(project_name='testproject')
    apply_naming_conventions(args)
    assert args.project_name == 'Testproject'

def test_apply_naming_conventions_multiple_names():
    args = Namespace(project_names=['testproject1', 'testproject2'])
    apply_naming_conventions(args)
    assert args.project_names == ['Testproject1', 'Testproject2']

def test_preprocess_arguments_valid_destination(setup_and_teardown):
    dummy_projects_dir, project_path = setup_and_teardown
    args = Namespace()
    args.destination = dummy_projects_dir
    preprocess_arguments(args)
    assert args.destination == dummy_projects_dir

def test_preprocess_arguments_env_variable(setup_and_teardown, monkeypatch):
    dummy_projects_dir, project_path = setup_and_teardown
    monkeypatch.setenv('ON_TEST', '1')
    args = Namespace()
    preprocess_arguments(args)
    monkeypatch.delenv('ON_TEST', raising=False)
    assert args.destination == dummy_projects_dir

def test_preprocess_arguments_invalid_destination():
    args = Namespace()
    args.destination = '/invalid/path'
    with pytest.raises(ValueError, match="The provided destination directory is not valid."):
        preprocess_arguments(args)

def test_preprocess_arguments_project_names():
    args = Namespace()
    args.project_names = ["projectA", "myProject", "anotherProject"]
    preprocess_arguments(args)
    assert args.project_names == ["Projecta", "Myproject", "Anotherproject"]

def test_preprocess_arguments_project_name():
    args = Namespace()
    args.project_name = "projectA"
    preprocess_arguments(args)
    assert args.project_name == "Projecta"

@mock.patch("subprocess.run")
def test_activate_virtual_env(mock_subprocess_run, setup_and_teardown, monkeypatch):
    dummy_projects_dir, project_path = setup_and_teardown
    
    # Mocking other utility functions
    with mock.patch("pyscaffold.utils.project_exists", return_value=True):
        with mock.patch("pyscaffold.utils.project_ready", return_value=True):
            with mock.patch("pyscaffold.utils.change_directory") as mock_change_dir:

                # Test the function in test mode
                monkeypatch.setenv('ON_TEST', '1')
                result = activate_virtual_env(project_path)

                # Check that subprocess.run was called with the correct command
                activate_script = project_path / 'venv' / 'bin' / 'activate'
                marker_file = project_path / 'venv_activated.marker'
                expected_command = f"source {activate_script} && touch {marker_file} && exit"
                mock_subprocess_run.assert_called_once_with(expected_command, shell=True, executable='/bin/bash', check=True)

                # Check that change_directory was called with the correct path
                mock_change_dir.assert_called_once_with(project_path)

                # Check the function result
                assert result == True
    monkeypatch.delenv('ON_TEST', raising=False)

@mock.patch("pyscaffold.utils.execute_command")
def test_activate_virtual_env_non_test(mock_execute_command, setup_and_teardown):
    dummy_projects_dir, project_path = setup_and_teardown
    
    # Mocking other utility functions if needed
    with mock.patch("pyscaffold.utils.project_exists", return_value=True):
        with mock.patch("pyscaffold.utils.project_ready", return_value=True):
            with mock.patch("pyscaffold.utils.change_directory") as mock_change_dir:

                # Mock the execute_command function
                mock_execute_command.return_value = True

                # Test the function in non-test mode
                result = activate_virtual_env(project_path)

                # Check that execute_command was called with the correct command
                activate_script = project_path / 'venv' / 'bin' / 'activate'
                expected_command = f"/bin/bash --rcfile {activate_script}"
                mock_execute_command.assert_called_once_with(expected_command)

                # Check that change_directory was called with the correct path
                mock_change_dir.assert_called_once_with(project_path)

                # Check the function result
                assert result == True

if __name__ == "__main__":
    pytest.main()