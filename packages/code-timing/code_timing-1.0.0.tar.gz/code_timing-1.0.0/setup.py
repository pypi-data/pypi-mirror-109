from os import name
from setuptools import setup, find_packages, version

VERSION = '1.0.0'
DESCRIPTION = 'Python Package to measure multiple executions to calculate the average execution-time.'
setup(
    # The name must match the folder name
    name = "code_timing",
    version = VERSION,
    author = '3301-byte',
    description = DESCRIPTION,
    packages = find_packages(),
    install_requires = [
        'numpy',
        'dataclasses'],
    keywords = ['python', 'code_timing'],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ] 
)