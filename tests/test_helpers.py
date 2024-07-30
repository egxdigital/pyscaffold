"""
Pyscaffold Test Helpers

This module contains tests for the Pyscaffold helper functions. These functions are responsible for applying naming conventions
to project and package names. The tests ensure that these helper functions correctly format names according to the specified 
conventions.

Functions:
- test_apply_project_naming_convention_single_word: Tests the application of project naming conventions to various single-word
  and multi-word project names.
- test_apply_package_naming_convention: Tests the application of package naming conventions to various project names.
"""

import pytest
from pyscaffold.helpers import (
    apply_project_naming_convention,
    apply_package_naming_convention
    )

def test_apply_project_naming_convention_single_word():
    """
    Test the application of project naming conventions.

    Validates that:
        - A single-word project name is capitalized (e.g., "project" -> "Project").
        - Multi-word project names are converted to CamelCase (e.g., "my new project" -> "MyNewProject").
        - Underscore-separated names are converted to CamelCase (e.g., "my_new_project" -> "MyNewProject").
        - Mixed-case names are normalized to CamelCase (e.g., "aNoThEr PrOjEcT" -> "AnotherProject").
        - Alphanumeric names are preserved with capitalization (e.g., "project123" -> "Project123").
    """
    assert apply_project_naming_convention("project") == "Project"
    assert apply_project_naming_convention("my new project") == "MyNewProject"
    assert apply_project_naming_convention("my_new_project") == "MyNewProject"
    assert apply_project_naming_convention("aNoThEr PrOjEcT") == "AnotherProject"
    assert apply_project_naming_convention("project123") == "Project123"

def test_apply_package_naming_convention():
    """
    Test the application of package naming conventions.

    Validates that:
        - CamelCase project names are converted to snake_case (e.g., "MyProject" -> "my_project").
        - Multi-word CamelCase names are converted to snake_case (e.g., "AnotherExampleProject" -> "another_example_project").
        - Short names are converted to lowercase with underscores (e.g., "YetAnother" -> "yet_another").
        - Alphanumeric names are preserved with lowercase and underscores (e.g., "Project123" -> "project123").
        - Multi-word CamelCase names are converted to snake_case (e.g., "ProjectOneTwoThree" -> "project_one_two_three").
    """
    assert apply_package_naming_convention("MyProject") == "my_project"
    assert apply_package_naming_convention("AnotherExampleProject") == "another_example_project"
    assert apply_package_naming_convention("YetAnother") == "yet_another"
    assert apply_package_naming_convention("Project123") == "project123"
    assert apply_package_naming_convention("ProjectOneTwoThree") == "project_one_two_three"

if __name__ == "__main__":
    pytest.main()