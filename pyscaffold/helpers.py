import sys
from pprint import pprint
from pathlib import Path


def is_camel_case(st: str) -> bool:
    """Takes a string and returns True if the string is camel case or similar"""
    return st != st.lower() and st != st.upper() and "_" not in st 


def contains_hyphen(st: str) -> bool:
    """Takes a string and returns True if there are hyphens"""
    return "_" in st


def conventional_naming(st: str, is_package=True) -> str:
    """Takes a proposed name and a choice of whether project or package and returns 
    a string with the appropriate naming convention"""

    res = ''.join(st.split("_")).lower()
        
    if is_package:
        return res
    else:
        return res.capitalize()

    
def get_file_name() -> str:
    """Returns the name of the enclosing file as a string"""
    return Path(sys._getframe(1).f_code.co_filename).name


def get_func_name() -> str:
    """Returns the name of the calling function as a string"""
    return sys._getframe(1).f_code.co_name


def return_file_content_as_string(p: Path) -> str:
    """Takes a file and returns the content of that file as a string"""
    try:
        return Path(p).read_text()
    except Exception as e:
        print(f"Exception: {e}")


def preview_file_content(p: Path) -> None:
    """Takes a file and displays the content of that file"""
    try:
        print(Path(p).read_text())
    except Exception as e:
        print(f"Exception: {e}")