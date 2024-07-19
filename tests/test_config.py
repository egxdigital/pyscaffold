# In tests/test_config.py
import pytest
from pathlib import Path
from pyscaffold.config import Config

def test_get_config_value_by_variable_name_valid_absolute():
    # Test with a valid absolute path variable
    result = Config.get_config_value_by_variable_name('PROJECTS')
    expected = Path('/mnt/c/Users/engineer/source/python')
    assert result == expected

def test_get_config_value_by_variable_name_valid_relative():
    # Test with a valid relative path variable
    result = Config.get_config_value_by_variable_name('TEST_PROJECTS')
    expected = Path(__file__).resolve().parent.parent / 'tests/dummyprojects'
    assert result == expected

def test_get_config_value_by_variable_name_invalid():
    # Test with an invalid variable name
    with pytest.raises(KeyError, match="Not a valid variable name: INVALID_VAR"):
        Config.get_config_value_by_variable_name('INVALID_VAR')

def test_get_config_value_by_variable_name_nonexistent_path():
    # Test with a variable pointing to a nonexistent path
    Config.EXPLICIT_STRING_DEFS['NON_EXISTENT_PATH'] = {
        'pathname': 'non_existent_path',
        'description': 'Nonexistent path for testing',
        'is_relative': True
    }
    with pytest.raises(ValueError, match="Pathname setting for NON_EXISTENT_PATH is not valid"):
        Config.get_config_value_by_variable_name('NON_EXISTENT_PATH')

def test_compare_config_value_with_environment_variable_valid():
    # Test with a valid environment variable name and value
    result = Config.compare_config_value_with_environment_variable('PROJECTS', '/mnt/c/Users/engineer/source/python')
    assert result == True

def test_compare_config_value_with_environment_variable_invalid_name():
    # Test with an invalid environment variable name
    with pytest.raises(KeyError, match="Not a valid variable name: INVALID_VAR"):
        Config.compare_config_value_with_environment_variable('INVALID_VAR', 'some_value')

def test_compare_config_value_with_environment_variable_invalid_value():
    # Test with an invalid value for a valid environment variable name
    result = Config.compare_config_value_with_environment_variable('PROJECTS', 'invalid_value')
    assert result == False

if __name__ == "__main__":
    pytest.main()
