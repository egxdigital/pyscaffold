"""
Pyscaffold

This module contains the definition of the Pyscaffold class.

"""
import os
import shutil
import subprocess
from pathlib import Path
from typing import Tuple

from pyscaffold import helpers
from pyscaffold import fragments
from pyscaffold import utils

class Pyscaffold():
    basic_package_content_map = {
        '__main__.py': fragments.PKG_MAIN_PY,
        'utils.py': fragments.PKG_UTILS_PY,
        'config.py': fragments.PKG_CONFIG_PY,
        'helpers.py': fragments.PKG_HELPERS_PY,
        'arg_parser.py': fragments.PKG_ARG_PARSER_PY,
        '{packagename}.py': fragments.PKG_MODULE_PY
    }

    basic_test_package_content_map = {
        'test_config.py': fragments.TEST_CONFIG_PY,
        'test_helpers.py': fragments.TEST_HELPERS_PY,
        'test_utils.py': fragments.TEST_UTILS_PY,        
        'test_arg_parser.py': fragments.TEST_PKG_ARG_PARSER_PY,
        'test_cli.py': fragments.TEST_CLI_PY,
        'test_{packagename}.py': fragments.TEST_PACKAGE_MODULE_PY
    }

    basic_project_content_map = {
        'setup.py': fragments.PROJECT_SETUP_PY,
        'README.md': fragments.PROJECT_README_PY,
        'MANIFEST.in': fragments.PROJECT_MANIFEST_IN,
        'pytest.ini': fragments.PROJECT_PYTEST_INI,
        'LICENSE': fragments.PROJECT_LICENSE,
        'config.yaml': fragments.PROJECT_CONFIG_YAML
    }
    
    @staticmethod
    def create_project_folder(project_name: str, destination: str) -> Path:
        project_path = Path(destination) / project_name
        
        if project_path.exists():
            raise FileExistsError(f"The project folder '{project_path}' already exists.")
        
        if not os.path.isdir(destination):
            raise OSError(f"The destination path '{destination}' is invalid.")

        project_path.mkdir(parents=True, exist_ok=True)
        return project_path
     
    @staticmethod
    def inject_basic_package_contents(project_name: str, package_name: str, package_path: Path):
        for filename_template, content in Pyscaffold.basic_package_content_map.items():
            filename = filename_template.format(packagename=package_name)
            try:
                with open(package_path / filename, "w", encoding="utf-8") as f:
                    f.write(content.format(ProjectName=project_name, packagename=package_name))
            except Exception as e:
                print(f"Error writing file {filename}: {e}")
                raise

    @staticmethod
    def deploy_basic_project_package(project_name: str, project_location: Path) -> Tuple[str, Path]:
        """Deploy a basic package within a project directory."""
        try:
            package_name = helpers.apply_package_naming_convention(project_name)
            package_path = Path(project_location) / package_name
            package_path.mkdir(parents=True, exist_ok=True)
            
            # Create __init__.py file
            with open(package_path / "__init__.py", "w", encoding="utf-8") as f:
                f.write("")
            
            # Deploy package content
            Pyscaffold.inject_basic_package_contents(project_name, package_name, package_path)
        
        except Exception as e:
            print(f"Error deploying basic project package: {e}")
            raise
        
        return package_name, package_path

    @staticmethod
    def inject_basic_test_package_contents(project_name: str, test_package_name: str, test_package_path: Path):
        for filename_template, content in Pyscaffold.basic_test_package_content_map.items():
            filename = filename_template.format(packagename=test_package_name)
            try:
                with open(test_package_path / filename, "w", encoding="utf-8") as f:
                    f.write(content.format(ProjectName=project_name, packagename=test_package_name))
            except Exception as e:
                print(f"Error writing file {filename}: {e}")
                raise
    
    @staticmethod
    def deploy_basic_tests_package(project_name: str, project_location: Path) -> Tuple[str, Path]:
        """Deploy a basic test package within a project directory."""
        try:
            test_package_name = "tests"
            test_package_path = Path(project_location) / test_package_name
            test_package_path.mkdir(parents=True, exist_ok=True)

            # Create __init__.py file
            with open(test_package_path / "__init__.py", "w", encoding="utf-8") as f:
                f.write("")

            # Deploy package content
            package_name = helpers.apply_package_naming_convention(project_name)
            Pyscaffold.inject_basic_test_package_contents(project_name, package_name, test_package_path)

        except Exception as e:
            print(f"Error deploying basic test package: {e}")
            raise

        return test_package_name, test_package_path
        
    @staticmethod
    def inject_basic_project_contents(project_name: str, project_path: Path) -> None:
        for filename, content in Pyscaffold.basic_project_content_map.items():
            try:
                with open(project_path / filename, "w", encoding="utf-8") as f:
                    f.write(content.format(ProjectName=project_name, packagename=project_name))
            except Exception as e:
                print(f"Error writing file {filename}: {e}")
                raise
    
    @staticmethod
    def inject_gitignore(project_path: Path) -> None:
        data_directory = Path(__file__).parent.parent / 'data'
        gitignore_path = data_directory / 'gitignore-python'
        
        try:
            # Read the content of gitignore file
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                gitignore_content = f.read()
            
            # Write content to .gitignore in the project directory
            with open(project_path / '.gitignore', 'w', encoding='utf-8') as f:
                f.write(gitignore_content)
        
        except PermissionError as e:
            # Specific handling for permission errors
            raise PermissionError(f"Permission error: {e}")
        except FileNotFoundError as e:
            # Handle case where the gitignore file does not exist
            raise FileNotFoundError(f"File not found: {e}")
        except Exception as e:
            # General exception handling
            raise RuntimeError(f"Unexpected error: {e}")
    
    @staticmethod
    def deploy_virtual_environment(project_path: Path, python_version: str = '3.11') -> bool:
        venv_path = project_path / 'env'
        python_executable = f'python{python_version}'

        if not shutil.which(python_executable):
            raise RuntimeError(f'Python {python_version} is not installed or not found in PATH.')

        try:
            subprocess.run([python_executable, '-m', 'venv', str(venv_path)], check=True)
            print(f"Virtual environment created at {venv_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error creating virtual environment: {e}")
            raise
        
        return True
    
    @staticmethod
    def start(project_names, python_version, **kwargs):
        destination = kwargs.get('destination', None)
        
        for project_name in project_names:
            try:
                project_path = Pyscaffold.create_project_folder(project_name, destination)

                if project_path:
                    print(f"Starting project: {project_name} at {project_path}")
                else:
                    print(f"Failed to create project folder for '{project_name}'.")

                Pyscaffold.deploy_basic_project_package(project_name, project_path)

                Pyscaffold.deploy_basic_tests_package(project_name, project_path)

                Pyscaffold.inject_basic_project_contents(project_name, project_path)

                Pyscaffold.inject_gitignore(project_path)

                Pyscaffold.deploy_virtual_environment(project_path, python_version)

                if len(project_names) == 1:
                    utils.activate_virtual_env(project_path)
            
            except Exception as e:
                if isinstance(e, RuntimeError) and f'Python {python_version} is not installed or not found in PATH.' in str(e):
                    raise
                print(f"Error starting project '{project_name}': {e}")
    
        return True
    
    @staticmethod
    def resume(project_name, destination, **kwargs):
        project_path = Path(destination) / project_name

        if not utils.project_exists(project_name, destination):
            raise FileNotFoundError(f"Project '{project_name}' does not exist at {destination}")

        if not utils.project_ready(project_path):
            raise ValueError(f"Directory '{project_name}' is not a valid project")

        return utils.activate_virtual_env(project_path)
    
    