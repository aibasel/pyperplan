#! /usr/bin/env python

from glob import glob
import os.path

from setuptools import find_packages, setup


VERSION = "1.2"


with open("README.md") as f:
    long_description = f.read()


setup(
    name="pyperplan",
    version=VERSION,
    description="A lightweight STRIPS planner written in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="classical planning STRIPS",
    author="Jendrik Seipp",
    author_email="jendrik.seipp@unibas.ch",
    url="https://github.com/aibasel/pyperplan",
    license="GPL3+",
    packages=find_packages("src", exclude=["tests"]),
    package_dir={"": "src"},
    py_modules=[
        os.path.splitext(os.path.basename(path))[0] for path in glob("src/*.py")
    ],
    include_package_data=True,
    entry_points={"console_scripts": ["pyperplan = pyperplan:main"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
    ],
    install_requires=["wheel"],
    python_requires=">=3.5",
)
