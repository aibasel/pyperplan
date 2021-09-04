# Introduction

This is the documentation for Pyperplan, a STRIPS planner built in the
winter term 2010/2011 by the students of the AI planning practical course
at the University of Freiburg. It is written in Python3 and is quite
competitive when it comes to feature completeness. This document should
help you to understand the planner's usage as well as the internal
structure and where to extend it, if you want to.

# Usage

The planner's executable is called `pyperplan`. It takes at least one
argument, the PDDL problem file.

If you only pass a problem file, Pyperplan will try to guess the domain
file from the problem file. If the problem file contains a number,
Pyperplan will use a filename like `domainNUMBER.pddl` as a domain file
candidate. If this file does not exist (or the problem name does not
contain a number), it just uses `domain.pddl`. If this fails, an error
will be raised.

You can pass a specific domain file by using `pyperplan domainfile
problemfile` to call the planner. **Note:** The domain comes before the
problem, even though the domain is optional.

There are several command line arguments you can specify to define how
Pyperplan should solve the problem. By default, it uses breadth first
search in the search space and the FF heuristic to estimate the goal
distance (which is ignored by the breadth-first search). By using the
parameters `-H` or `-s`, you can select a different heuristic or search
algorithm, respectively. If you leave one of them out, the default will be
used. You can get a list of available search algorithms by executing
`pyperplan --help`.

## Solution

After a plan is found, it is saved in a file named just the same as the
problem file but with the `.soln` suffix appended.

A `soln` file contains actions in a LISP-like notation. The first element
in each list is the action as taken from the domain specification, and all
the following elements are the arguments to the action. This format is a
PDDL compatible plan representation that can be fed to PDDL validators to
check if the plans are actually valid.

# Internals

## PDDL representation

The PDDL parsing and representation is in the package `pddl`.
Currently both the parser and the data structures only support positive STRIPS,
meaning that only positive preconditions are supported. For every element in a
PDDL STRIPS problem or domain, there is a class in the `pddl.pddl` module.
These classes are populated by the PDDL parser accordingly. The main parsing
is done in `pddl.parser` where the `Parser` class is defined which provides
methods for parsing a domain and a problem file. It parses the file by
using a generic LISP parser that fills an abstract syntax tree. This tree is
then traversed and nodes with PDDL-specific keywords are used to generate
instances of the according class of from the `pddl.pddl` module. When
more features are added to the STRIPS implementation, e.g., supporting the
complete set of STRIPS features, it should be sufficient to modify the existing
visitors.

## Task and grounding

After the domain and problem have been parsed to an instance of `Domain`
and `Problem` respectively, they pass the grounding step in which a
concrete planning task is generated. The grounding is implemented in the
module `grounding` and takes a PDDL problem and returns a `Task` instance
that represents the search task. This is a container class for a set of
concrete Operator instances. The actions are no longer abstract
definitions with types, but for any applicable object in the domain, there
is an `Operator` that can be applied to the current state and that has
specific results.

The `Task` class provides a function that helps to build a search space:
`get_successor_states` returns a list of all the possible states that can
be reached using only valid operators. This creates a tree-like structure
that, at some nodes, contain the goal state. The actual planning then
consists in finding the shortest path to the goal state.

## Search

The search package contains a collection of search algorithms, like
breadth-first search or A*. The `searchspace` module contains a data
structure `SearchNode` to create the search space, which stores
information from the search and allows to efficiently extract the plan.

### Using the SearchNode class

The `SearchNode` class in `searchspace.py` is easy to use; just create a
root node for the initial state of the planning task by using the function
`searchspace.make_root_node(...)`. When applying an operator to a state
you get a new state. This applied operator and the new state are stored in
a new node, using the function `searchspace.make_child_node(...)` with the
current search node as parent. This builds a tree-like structure.

In this way you can store the information from the search and, if you are
in a goal state, you can extract the plan by calling `extract_solution()`
on the goal node.

### SAT planner

You can also find a SAT planner in the search package. It uses the minisat
SAT solver to find a plan for a given problem. Pyperplan encodes the
problem in a Boolean formula in conjunctive normal form before it invokes
minisat. To use the SAT planner you have to make the `minisat` executable
available on the system `PATH` (e.g., /usr/local/bin/). Afterwards you can
run the planner with the `--search sat` option. Please note that the
executable is sometimes called "minisat2" in distribution packages (e.g.,
in some versions of Ubuntu). If that is the case you will have to rename
the binary to "minisat".

### Implementing new search algorithms

There is no base class to implement a new search algorithm, because each
algorithm needs other arguments. So most of the algorithms are just single
functions implemented in their own file. The naming convention is to name
the module according to the algorithm and provide a function with a
_search suffix that does the search. There should be no other side effects
or things that need to be set up before doing the search. For convenience,
the `*_search()` function should be properly imported in the package's
`__init__.py`.

## Heuristics

Most of the more advanced search algorithms are *informed* searches, which
means they need information about how far a node is from the goal. Such
information is taken from a heuristic which, given a node, estimates how
far the node is away from the goal state.

The heuristics in Pyperplan are implemented as modules in the `heuristics`
package.

### Implementing new heuristics

For all the heuristics, there is a base class in the
`heuristics.heuristic_base` package called `Heuristic`. Unlike search
algorithms, which can be implemented as a single function, heuristics need
to know something about the task and are hence a class. The class
constructor takes the planning task as an argument and can apply
preprocessing of states if necessary. In most of the cases you want to at
least store a reference to the goal state.

Each descendant of heuristic must implement the `__call__` magic method
which has to take a node and return the estimated distance from the goal.
For nodes that are known to be unsolvable (i.e., there is no valid plan that
reaches the goal from this node), a heuristic value of `float('inf')` should
be returned.

Pyperplan automatically finds all heuristic classes that reside in modules
in the `heuristics` folder if the class name ends with "Heuristic".

## Logging

Pyperplan uses the `logging` package from the Python standard library
(http://docs.python.org/library/logging.html). Just add `import logging`
in your file and use the function `logging.info(...)` to add your own
logging output.

# Tests

Pyperplan includes a comprehensive test suite. To run the tests, install
and run `tox` (preferably in a virtual environment).

    pip install tox
    tox

# Plan validation

If the plan validation tool VAL is found on the system `PATH` under the
name `validate`, all found plans will be validated. To use this feature,
run the following steps (on Ubuntu)

    sudo apt install bison flex g++ git make
    git clone https://github.com/KCL-Planning/VAL.git
    cd VAL
    # Newer VAL versions need time stamps, so we use an old version
    # (https://github.com/KCL-Planning/VAL/issues/46).
    git checkout a556539
    make clean  # Remove old binaries.
    sed -i 's/-Werror //g' Makefile  # Ignore warnings.
    make
    cp validate ~/bin/  # Add binary to a directory on your ``PATH``.

