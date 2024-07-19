import pytest
import shutil
import subprocess
from pathlib import Path

from pyscaffold.pyscaffold import Pyscaffold
from pyscaffold.config import Config

@pytest.fixture(scope="function")
def setup_and_teardown():
    dummy_projects_dir = Config.get_config_value_by_variable_name('TEST_PROJECTS')
    project_path = dummy_projects_dir / "TestProject"

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

def test_start():
    pass

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

@pytest.mark.script_launch_mode('subprocess')
def test_resume_non_existing_project(setup_and_teardown):
    dummy_projects_dir, _ = setup_and_teardown

    with pytest.raises(FileNotFoundError):
        Pyscaffold.resume("NonExistentProject", str(dummy_projects_dir))

@pytest.mark.script_launch_mode('subprocess')
def test_resume_invalid_project(setup_and_teardown):
    dummy_projects_dir, _ = setup_and_teardown
    invalid_project_name = "InvalidProject"
    invalid_project_path = dummy_projects_dir / invalid_project_name

    # Setup: Create an invalid project directory (without setup.py and venv)
    invalid_project_path.mkdir(parents=True, exist_ok=True)

    with pytest.raises(ValueError):
        Pyscaffold.resume(invalid_project_name, str(dummy_projects_dir))