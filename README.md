# pyscaffold

> A CLI tool for scaffolding Python projects

Tested only on Linux so far.

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

## Why pyscaffold?

The question that may come to mind is, why not just use an IDE?

Now pyscaffold was born purely of a personal preference to use the familiar environment of the command-line interpreter to spin up Python projects.

It helps that modern text editors come with amazing features that sometimes surpass outstanding IDE's and what's more, unlike good IDE's, many great modern text editors are absolutely free.

**When paired with an extensible text-editor, this tool proves indispensable.**


## Acknowledgements

Thank you [Stephan Tual](https://github.com/stephantual) for [your solution to to the argparse description field limitation](https://stackoverflow.com/a/15721870)