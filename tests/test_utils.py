"""
Pyscaffold Test Utilities

This module contains tests for the utility functions used in the Pyscaffold 
application. It includes fixtures and test cases for various functions 
related to project management and argument preprocessing.

"""
import shutil
from pathlib import Path
from unittest import mock
from argparse import Namespace

import pytest

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
    """
    Fixture to set up and tear down a dummy project environment for testing.

    This fixture creates a dummy project directory with necessary files and 
    directories for testing. After the tests are complete, it cleans up by 
    removing the created files and directories.

    Yields:
        tuple: Contains the path to the dummy projects directory, the path to 
        the dummy project, and the Config instance used for testing.
    """
    config = Config()
    dummy_projects_dir = config.get_tests_directory_path()
    Path(dummy_projects_dir).mkdir(parents=True, exist_ok=True)

    project_path =  dummy_projects_dir / "TestProject"

    # Setup: Create a dummy project directory with setup.py and venv
    project_path.mkdir(parents=True, exist_ok=True)
    (project_path / 'setup.py').touch()
    (project_path / 'venv').mkdir(parents=True, exist_ok=True)
    (project_path / 'venv' / 'bin').mkdir(parents=True, exist_ok=True)
    (project_path / 'venv' / 'bin' / 'activate').touch()

    yield dummy_projects_dir, project_path, config

    # Teardown: Clean up the dummy project directory    
    for item in dummy_projects_dir.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

def test_project_exists(setup_and_teardown):
    """
    Test the project_exists function.

    This test verifies if the project_exists function correctly identifies 
    whether a specified project directory exists.

    Args:
        setup_and_teardown (tuple): The fixture providing paths and config.
    """
    dummy_projects_dir, __, _ = setup_and_teardown
    assert project_exists("TestProject", dummy_projects_dir) == True
    assert project_exists("nonexistent_project", dummy_projects_dir) == False

def test_project_ready(setup_and_teardown):
    """
    Test the project_ready function.

    This test checks if the project_ready function correctly determines if a 
    project directory is ready by verifying the presence of 'setup.py' and 
    a virtual environment.

    Args:
        setup_and_teardown (tuple): The fixture providing paths and config.
    """
    _, project_path, _ = setup_and_teardown
    assert project_ready(project_path) == True
    (project_path / 'setup.py').unlink()
    assert project_ready(project_path) == False

def test_change_directory(setup_and_teardown):
    """
    Test the change_directory function.

    This test ensures that the change_directory function calls os.chdir with 
    the correct path.

    Args:
        setup_and_teardown (tuple): The fixture providing paths and config.
    """
    _, project_path, _ = setup_and_teardown
    with mock.patch('os.chdir') as mock_chdir:
        change_directory(project_path)
        mock_chdir.assert_called_once_with(project_path)

def test_set_destination_with_valid_destination(setup_and_teardown):
    """
    Test set_destination with a valid destination directory.

    This test verifies that the set_destination function correctly sets the 
    destination when a valid directory is provided.

    Args:
        setup_and_teardown (tuple): The fixture providing paths and config.
    """
    __, project_path, _ = setup_and_teardown
    args = Namespace(destination=str(project_path))
    set_destination(args)
    assert args.destination == str(project_path)

def test_set_destination_with_invalid_destination():
    """
    Test set_destination with an invalid destination directory.

    This test ensures that set_destination raises a ValueError when an invalid 
    directory is provided.

    Raises:
        ValueError: If the destination directory is not valid.
    """
    args = Namespace(destination='/invalid/path')

    with pytest.raises(ValueError, match="The provided destination directory is not valid."):
        set_destination(args)

def test_set_destination_with_no_destination_and_on_test(monkeypatch, setup_and_teardown):
    """
    Test set_destination when no destination is provided and ON_TEST is set.

    This test checks if set_destination correctly uses the test directory path 
    when the ON_TEST environment variable is set.

    Args:
        monkeypatch (MonkeyPatch): Pytest monkeypatch fixture.
        setup_and_teardown (tuple): The fixture providing paths and config.
    """
    dummy_projects_dir, __, _ = setup_and_teardown
    monkeypatch.setenv('ON_TEST', '1')
    args = Namespace(destination=None)
    assert args.destination is None
    set_destination(args)
    monkeypatch.delenv('ON_TEST', raising=False)
    assert args.destination == dummy_projects_dir

def test_set_destination_with_no_destination_and_not_on_test(monkeypatch, setup_and_teardown):
    """
    Test set_destination when no destination is provided and ON_TEST is not set.

    This test ensures that set_destination uses the projects directory path 
    from the config when ON_TEST is not set.

    Args:
        monkeypatch (MonkeyPatch): Pytest monkeypatch fixture.
        setup_and_teardown (tuple): The fixture providing paths and config.
    """
    ___, __, config = setup_and_teardown
    monkeypatch.delenv('ON_TEST', raising=False)
    args = Namespace(destination=None)
    set_destination(args)
    assert args.destination == config.get_projects_directory_path()

