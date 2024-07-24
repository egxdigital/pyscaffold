"""
Pyscaffold Test Configuration

This module contains tests for the Pyscaffold configuration settings.

"""
import pytest
from pathlib import Path
from pyscaffold.config import Config

sample_config = """
locations:
  PROJECTS: /mnt/c/Users/engineer/source/python
  TEST_PROJECTS: tests/dummyprojects
"""

@pytest.fixture(scope="module")
def config_file(tmp_path_factory):
    config_path = tmp_path_factory.mktemp("data") / "config.yaml"
    with open(config_path, 'w') as f:
        f.write(sample_config)
    return config_path

def test_load_from_file(config_file):
    config = Config(config_file)
    assert config.get("locations.PROJECTS") == "/mnt/c/Users/engineer/source/python"
    assert config.get("locations.TEST_PROJECTS") == "tests/dummyprojects"

def test_get_existing_key(config_file):
    config = Config(config_file)
    assert config.get("locations.PROJECTS") == "/mnt/c/Users/engineer/source/python"

def test_get_non_existing_key(config_file):
    config = Config(config_file)
    assert config.get("non.existing.key") is None
    assert config.get("non.existing.key", "default_value") == "default_value"

def test_add_setting(config_file):
    config = Config(config_file)
    config.add_setting("new_setting", key1="value1", key2="value2")
    assert config.get("new_setting.key1") == "value1"
    assert config.get("new_setting.key2") == "value2"

def test_update_setting(config_file):
    config = Config(config_file)
    config.add_setting("update_setting", key1="value1")
    config.update_setting("update_setting", key1="new_value", key2="value2")
    assert config.get("update_setting.key1") == "new_value"
    assert config.get("update_setting.key2") == "value2"

def test_get_projects_directory_path(config_file):
    config = Config(config_file)
    path = config.get_projects_directory_path()
    assert path == Path("/mnt/c/Users/engineer/source/python")
    assert path.exists()  # Ensure this path exists in your environment for the test to pass

def test_get_tests_directory_path(config_file):
    config = Config(config_file)
    path = config.get_tests_directory_path()
    assert path == Path("tests/dummyprojects")
    assert path.exists()  # Ensure this path exists in your environment for the test to pass

def test_get_tests_directory_path_abs(config_file):
    config = Config(config_file)
    path = config.get_tests_directory_path(abs=True)
    assert path == Path(__file__).resolve().parent.parent / "tests/dummyprojects"
    assert path.exists()  # Ensure this path exists in your environment for the test to pass

def test_invalid_get_projects_directory_path(config_file):
    config = Config(config_file)
    config.update_setting("locations", PROJECTS="/invalid/path")
    with pytest.raises(ValueError, match="Projects directory has not been set."):
        config.get_projects_directory_path()

def test_invalid_get_tests_directory_path(config_file):
    config = Config(config_file)
    config.update_setting("locations", TEST_PROJECTS="invalid/tests/dummyprojects")
    with pytest.raises(ValueError, match="Tests directory does not exist."):
        config.get_tests_directory_path()

if __name__ == "__main__":
    pytest.main()
