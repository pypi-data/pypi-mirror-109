#!/usr/bin/env python

from setuptools import setup
from setuptools import find_packages


project_name = "ordered_argparse"
package_dir = "src"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
        name=project_name,
        version="1.0.4",
        description="Modified version of argparse which remembers the order of CLI arguments",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="Sven Siegmund",
        author_email="sven.siegmund@gmail.com",
        url="https://github.com/Nagidal/ordered_argparse",
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
