**Pyperplan** is a lightweight STRIPS planner written in Python.

Please note that Pyperplan deliberately prefers clean code over fast
code. It is designed to be used as a teaching or prototyping tool. If
you use it for paper experiments, please state clearly that Pyperplan
does not offer state-of-the-art performance.

It was developed during the planning practical course at
Albert-Ludwigs-Universität Freiburg during the winter term 2010/2011 and
is published under the terms of the GNU General Public License 3
(GPLv3).

Pyperplan supports the following PDDL fragment: STRIPS without action
costs.

# Requirements

Pyperplan requires [Python](https://python.org) >= 3.6.

# Installation

From the Python package index (PyPI):

    pip install pyperplan

From inside a repository clone:

    pip install --editable .

This makes the `pyperplan` command available globally or in your [virtual
environment](https://docs.python.org/3/tutorial/venv.html) (recommended).

# Usage

The `pyperplan` executable accepts two arguments: a PDDL domain file and a
PDDL problem file. Example:

    pyperplan benchmarks/tpp/domain.pddl benchmarks/tpp/task01.pddl

The domain file can be omitted, in which case the planner will attempt
to guess its name based on the problem file. If a plan is found, it is
stored alongside the problem file with a .soln extension.

By default, the planner performs a blind breadth-first search, which
does not scale very well. Heuristic search algorithms are available. For
example, to use greedy-best-first search with the FF heuristic, run

    pyperplan -H hff -s gbf DOMAIN PROBLEM

For a list of available search algorithms and heuristics, run

    pyperplan --help

For more information on using the planner and how to extend it to do
more fancy stuff, see the [documentation](doc/documentation.md).

# FAQs

## PDDL types

Pyperplan follows the semantics that all types other than the universal
supertype object (which is mentioned as such in the PDDL 1.2 paper) need
to be explicitly introduced.

# Contact

Pyperplan is hosted on GitHub: <https://github.com/aibasel/pyperplan>

The original authors of Pyperplan are, in alphabetical order:

  - Yusra Alkhazraji
  - Matthias Frorath
  - Markus Grützner
  - Thomas Liebetraut
  - Manuela Ortlieb
  - Jendrik Seipp
  - Tobias Springenberg
  - Philip Stahl
  - Jan Wülfing

The instructors of the course in which Pyperplan was created were Malte
Helmert and Robert Mattmüller.

If you want to get in touch with us, please contact Robert Mattmüller or
Jendrik Seipp. Their email addresses can easily be found on the web.

# Citing Pyperplan

Please cite Pyperplan using

    @Misc{alkhazraji-et-al-zenodo2020,
      author =       "Yusra Alkhazraji and Matthias Frorath and Markus Gr{\"u}tzner
                      and Malte Helmert and Thomas Liebetraut and Robert Mattm{\"u}ller
                      and Manuela Ortlieb and Jendrik Seipp and Tobias Springenberg and
                      Philip Stahl and Jan W{\"u}lfing",
      title =        "Pyperplan",
      publisher =    "Zenodo",
      year =         "2020",
      doi =          "10.5281/zenodo.3700819",
      url =          "https://doi.org/10.5281/zenodo.3700819",
      howpublished = "\url{https://doi.org/10.5281/zenodo.3700819}"
    }
