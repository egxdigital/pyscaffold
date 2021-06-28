import sys
from pprint import pprint
from pathlib import Path

def get_file_name():
    """Returns the name of the enclosing file as a string"""
    return Path(sys._getframe(1).f_code.co_filename).name


def get_func_name():
    """Returns the name of the calling function as a string"""
    return sys._getframe(1).f_code.co_name


def lower_first_letter(st: str) -> str:
    """Takes a string and returns a 
    new string with the first letter lowered"""
    return st[0].lower() + st[1:]


def return_file_content_as_string(path: Path) -> str:
    """Takes a file pathname and returns the content of that file as a string"""
    try:
        with Path(path).open() as f:
            lines = f.readlines()
            return "".join(lines)
    except Exception as e:
        print(f"Exception: {e}")


def preview_file_content(path: Path) -> None:
    """Takes a file pathname and pretty prints the content of that file"""
    try:
        with Path(path).open() as f:
            lines = f.readlines()
            pprint(lines)
    except Exception as e:
        print(f"Exception: {e}")


def capitalize_first_letter(st: str) -> str:
    """Takes a string and returns a new string with the first letter capitalized"""
    return st[0].upper() + st[1:]
