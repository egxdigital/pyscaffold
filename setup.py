"""Pyscaffold Setup

This module contains the setuptools.setup() definition for the Pyscaffold program.

Usage
    deactivate \\
    pip freeze > requirements.txt\\
    sudo python3.9 -m setup develop
"""
from pathlib import Path, PurePath
from setuptools import setup, find_packages

requirements = []

requirements_txt = PurePath(
    Path(__file__).resolve().parent, 'requirements.txt')

if Path(requirements_txt).is_file():
    with open(Path(requirements_txt)) as fd:
        lines = fd.readlines()[:-2]
        requirements += lines

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Pyscaffold",
    version="0.0.0",
    author="Emille Giddings",
    author_email="emilledigital@gmail.com",
    description="Scaffold Python projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    install_requires=requirements,
    packages=find_packages(include=['pyscaffold']),
    package_data={'': ['data/gitignore-python', 'data/LICENSE']},
    entry_points={
        'console_scripts': ['pyscaffold=pyscaffold.__main__:main']
    },
    tests_require=['unittest'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
