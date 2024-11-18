"""
Pyscaffold Setup

This module contains the setuptools.setup() definition for the Pyscaffold program.

Usage
    pipx install --editable .
    pipx inject pyscaffold -r requirements.txt
"""
from pathlib import Path
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

def parse_requirements(file_path):
    prod_deps = []
    dev_deps = []
    current_section = "prod"

    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith("#"):
                if line.lower() == "# production dependencies":
                    current_section = "prod"
                elif line.lower() == "# development dependencies":
                    current_section = "dev"
                continue
            # Add dependency to the correct section
            if current_section == "prod":
                prod_deps.append(line)
            elif current_section == "dev":
                dev_deps.append(line)
    
    return prod_deps, dev_deps

# Load dependencies from requirements.txt
requirements_path = Path(__file__).parent / "requirements.txt"
production_deps, development_deps = parse_requirements("requirements.txt")

def get_version():
    version_file = Path(__file__).parent / 'pyscaffold' / '_version.py'
    with open(version_file) as f:
        version_globals = {}
        exec(f.read(), version_globals)
    return version_globals['__version__']

version = get_version()

setup(
    name="Pyscaffold",
    version=version,
    author="Emille Giddings",
    author_email="emilledigital@gmail.com",
    description="Scaffold Python projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(include=['pyscaffold', 'pyscaffold.*']),
    include_package_data=True,
    package_data={
        '': ['config.yaml', 'data/gitignore-python', 'data/LICENSE']
    },
    entry_points={
        'console_scripts': ['pyscaffold=pyscaffold.__main__:main']
    },
    tests_require=['pytest'],
    install_requires=production_deps,
    extras_require={
        "dev": development_deps
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Natural Language :: English",
    ],
    python_requires='>=3.11',
)
