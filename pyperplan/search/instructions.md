# The search module

## Summary

The search package contains a collection of search algorithms, such as
breadth-first search or A*. The `searchspace` module contains a `SearchNode`
data structure for building the search space, which stores information from
the search and allows the plan to be extracted quickly.

## Using the SearchNode class

(See `searchspace.py`.)

The `SearchNode` class is easy to use: create a root node for the initial
state of the planning task with `searchspace.make_root_node(...)`. Applying
an operator to a state yields a new state; store the applied operator and the
new state in a new node with `searchspace.make_child_node(...)`, passing the
current search node as the parent. This builds a tree-like structure.

This way you can store the information from the search, and once you reach a
goal state you can read off the plan by calling `extract_solution()` on the
goal node.

## Implementing search algorithms

There is no base class for search algorithms, because each algorithm needs
different arguments. Most algorithms are therefore just single functions, each
implemented in its own file. The naming convention is to name the module after
the algorithm and to provide a function with a `_search` suffix that performs
the search. There should be no other side effects or setup required before
running the search. For convenience, the `*_search()` function should be
imported in the package's `__init__.py`.

For logging, use the standard library's `logging` module: add
`import logging` to your file and call `logging.info(...)`. See the `logging`
documentation for the full set of logging functions.
