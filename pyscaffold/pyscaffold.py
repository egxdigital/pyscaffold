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
    def start(project_names, destination, **kwargs):
        #print('IN start() -> destination: ', kwargs.get('destination'))
        for p in project_names:
            print(f"Starting project: {p} at {destination}")
            # create project folder
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
    
    