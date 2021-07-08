# pyscaffold

> A CLI tool for scaffolding projects

## Installation

Change current directory to download location and run

```bash
pip install .
```

Or install from VCS using pip

```bash
python3 -m pip install git+https://github.com/egxdigital/pyscaffold.git#egg=Pyscaffold
```

## Usage

1. First set an environment variable called 'python' to your preferred Python projects location.

Or 

1. Change the current directory to the preferred location and proceed to the next step.

2. To scaffold an installable Python application, run

```bash
pyscaffold start <project_name>
```

Creates a directory with the following contents including boilerplate code.

Python project structure
```
Project
    bin/
    data/
    docs/
    env/
    project/
        __init__.py
        __main__.py
        helpers.py
        project.py
    tests/
        test_helpers.py
        test_project.py
    .gitignore
    LICENSE
    README.md
    setup.py
```
## Acknowledgements

Thank you [Stephan Tual](https://github.com/stephantual) for [your solution to to the argparse description field limitation](https://stackoverflow.com/a/15721870)