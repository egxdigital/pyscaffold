"""
Pyscaffold Helpers

This module provides utility functions for the Pyscaffold application to assist 
with naming conventions and other related tasks.

"""

def apply_project_naming_convention(name: str) -> str:
    """
    Convert a project name from snake_case to PascalCase.

    Given a project name in snake_case, such as "my_new_project", this function
    converts it to PascalCase, resulting in "MyNewProject". This is commonly used
    for naming classes or projects in a format where each word starts with an uppercase letter.

    Args:
        name (str): The project name in snake_case.

    Returns:
        str: The project name converted to PascalCase.
    """
    name = name.replace('_', ' ')
    name = name.title().replace(' ', '')
    return name

def apply_package_naming_convention(project_name: str) -> str:
    """
    Convert a project name from PascalCase to snake_case for package naming.

    This function takes a project name in PascalCase, such as "MyNewProject", 
    and converts it to snake_case, resulting in "my_new_project". This is often used
    for naming Python packages in a format that is compatible with Python's module
    naming conventions.

    Args:
        project_name (str): The project name in PascalCase.

    Returns:
        str: The project name converted to snake_case.
    """
    # Convert PascalCase to snake_case
    return ''.join(['_' + c.lower() if c.isupper() else c for c in project_name]).lstrip('_')
