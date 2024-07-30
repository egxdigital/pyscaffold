"""
Pyscaffold Tests

This module contains tests for the Pyscaffold class.

"""
import pytest
import shutil
import subprocess
from unittest import mock
from pathlib import Path


from pyscaffold.config import Config
from pyscaffold.pyscaffold import Pyscaffold
from pyscaffold import helpers
from pyscaffold import utils

REASON="Time consuming test. Skipping for now"

@pytest.fixture(scope="function")
def setup_and_teardown():
    dummy_projects_dir = Config().get_tests_directory_path()
    project_path = dummy_projects_dir / "TestProject"

    # Setup: Create a dummy project directory with setup.py and venv
    project_path.mkdir(parents=True, exist_ok=True)
    (project_path / 'setup.py').touch()
    (project_path / 'venv').mkdir(parents=True, exist_ok=True)
    (project_path / 'venv' / 'bin').mkdir(parents=True, exist_ok=True)
    (project_path / 'venv' / 'bin' / 'activate').touch()

    yield dummy_projects_dir, project_path

    # Teardown: Clean up the dummy project directory
    for item in dummy_projects_dir.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

@pytest.fixture
def setup_venv_test():
    test_path = Path('/tmp/test_project')
    test_path.mkdir(parents=True, exist_ok=True)
    
    yield test_path

    for item in test_path.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

def test_create_project_folder(setup_and_teardown):
    dummy_projects_dir, _ = setup_and_teardown
    project_name = "NewTestProject"

    project_path = Pyscaffold.create_project_folder(project_name, str(dummy_projects_dir))

    # Verify that the project folder was created
    assert project_path.exists()
    assert project_path.is_dir()
    assert project_path.name == project_name

def test_create_project_folder_already_exists(setup_and_teardown):
    dummy_projects_dir, project_path = setup_and_teardown
    project_name = project_path.name

    with pytest.raises(FileExistsError):
        Pyscaffold.create_project_folder(project_name, str(dummy_projects_dir))

def test_create_project_folder_invalid_path():
    invalid_destination = "/invalid/path"
    project_name = "InvalidProject"

    with pytest.raises(OSError):
        Pyscaffold.create_project_folder(project_name, invalid_destination)

def test_inject_basic_package_contents(setup_and_teardown):
    _, project_path = setup_and_teardown
    package_name = "test_package"
    package_path = project_path / package_name
    package_path.mkdir(parents=True, exist_ok=True)

    Pyscaffold.inject_basic_package_contents("TestProject", package_name, package_path)
    
    for filename_template in Pyscaffold.basic_package_content_map:
        filename = filename_template.format(packagename=package_name)
        assert (package_path / filename).exists(), f"{filename} was not created in the package directory"

def test_deploy_basic_project_package(setup_and_teardown):
    dummy_projects_dir, project_path = setup_and_teardown
    project_name = "TestProject"

    package_name, package_path = Pyscaffold.deploy_basic_project_package(project_name, project_path)

    assert package_path.exists(), "Package path does not exist"
    assert (package_path / "__init__.py").exists(), "__init__.py was not created in the package directory"

    for filename_template in Pyscaffold.basic_package_content_map:
        filename = filename_template.format(packagename=package_name)
        assert (package_path / filename).exists(), f"{filename} was not created in the package directory"

def test_deploy_basic_project_package_error_handling(setup_and_teardown):
    _, project_path = setup_and_teardown
    project_name = "TestProject"
    
    # Create a file with the same name as a package to trigger an error
    package_name = helpers.apply_package_naming_convention(project_name)
    (project_path / package_name).touch()

    with pytest.raises(Exception):
        Pyscaffold.deploy_basic_project_package(project_name, project_path)

def test_inject_basic_test_package_contents(setup_and_teardown):
    _, project_path = setup_and_teardown
    test_package_name = "tests"
    test_package_path = project_path / test_package_name
    test_package_path.mkdir(parents=True, exist_ok=True)

    Pyscaffold.inject_basic_test_package_contents("TestProject", test_package_name, test_package_path)
    
    for filename_template in Pyscaffold.basic_test_package_content_map:
        filename = filename_template.format(packagename=test_package_name)
        assert (test_package_path / filename).exists(), f"{filename} was not created in the test package directory"

