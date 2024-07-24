"""
Pyscaffold Helpers

This module contains helper function definitions for the Pyscaffold application.

"""

def apply_project_naming_convention(name: str) -> str:
    """
    Apply Pascal naming convention to a given project name. Converts strings like
    "my_new_project" to "MyNewProject".
    """
    name = name.replace('_', ' ')
    name = name.title().replace(' ', '')
    return name

def apply_package_naming_convention(project_name: str) -> str:
    """Apply package naming convention: PascalCase to snakecase."""
    # Convert PascalCase to snake_case
    return ''.join(['_' + c.lower() if c.isupper() else c for c in project_name]).lstrip('_')
