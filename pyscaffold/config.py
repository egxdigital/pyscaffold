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
    EXPLICIT_STRING_DEFS = {
        'PROJECTS': {
            'pathname':'/mnt/c/Users/engineer/source/python',
            'description': 'Absolute path to global projects directory on local machine',
            'is_relative': False
        },
        'TEST_PROJECTS': {
            'pathname': 'tests/dummyprojects',
            'description': 'Relative path to test projects directory for use during testing',
            'is_relative': True
        },
        'ENV': {
            'pathname': './.env',
            'description': 'Relative path to project root environment variables',
            'absolute': True

        },
        'TEST_ENV': {
            'pathname': 'tests/.env',
            'description': 'Relative to test environment variables',
            'is_relative': True
        }
    }
    @staticmethod
    def display():
        """
        Display all configuration settings.
        """
        from pprint import pprint
        pprint(Config.EXPLICIT_STRING_DEFS)

    @staticmethod
    def get_config_value_by_variable_name(variable_name: str) -> Path:
        """
        Retrieve the pathname associated with the given variable name.
        
        Args:
            variable_name (str): The configuration variable name.
        
        Returns:
            Path: The resolved pathname.
        
        Raises:
            KeyError: If the variable name is not found.
            ValueError: If the resolved path does not exist.
        """
        config = Config.EXPLICIT_STRING_DEFS.get(variable_name)
        if config is None:
            raise KeyError(f"Not a valid variable name: {variable_name}")

        path = Path(config['pathname'])
        if config['is_relative']:
            path = Path(__file__).resolve().parent.parent / path

        if not path.exists():
            raise ValueError(f'Pathname setting for {variable_name} is not valid: {path}')
        
        return path
    
    @staticmethod
    def compare_config_value_with_environment_variable(env_var_name: str, value: str):
        """
        Compare the provided environment variable value with the configuration setting.
        
        Args:
            env_var_name (str): The environment variable name.
            value (str): The value to compare.
        
        Returns:
            bool: True if the value matches the configuration setting, False otherwise.
        
        Raises:
            KeyError: If the environment variable name is not found.
        """
        config = Config.EXPLICIT_STRING_DEFS.get(env_var_name)
        if config is None:
            raise KeyError(f"Not a valid variable name: {env_var_name}")

        return value == config['pathname']