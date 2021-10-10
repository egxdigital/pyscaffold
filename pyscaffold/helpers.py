import sys
from pprint import pprint
from shutil import which, rmtree
from pathlib import Path, PurePath
from pyscaffold.config import *



def message(*args):
    result = ""
    for arg in args:
        if arg == args[-1]:
            result += f"{arg}"
            return result
        result += f"{arg}: "
    return result
        

def error(cmd: str, msg: str, *details):
    message = f"{colors.BOLD}{cmd}{colors.ENDC}: {colors.FAIL}{msg}{colors.ENDC}"
    for detail in details:
        if detail == details[-1]:
            message += f": {colors.WARNING}{detail}{colors.ENDC}"
            return message
        if isinstance(detail, float):
            detail = "{:.1f}".format(detail)
        message += f": {colors.WARNING}{detail}{colors.ENDC}"
    return message


def delete_directory(pathname):
    try:
        rmtree(Path(pathname))
    except Exception as e:
        print(e)
    else:
        print(f"path removed: {pathname}")


def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""
    return which(name) is not None


def project_root_exists(name: str, projects_dir: Path) -> bool:
    proper = conventional_naming(name, is_package=False)
    pathname = PurePath(projects_dir, proper)
    is_dir =  Path(pathname).is_dir()
    is_proj = 'setup.py' in [_.name for _ in Path(pathname).iterdir()]    
    return is_dir and is_proj


def is_camel_case(st: str) -> bool:
    """Takes a string and returns True if the string is camel case or similar"""
    return st != st.lower() and st != st.upper() and "_" not in st 


def contains_hyphen(st: str) -> bool:
    """Takes a string and returns True if there are hyphens"""
    return "_" in st


def conventional_naming(st: str, is_package=True) -> str:
    """If st is not a package name then conventional_naming
    treats it as a project name.

    Parameters
    ----------
    st : str
        Underscores are allowed. No spaces are allowed.
    is_package : bool, optional
        Considered project if not package, by default True

    Returns
    -------
    str
        String with underscores removed.
    """
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