def test_set_destination_with_no_destination_and_invalid_projects_dir(monkeypatch, setup_and_teardown):
    """
    Test set_destination with no destination and an invalid projects directory.

    This test verifies that set_destination raises a ValueError when the config 
    provides an invalid projects directory path.

    Args:
        monkeypatch (MonkeyPatch): Pytest monkeypatch fixture.
        setup_and_teardown (tuple): The fixture providing paths and config.
    """
    ___, __, config = setup_and_teardown
    monkeypatch.delenv('ON_TEST', raising=False)
    invalid_projects_dir = '/invalid/projects/path'

    from pathlib import Path

    # Create a mock Config class that returns the desired settings
    class MockConfig:
        def __init__(self):
            self.settings = {
                'locations': {
                    'PROJECTS': invalid_projects_dir
                }
            }

        def get_tests_directory_path(self):
            return Path(self.settings['locations']['PROJECTS'])

        def get_projects_directory_path(self):
            return Path(self.settings['locations']['PROJECTS'])

        def get(self, key, default=None):
            keys = key.split('.')
            value = self.settings
            for k in keys:
                if isinstance(value, dict):
                    value = value.get(k, default)
                else:
                    return default
            return value

    # Replace the Config class in the utils module with the mock version
    monkeypatch.setattr('pyscaffold.utils.Config', MockConfig)
    
    args = Namespace(destination=None)

    with pytest.raises(ValueError, match=f"A valid destination directory must be provided either via --destination or by setting the value in config.yaml"):
        set_destination(args)

def test_apply_naming_conventions_single_name():
    """
    Test apply_naming_conventions with a single project name.

    This test checks if the apply_naming_conventions function correctly applies 
    naming conventions to a single project name.

    Args:
        None
    """
    args = Namespace(project_name='testproject')
    apply_naming_conventions(args)
    assert args.project_name == 'Testproject'

def test_apply_naming_conventions_multiple_names():
    """
    Test apply_naming_conventions with multiple project names.

    This test ensures that apply_naming_conventions correctly applies naming 
    conventions to a list of project names.

    Args:
        None
    """
    args = Namespace(project_names=['testproject1', 'testproject2'])
    apply_naming_conventions(args)
    assert args.project_names == ['Testproject1', 'Testproject2']

def test_preprocess_arguments_valid_destination(setup_and_teardown):
    """
    Test preprocess_arguments with a valid destination directory.

    This test verifies that preprocess_arguments correctly processes the destination 
    when a valid directory is provided.

    Args:
        setup_and_teardown (tuple): The fixture providing paths and config.
    """
    dummy_projects_dir, __, _ = setup_and_teardown
    args = Namespace()
    args.destination = dummy_projects_dir
    preprocess_arguments(args)
    assert args.destination == dummy_projects_dir

def test_preprocess_arguments_env_variable(setup_and_teardown, monkeypatch):
    """
    Test preprocess_arguments when ON_TEST environment variable is set.

    This test checks if preprocess_arguments correctly uses the test directory path 
    when ON_TEST is set.

    Args:
        monkeypatch (MonkeyPatch): Pytest monkeypatch fixture.
        setup_and_teardown (tuple): The fixture providing paths and config.
    """
    dummy_projects_dir, __, _ = setup_and_teardown
    monkeypatch.setenv('ON_TEST', '1')
    args = Namespace()
    preprocess_arguments(args)
    monkeypatch.delenv('ON_TEST', raising=False)
    assert args.destination == dummy_projects_dir

def test_preprocess_arguments_invalid_destination():
    """
    Test preprocess_arguments with an invalid destination directory.

    This test ensures that preprocess_arguments raises a ValueError when an invalid 
    directory is provided.

    Args:
        None
    """
    args = Namespace()
    args.destination = '/invalid/path'
    with pytest.raises(ValueError, match="The provided destination directory is not valid."):
        preprocess_arguments(args)

def test_preprocess_arguments_project_names():
    """
    Test preprocess_arguments with a list of project names.

    This test verifies that preprocess_arguments applies naming conventions to 
    a list of project names.

    Args:
        None
    """
    args = Namespace()
    args.project_names = ["projectA", "myProject", "anotherProject"]
    preprocess_arguments(args)
    assert args.project_names == ["Projecta", "Myproject", "Anotherproject"]

def test_preprocess_arguments_project_name():
    """
    Test preprocess_arguments with a single project name.

    This test checks if preprocess_arguments correctly applies naming conventions 
    to a single project name.

    Args:
        None
    """
    args = Namespace()
    args.project_name = "projectA"
    preprocess_arguments(args)
    assert args.project_name == "Projecta"

@mock.patch("subprocess.run")
def test_activate_virtual_env(mock_subprocess_run, setup_and_teardown, monkeypatch):
    """
    Test activate_virtual_env in test mode.

    This test ensures that activate_virtual_env correctly calls subprocess.run 
    with the expected command when ON_TEST environment variable is set.

    Args:
        mock_subprocess_run (Mock): Mock object for subprocess.run.
        setup_and_teardown (tuple): The fixture providing paths and config.
        monkeypatch (MonkeyPatch): Pytest monkeypatch fixture.
    """
    dummy_projects_dir, project_path, _ = setup_and_teardown
    
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
    """
    Test activate_virtual_env in non-test mode.

    This test verifies that activate_virtual_env correctly calls execute_command 
    with the expected command when ON_TEST environment variable is not set.

    Args:
        mock_execute_command (Mock): Mock object for execute_command.
        setup_and_teardown (tuple): The fixture providing paths and config.
    """
    dummy_projects_dir, project_path, _ = setup_and_teardown
    
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