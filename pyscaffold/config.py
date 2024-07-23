import yaml
from pathlib import Path

class colors():
    HEADER     = '\033[95m'
    OKBLUE     = '\033[94m'
    OKCYAN     = '\033[96m'
    OKGREEN    = '\033[92m'
    WARNING    = '\033[93m'
    FAIL       = '\033[91m'
    ENDC       = '\033[0m'
    BOLD       = '\033[1m'
    UNDERLINE  = '\033[4m'

class Config():
    def __init__(self, config_path=None):
        self.settings = {}
        if config_path is None:
            config_path = Path(__file__).resolve().parent.parent / 'config.yaml'
        self.load_from_file(config_path)

    def load_from_file(self, config_path):
        """
        Load configuration settings from a YAML file.
        
        Args:
            config_path (str): Path to the YAML configuration file.
        """
        with open(config_path, 'r') as file:
            self.settings = yaml.safe_load(file)

    def get(self, key, default=None):
        """
        Retrieve a configuration value by its key.
        
        Args:
            key (str): The key to look up in the configuration.
            default: The default value to return if the key is not found.
        
        Returns:
            The value associated with the key, or the default value.
        """
        keys = key.split('.')
        value = self.settings
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value

    def add_setting(self, name, **kwargs):
        """
        Add a new setting to the configuration.
        
        Args:
            name (str): The name of the new setting.
            kwargs: The key-value pairs for the new setting.
        
        Returns:
            self
        """
        self.settings[name] = kwargs
        return self

    def update_setting(self, name, **kwargs):
        """
        Update an existing setting in the configuration.
        
        Args:
            name (str): The name of the setting to update.
            kwargs: The key-value pairs to update the setting with.
        
        Returns:
            self
        """
        if name in self.settings:
            self.settings[name].update(kwargs)
        else:
            self.settings[name] = kwargs
        return self

    def display(self):
        """
        Display all configuration settings.
        """
        from pprint import pprint
        pprint(self.settings)
    
    def get_projects_directory_path(self) -> Path:
        """
        Retrieve the absolute path to the global projects directory.

        Returns:
            Path: The resolved projects directory pathname.
        
        Raises:
            ValueError: If the resolved path does not exist.
        """
        path = Path(self.get("locations.PROJECTS"))

        if not path.exists():
            raise ValueError('Projects directory has not been set.')
        
        return path

    def get_tests_directory_path(self, abs=False) -> Path:
        """
        Retrieve the path to the test projects directory.

        Args:
            abs (bool): If True, returns the absolute path.

        Returns:
            Path: The resolved test projects directory pathname.
        
        Raises:
            ValueError: If the resolved path does not exist.
        """
        path = Path(self.get("locations.TEST_PROJECTS"))
        if abs:
            path = Path(__file__).resolve().parent.parent / path
        
        if not path.exists():
            raise ValueError('Tests directory does not exist.')
        
        return path