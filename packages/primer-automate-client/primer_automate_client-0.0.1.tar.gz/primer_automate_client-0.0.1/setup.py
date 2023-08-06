from typing import List

from pkg_resources import parse_requirements
from setuptools import find_packages, setup

from primer_automate_client.__version__ import __version__


def _parse(filename: str) -> List[str]:
    return [str(r) for r in parse_requirements(open(filename))]


def _parse(filename):
    """Parse a requirements file, including `-r requirements.txt` references"""
    reqs = None
    with open(filename) as reqs_file:
        reqs = reqs_file.read().splitlines()
    return reqs


reqs = _parse("requirements.txt")

setup(
    name="primer_automate_client",
    version=__version__,
    author="Connor Jennings",
    author_email="connor.jennings@primer.ai",
    description="A client for interacting with Automate",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=("tests")),
    install_requires=reqs,
    include_package_data=True,
)
