"""
Pyscaffold Test Configuration

This module contains tests for the `Pyscaffold` configuration settings. It verifies the functionality of loading configuration 
from a file, accessing existing and non-existing settings, and adding or updating configuration settings. Additionally, it 
tests the retrieval of project and test directory paths from the configuration and handles invalid scenarios.

Fixtures:
- config_file: Provides a temporary configuration file for the tests.

Tests:
- test_load_from_file: Verifies that configuration values can be correctly loaded from the file.
- test_get_existing_key: Checks that existing configuration keys return the correct values.
- test_get_non_existing_key: Ensures that non-existing keys return `None` or a default value.
- test_add_setting: Tests the addition of new settings to the configuration.
- test_update_setting: Verifies that existing settings can be updated correctly.
- test_get_projects_directory_path: Checks that the projects directory path is retrieved correctly from the configuration.
- test_get_tests_directory_path: Validates that the tests directory path is retrieved correctly.
- test_invalid_get_projects_directory_path: Tests the handling of an invalid projects directory path.
- test_invalid_get_tests_directory_path: Ensures proper error handling for an invalid tests directory path.
"""

import pytest
from pathlib import Path
from pyscaffold.config import Config

PROJECTS = "/home/engineer/source/python/projects"

sample_config = """
locations:
  PROJECTS: {projects}
  TEST_PROJECTS: tests/dummyprojects
""".format(projects=PROJECTS)

@pytest.fixture(scope="module")
def config_file(tmp_path_factory):
    """
    Fixture to create a temporary configuration file.

    This fixture sets up a temporary configuration file with sample settings for the duration of the test module. 

    Returns:
        Path: The path to the temporary configuration file.
    """
    config_path = tmp_path_factory.mktemp("data") / "config.yaml"
    with open(config_path, 'w') as f:
        f.write(sample_config)
    return config_path

def test_load_from_file(config_file):
    """
    Test loading configuration from a file.

    Validates that the configuration values for `PROJECTS` and `TEST_PROJECTS` are correctly loaded from the provided file.

    Args:
        config_file (Path): Path to the temporary configuration file.
    """
    config = Config(config_file)
    assert config.get("locations.PROJECTS") == PROJECTS
    assert config.get("locations.TEST_PROJECTS") == "tests/dummyprojects"

def test_get_existing_key(config_file):
    """
    Test retrieving an existing configuration key.

    Ensures that a key present in the configuration file returns the expected value.

    Args:
        config_file (Path): Path to the temporary configuration file.
    """
    config = Config(config_file)
    assert config.get("locations.PROJECTS") == PROJECTS

def test_get_non_existing_key(config_file):
    """
    Test retrieving a non-existing configuration key.

    Validates that a non-existing key returns `None` or a specified default value.

    Args:
        config_file (Path): Path to the temporary configuration file.
    """
    config = Config(config_file)
    assert config.get("non.existing.key") is None
    assert config.get("non.existing.key", "default_value") == "default_value"

def test_add_setting(config_file):
    """
    Test adding new settings to the configuration.

    Verifies that new settings can be added to the configuration and accessed correctly.

    Args:
        config_file (Path): Path to the temporary configuration file.
    """
    config = Config(config_file)
    config.add_setting("new_setting", key1="value1", key2="value2")
    assert config.get("new_setting.key1") == "value1"
    assert config.get("new_setting.key2") == "value2"

def test_update_setting(config_file):
    """
    Test updating existing configuration settings.

    Ensures that existing settings can be updated and that the updated values are correctly retrieved.

    Args:
        config_file (Path): Path to the temporary configuration file.
    """
    config = Config(config_file)
    config.add_setting("update_setting", key1="value1")
    config.update_setting("update_setting", key1="new_value", key2="value2")
    assert config.get("update_setting.key1") == "new_value"
    assert config.get("update_setting.key2") == "value2"

def test_get_projects_directory_path(config_file):
    """
    Test retrieving the projects directory path from configuration.

    Validates that the `PROJECTS` directory path is correctly retrieved and exists.

    Args:
        config_file (Path): Path to the temporary configuration file.
    """
    config = Config(config_file)
    path = config.get_projects_directory_path()
    assert path == Path(PROJECTS)
    assert path.exists()  # Ensure this path exists in your environment for the test to pass

def test_get_tests_directory_path(config_file):
    """
    Test retrieving the tests directory path from configuration.

    Validates that the `TEST_PROJECTS` directory path is correctly retrieved and exists.

    Args:
        config_file (Path): Path to the temporary configuration file.
    """
    config = Config(config_file)
    path = config.get_tests_directory_path()
    assert path == Path(__file__).resolve().parent.parent / "tests/dummyprojects"
    assert path.exists()  # Ensure this path exists in your environment for the test to pass

def test_invalid_get_projects_directory_path(config_file):
    """
    Test handling of an invalid projects directory path.

    Ensures that an invalid path for the projects directory raises a `ValueError` with the appropriate message.

    Args:
        config_file (Path): Path to the temporary configuration file.
    """
    config = Config(config_file)
    config.update_setting("locations", PROJECTS="/invalid/path")
    with pytest.raises(ValueError, match="Projects directory has not been set."):
        config.get_projects_directory_path()

def test_invalid_get_tests_directory_path(config_file):
    """
    Test handling of an invalid tests directory path.

    Ensures that an invalid path for the tests directory raises a `ValueError` with the appropriate message.

    Args:
        config_file (Path): Path to the temporary configuration file.
    """
    config = Config(config_file)
    config.update_setting("locations", TEST_PROJECTS="invalid/tests/dummyprojects")
    with pytest.raises(ValueError, match="Tests directory does not exist."):
        config.get_tests_directory_path()

if __name__ == "__main__":
    pytest.main()
