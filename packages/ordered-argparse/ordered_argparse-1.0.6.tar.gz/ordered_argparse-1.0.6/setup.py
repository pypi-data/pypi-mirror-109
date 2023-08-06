#!/usr/bin/env python

from setuptools import setup
from setuptools import find_packages
import pathlib
import re


this_dir = pathlib.Path(__file__).parent.absolute()
project_name = "ordered_argparse"
package_dir = "src"
path_to_init_file = this_dir / package_dir / project_name / "__init__.py"


with open("README.md", mode="r", encoding="utf-8") as fh:
    long_description = fh.read()


with open(this_dir / "requirements.txt", mode="r", encoding="utf-8") as reqs:
    requirements = [line.strip() for line in reqs]


def get_property(property: str, path_to_init_file: pathlib.Path) -> str:
    """
    Reads a property from the project's __init__.py
    e.g. get_property("__version__") --> "1.2.3"
    """
    regex = re.compile(r"{}\s*=\s*[\"'](?P<value>[^\"']*)[\"']".format(property))
    try:
        with open(path_to_init_file) as initfh:
            try:
                result = regex.search(initfh.read()).group("value")
            except AttributeError:
                result = None
    except FileNotFoundError:
        result = None
    return result


setup(
        name=project_name,
        version=get_property("__version__", path_to_init_file),
        description="Modified version of argparse which remembers the order of CLI arguments",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author=get_property("__author__", path_to_init_file),
        author_email=get_property("__author_email__", path_to_init_file),
        url=get_property("__url__", path_to_init_file),
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: End Users/Desktop",
            "Intended Audience :: Developers",
            "Intended Audience :: System Administrators",
            "Environment :: Console",
            "Topic :: Software Development",
            "Topic :: Utilities",
            "License :: OSI Approved :: MIT License",
            "Natural Language :: English",
            "Programming Language :: Python :: 3.9",
            "Operating System :: OS Independent",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX :: Linux",
            "Operating System :: MacOS :: MacOS X",
            ],
        keywords="cli argument parsing",
        package_dir={"": package_dir},
        packages=find_packages(where=package_dir),
        package_data={
            project_name: [],
            },
        python_requires=">=3.9",
        install_requires=[],
        entry_points={
            "console_scripts": [],
            },
        platforms=["any"],
    )
