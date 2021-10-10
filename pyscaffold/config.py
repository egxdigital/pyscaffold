import os
from pathlib import Path, PurePath

ROOT      = Path(__file__).resolve().parent.parent
PKG       = Path(__file__).resolve().parent
DATA      = Path(PurePath(ROOT, 'data'))
TESTS     = Path(PurePath(ROOT, 'tests'))
TEST_DATA = Path(PurePath(TESTS, 'data'))

PYTHON_VERSION  = 3.9
PROJECTS_FOLDER = os.getenv('python', default=Path.cwd())

class ERROR():
    bad_command         = 'invalid command!'
    bad_directory       = 'invalid destination directory!'
    bad_project_list    = 'invalid project list format!'
    bad_python_version  = 'python version does not exist!'
    no_projects         = 'no projects specified!'
    no_env_found        = 'no virtual environment found!'
    more_than_one       = 'too many projects!'
    project_not_found   = 'project not found!'
    project_exists      = 'project already exists!'

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
