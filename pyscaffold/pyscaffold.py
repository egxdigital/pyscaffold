import os
from pathlib import Path

from pyscaffold.utils import (
    project_exists, 
    project_ready, 
    activate_virtual_env
)

class Pyscaffold():
    @staticmethod
    def list_projects(*args, **kwargs):
        print(kwargs)
        return
    
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
    def start(project_names, **kwargs):
        destination = kwargs.get('destination', None)
        
        for project_name in project_names:
            project_path = Pyscaffold.create_project_folder(project_name, destination)

            if project_path:
                print(f"Starting project: {project_name} at {project_path}")
            else:
                print(f"Failed to create project folder for '{project_name}'.")
            # deploy package
            #    deploy package contents
            # deploy tests package
            #    deploy tests package contents
            # deploy setup.py
            # deploy pytest.ini
            # deploy .env
            # deploy .gitignore
            # deploy LICENSE
            # deploy README.md
            # deploy virtual environment
        return
    
    @staticmethod
    def resume(project_name, destination, **kwargs):
        project_path = Path(destination) / project_name

        if not project_exists(project_name, destination):
            raise FileNotFoundError(f"Project '{project_name}' does not exist at {destination}")

        if not project_ready(project_path):
            raise ValueError(f"Directory '{project_name}' is not a valid project")

        return activate_virtual_env(project_path)
    
    