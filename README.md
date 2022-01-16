# pyscaffold

> A CLI tool for scaffolding Python projects

Tested only on Linux so far.

## Why pyscaffold?

Why not just use an IDE?

It helps that modern text editors come with amazing features that sometimes surpass outstanding IDE's and what's more, unlike good IDE's, many great modern text editors are absolutely free.

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

1. First set an environment variable called 'python' to your preferred Python projects location or edit the line in the code to reflect your own shell variable for your projects folder.

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
        config.py
        helpers.py
        project.py
    tests/
        data/
        test_helpers.py
        test_project.py
    .gitignore
    LICENSE
    README.md
    setup.py
```
<br>

---

<br>

## To do

- Add function check_env_python_version()
    - invoke in replace_env()
- Migrate fron unittest to pytest
    - Add test for the pyscaffold class

<br>

---

<br>

## Acknowledgements

Thanks to:
- [Depado](https://github.com/Depado) and [Peter Mortensen](https://github.com/PeterMortensen) for [solution to "activating virtual environment from a python script"](https://stackoverflow.com/a/18037819)
- [Stephan Tual](https://github.com/stephantual) for [solution to to the argparse description field limitation](https://stackoverflow.com/a/15721870)