from setuptools import setup, find_packages

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