def test_deploy_basic_tests_package(setup_and_teardown):
    _, project_path = setup_and_teardown
    project_name = "TestProject"
    package_name = helpers.apply_package_naming_convention(project_name)

    _, test_package_path = Pyscaffold.deploy_basic_tests_package(project_name, project_path)

    assert test_package_path.exists(), "Test package path does not exist"
    assert (test_package_path / "__init__.py").exists(), "__init__.py was not created in the test package directory"

    for filename_template in Pyscaffold.basic_test_package_content_map:
        filename = filename_template.format(packagename=package_name)
        assert (test_package_path / filename).exists(), f"{filename} was not created in the test package directory"

def test_deploy_basic_tests_package_error_handling(setup_and_teardown):
    dummy_projects_dir, project_path = setup_and_teardown
    project_name = "TestProject"
    
    # Create a file with the same name as the test package to trigger an error
    test_package_name = "tests"
    (project_path / test_package_name).touch()

    with pytest.raises(Exception):
        Pyscaffold.deploy_basic_tests_package(project_name, project_path)

def test_inject_basic_project_contents(setup_and_teardown):
    _, project_path = setup_and_teardown
    project_name = "TestProject"

    Pyscaffold.inject_basic_project_contents(project_name, project_path)

    for filename in Pyscaffold.basic_project_content_map:
        assert (project_path / filename).exists(), f"{filename} was not created in the project directory"
        with open(project_path / filename, "r", encoding="utf-8") as f:
            content = f.read()
            expected_content = Pyscaffold.basic_project_content_map[filename].format(ProjectName=project_name, packagename=project_name)
            assert content == expected_content, f"Content of {filename} does not match expected content"

def test_inject_basic_project_contents_error_handling(setup_and_teardown):
    _, project_path = setup_and_teardown
    project_name = "TestProject"

    # Make one of the files read-only to trigger an error
    readonly_file = project_path / 'setup.py'
    readonly_file.touch()
    readonly_file.chmod(0o444)

    with pytest.raises(Exception):
        Pyscaffold.inject_basic_project_contents(project_name, project_path)

    # Reset permissions for cleanup
    readonly_file.chmod(0o666)

