#! /usr/bin/env python

from setuptools import find_packages, setup


VERSION = "2.1"


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
    author_email="jendrik.seipp@liu.se",
    url="https://github.com/aibasel/pyperplan",
    license="GPL3+",
    packages=find_packages(exclude=["pyperplan.tests"]),
    entry_points={"console_scripts": ["pyperplan = pyperplan.__main__:main"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
    ],
    install_requires=["wheel"],
    python_requires=">=3.6",
)
