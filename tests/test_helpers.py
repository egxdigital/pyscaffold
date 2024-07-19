import pytest
from pyscaffold.helpers import (
    apply_project_naming_convention,
    apply_package_naming_convention
    )

def test_apply_project_naming_convention_single_word():
    assert apply_project_naming_convention("project") == "Project"
    assert apply_project_naming_convention("my new project") == "MyNewProject"
    assert apply_project_naming_convention("my_new_project") == "MyNewProject"
    assert apply_project_naming_convention("aNoThEr PrOjEcT") == "AnotherProject"
    assert apply_project_naming_convention("project123") == "Project123"

def test_apply_package_naming_convention():
    assert apply_package_naming_convention("MyProject") == "my_project"
    assert apply_package_naming_convention("AnotherExampleProject") == "another_example_project"
    assert apply_package_naming_convention("YetAnother") == "yet_another"
    assert apply_package_naming_convention("Project123") == "project123"
    assert apply_package_naming_convention("ProjectOneTwoThree") == "project_one_two_three"

if __name__ == "__main__":
    pytest.main()