def test_inject_gitignore(setup_and_teardown):
    _, project_path = setup_and_teardown
    
    # Ensure the data directory and gitignore file exist
    data_dir = Path(__file__).parent.parent / 'data'
    gitignore_file = data_dir / 'gitignore-python'
    
    assert gitignore_file.exists()
    
    # Call the method
    Pyscaffold.inject_gitignore(project_path)
    
    # Check if .gitignore is created and has the expected content
    gitignore_path = project_path / '.gitignore'
    assert gitignore_path.exists()
    
    with open(gitignore_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    with open(gitignore_file, 'r', encoding='utf-8') as f:
        expected_content = f.read()
    
    assert content == expected_content

#@pytest.mark.skip(reason=REASON)
def test_deploy_virtual_environment(setup_venv_test):
    project_path = setup_venv_test
    python_version = '3.11'  # adjust based on the available Python version in your system

    Pyscaffold.deploy_virtual_environment(project_path, python_version)
    
    venv_path = project_path / 'env'
    assert venv_path.exists()
    assert (venv_path / 'bin' / 'python').exists()

#@pytest.mark.skip(reason=REASON)
def test_deploy_virtual_environment_invalid_python(setup_venv_test):
    project_path = setup_venv_test
    invalid_python_version = '9.9'  # assuming this version does not exist

    with mock.patch('shutil.which', return_value=None):
        with pytest.raises(RuntimeError, match=f'Python {invalid_python_version} is not installed or not found in PATH.'):
            Pyscaffold.deploy_virtual_environment(project_path, invalid_python_version)

#@pytest.mark.skip(reason=REASON)
@pytest.mark.script_launch_mode('subprocess')
def test_start_creates_project_structure(setup_and_teardown, monkeypatch):
    dummy_projects_dir, _ = setup_and_teardown
    project_name = 'AnotherTestProject'
    project_path = dummy_projects_dir / project_name    
    python_version = '3.11'  # Adjust according to available versions on your system

    monkeypatch.setenv('ON_TEST', '1')
    
    Pyscaffold.start([project_name], python_version, destination=str(dummy_projects_dir))

    # Verify project structure
    assert (project_path / 'setup.py').exists()
    assert (project_path / 'tests').exists()
    assert (project_path / 'env').exists()

    marker_file = project_path / 'venv_activated.marker'
    assert marker_file.exists()

    monkeypatch.delenv('ON_TEST', raising=False)

#@pytest.mark.skip(reason=REASON)
@pytest.mark.script_launch_mode('subprocess')
def test_start_with_invalid_python_version(setup_and_teardown, monkeypatch):
    dummy_projects_dir, _ = setup_and_teardown
    project_name = 'AnotherTestProject'
    invalid_python_version = '9.9'  # Assuming this version does not exist

    monkeypatch.setenv('ON_TEST', '1')

    with mock.patch('shutil.which', return_value=None):
        with pytest.raises(RuntimeError, match=f"Python {invalid_python_version} is not installed or not found in PATH."):
            Pyscaffold.start([project_name], invalid_python_version, destination=str(dummy_projects_dir))
    
    monkeypatch.delenv('ON_TEST', raising=False)

#@pytest.mark.skip(reason=REASON)
@pytest.mark.script_launch_mode('subprocess')
def test_start_handles_exception(setup_and_teardown, monkeypatch):
    dummy_projects_dir, _ = setup_and_teardown
    project_name = 'AnotherTestProject'
    python_version = '3.11'  # Adjust according to available versions on your system

    monkeypatch.setenv('ON_TEST', '1')

    # Mocking methods to raise an exception
    with mock.patch('pyscaffold.pyscaffold.Pyscaffold.create_project_folder', side_effect=Exception("Mocked exception")):
        result = Pyscaffold.start([project_name], python_version, destination=str(dummy_projects_dir))
    
    assert result is True  # Method returns True despite the error
    monkeypatch.delenv('ON_TEST', raising=False)

#@pytest.mark.skip(reason=REASON)
@pytest.mark.script_launch_mode('subprocess')
def test_resume_existing_project(setup_and_teardown, monkeypatch):
    dummy_projects_dir, project_path = setup_and_teardown
    project_name = Path(project_path).stem

    # Turn on test mode to get marker file
    monkeypatch.setenv('ON_TEST', '1')

    # Initialize virtual environment for testing
    subprocess.run(["python3", "-m", "venv", project_path / 'venv'], check=True)

    #ret = script_runner.run(['pyscaffold', 'resume', project_name, '--destination', str(dummy_projects_dir)])
    ret = Pyscaffold.resume(project_name, dummy_projects_dir)
    monkeypatch.delenv('ON_TEST', raising=False)

    assert ret is True

    # Check if the marker file is created
    marker_file = project_path / 'venv_activated.marker'
    assert marker_file.exists()

#@pytest.mark.skip(reason=REASON)
@pytest.mark.script_launch_mode('subprocess')
def test_resume_non_existing_project(setup_and_teardown):
    dummy_projects_dir, _ = setup_and_teardown

    with pytest.raises(FileNotFoundError):
        Pyscaffold.resume("NonExistentProject", str(dummy_projects_dir))

#@pytest.mark.skip(reason=REASON)
@pytest.mark.script_launch_mode('subprocess')
def test_resume_invalid_project(setup_and_teardown):
    dummy_projects_dir, _ = setup_and_teardown
    invalid_project_name = "InvalidProject"
    invalid_project_path = dummy_projects_dir / invalid_project_name

    # Setup: Create an invalid project directory (without setup.py and venv)
    invalid_project_path.mkdir(parents=True, exist_ok=True)

    with pytest.raises(ValueError):
        Pyscaffold.resume(invalid_project_name, str(dummy_projects_dir))