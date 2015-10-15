This is **pyperplan**, a lightweight STRIPS planner written in Python.

It was developed during the planning practical course at
Albert-Ludwigs-Universität Freiburg during the winter term 2010/2011 and is
published under the terms of the GNU General Public License 3 (GPLv3).

Pyperplan supports the following PDDL fragment: STRIPS without action costs.
This file only gives the basic information to get you up and running.
The full documentation can be found in the doc directory. You can either read
the text file documentation.txt directly or run "make" in the doc directory to
convert it to a PDF document.


Requirements
============

pyperplan is written in Python 3, so you need a recent version of Python 3
installed to run it. If Python 3 is not installed on your system, you can
download it from http://python.org. Alternatively, most current Linux
distributions include Python 3. For example,

    sudo apt-get install python3

will install Python 3 on an Ubuntu system.

Versions of Python before Python 3.2 lack the argparse package, which pyperplan
uses for command line argument parsing. A copy of the argparse package is
included with the planner and will be used automatically if no preinstalled
version can be found.


Usage
=====

The planner is invoked through the file src/pyperplan.py and accepts two
arguments: a PDDL domain file and a PDDL problem file. Example:

    ./src/pyperplan.py benchmarks/tpp/domain.pddl benchmarks/tpp/task01.pddl

The domain file can be omitted, in which case the planner will attempt to guess
its name based on the problem file. If a plan is found, it is stored alongside
the problem file with a .soln extension.

By default, the planner performs a blind breadth-first search, which does not
scale very well. Heuristic search algorithms are available. For example, to use
greedy-best-first search with the FF heuristic, run

    ./src/pyperplan.py -H hff -s gbf DOMAIN PROBLEM

For a list of available search algorithms and heuristics, run

    ./src/pyperplan.py --help

For more information on using the planner and how to extend it to do more fancy
stuff, see doc/documentation.txt.


Contact
=======

pyperplan is hosted on bitbucket: https://bitbucket.org/malte/pyperplan

The original authors of pyperplan are, in alphabetical order:

* Yusra Alkhazraji
* Matthias Frorath
* Markus Grützner
* Thomas Liebetraut
* Manuela Ortlieb
* Jendrik Seipp
* Tobias Springenberg
* Philip Stahl
* Jan Wülfing

The instructors of the course in which pyperplan was created were
Malte Helmert and Robert Mattmüller.

If you want to get in touch with us, please contact Robert Mattmüller or
Jendrik Seipp. Their email addresses can easily be found on the web.