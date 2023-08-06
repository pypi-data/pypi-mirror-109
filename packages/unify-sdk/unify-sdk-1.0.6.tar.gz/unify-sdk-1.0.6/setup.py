import os
import pathlib
import re
from setuptools import setup
from setuptools import find_packages
import subprocess

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text().strip()

version = os.popen('git describe --dirty').read()

setup(
    name='unify-sdk',
    version=str(version),
    description="Unify Python SDK",
    long_description=README,
    long_description_content_type='text/markdown',
    python_requires='>=3',
    packages=find_packages(),
    include_package_data=True,
    hiddenimports=[
        'keyring',
        'setuptools',
        'tabulate',
        'requests',
    ],
    install_requires=[
        'keyring',
        'setuptools',
        'tabulate',
        'requests',
    ],
    url='https://github.com/ElementAnalytics/unify-python-sdk',
    author='Element Analytics',
    author_email='platform@ean.io',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
