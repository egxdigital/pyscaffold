"""
Pyscaffold

This module defines the Pyscaffold class, which provides methods for creating and 
managing Python projects, including setting up project folders, deploying project 
and test packages, configuring Git ignore files, and managing virtual environments.
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
    """
    A class for scaffolding and managing Python projects with predefined 
    structure and configurations.
    """

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
        """
        Create a new project folder at the specified destination.

        Args:
            project_name (str): The name of the project to create.
            destination (str): The path where the project folder should be created.

        Returns:
            Path: The path to the newly created project folder.

        Raises:
            FileExistsError: If a folder with the same name already exists.
            OSError: If the destination path is not a valid directory.
        """
        project_path = Path(destination) / project_name
        
        if project_path.exists():
            raise FileExistsError(f"The project folder '{project_path}' already exists.")
        
        if not os.path.isdir(destination):
            raise OSError(f"The destination path '{destination}' is invalid.")

        project_path.mkdir(parents=True, exist_ok=True)
        return project_path
     
    @staticmethod
    def inject_basic_package_contents(project_name: str, package_name: str, package_path: Path) -> None:
        """
        Inject basic package files into the project package directory.

        Args:
            project_name (str): The name of the project.
            package_name (str): The name of the package to be created.
            package_path (Path): The path to the package directory.

        Raises:
            Exception: If there is an error writing any of the files.
        """
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
        """
        Deploy a basic package structure within the project directory.

        Args:
            project_name (str): The name of the project.
            project_location (Path): The location where the package should be deployed.

        Returns:
            Tuple[str, Path]: The name and path of the deployed package.

        Raises:
            Exception: If there is an error during package deployment.
        """
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
    def inject_basic_test_package_contents(project_name: str, test_package_name: str, test_package_path: Path) -> None:
        """
        Inject basic test package files into the project test directory.

        Args:
            project_name (str): The name of the project.
            test_package_name (str): The name of the test package.
            test_package_path (Path): The path to the test package directory.

        Raises:
            Exception: If there is an error writing any of the files.
        """
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
        """
        Deploy a basic test package structure within the project directory.

        Args:
            project_name (str): The name of the project.
            project_location (Path): The location where the test package should be deployed.

        Returns:
            Tuple[str, Path]: The name and path of the deployed test package.

        Raises:
            Exception: If there is an error during test package deployment.
        """
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
        """
        Inject basic project files into the project directory.

        Args:
            project_name (str): The name of the project.
            project_path (Path): The path to the project directory.

        Raises:
            Exception: If there is an error writing any of the files.
        """
        for filename, content in Pyscaffold.basic_project_content_map.items():
            try:
                with open(project_path / filename, "w", encoding="utf-8") as f:
                    f.write(content.format(ProjectName=project_name, packagename=project_name))
            except Exception as e:
                print(f"Error writing file {filename}: {e}")
                raise
    
    @staticmethod
    def inject_gitignore(project_path: Path) -> None:
        """
        Inject a .gitignore file into the project directory.

        Args:
            project_path (Path): The path to the project directory.

        Raises:
            PermissionError: If there is a permission issue while accessing or writing files.
            FileNotFoundError: If the .gitignore template file is not found.
            RuntimeError: For unexpected errors during the .gitignore injection process.
        """
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
        """
        Create a virtual environment in the specified project directory.

        Args:
            project_path (Path): The path to the project directory.
            python_version (str): The version of Python to use for the virtual environment (default: '3.11').

        Returns:
            bool: True if the virtual environment was created successfully.

        Raises:
            RuntimeError: If the specified Python version is not installed or not found in PATH.
            subprocess.CalledProcessError: If there is an error creating the virtual environment.
        """
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
    def start(project_names, python_version, **kwargs) -> bool:
        """
        Initialize and set up projects with the specified names.

        Args:
            project_names (list of str): The names of the projects to be created.
            python_version (str): The version of Python to use for the virtual environment.
            **kwargs: Additional keyword arguments. The 'destination' key specifies where to create the projects.

        Returns:
            bool: True if all projects were initialized and set up successfully.

        Raises:
            RuntimeError: If the specified Python version is not installed or not found in PATH.
            Exception: For other errors that occur during project setup.
        """
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
    def resume(project_name, destination, **kwargs) -> bool:
        """
        Resume a project by activating its virtual environment.

        Args:
            project_name (str): The name of the project to resume.
            destination (str): The path where the project is located.
            **kwargs: Additional keyword arguments (not used).

        Returns:
            bool: True if the virtual environment was successfully activated.

        Raises:
            FileNotFoundError: If the project does not exist at the specified destination.
            ValueError: If the project directory is not valid.
        """
        project_path = Path(destination) / project_name

        if not utils.project_exists(project_name, destination):
            raise FileNotFoundError(f"Project '{project_name}' does not exist at {destination}")

        if not utils.project_ready(project_path):
            raise ValueError(f"Directory '{project_name}' is not a valid project")

        return utils.activate_virtual_env(project_path)
    
    