#! /usr/bin/env python3
"""Blind breadth-first search over a grounded task, compilable with Shed Skin.

This is a self-contained reimplementation of pyperplan's blind breadth-first
search (see ``pyperplan/search/breadth_first_search.py``). It operates on a task
that was grounded by pyperplan and serialized with ``dump_task.py``, so it does
not depend on any pyperplan module. States are represented as ``frozenset``\\s of
integer fact ids, mirroring pyperplan's ``frozenset``-of-facts representation.

The exact same source file runs both under CPython and, once compiled with Shed
Skin, as a native executable. ``benchmark.py`` uses this to compare the two:

    shedskin build -x --jobs 4 bfs_search    # native executable
    ./build/bfs_search task.txt              # native run
    python3 bfs_search.py task.txt           # interpreted run

Both print a machine-readable ``RESULT`` line with the search time, the plan
length and the number of expanded nodes.

Note for Shed Skin: tuples with more than two differently-typed elements are not
supported, so ``Task`` and ``Result`` bundle the heterogeneous values instead.
"""

import sys
import time
from collections import deque


class Operator:
    """A grounded STRIPS operator: preconditions and add/delete effects."""

    def __init__(self, name, preconditions, add_effects, del_effects):
        self.name = name
        self.preconditions = preconditions
        self.add_effects = add_effects
        self.del_effects = del_effects

    def applicable(self, state):
        return self.preconditions <= state

    def apply(self, state):
        # Shed Skin's frozenset arithmetic yields a (mutable, unhashable) set, so
        # we wrap the result to keep states hashable for the closed list.
        return frozenset((state - self.del_effects) | self.add_effects)


class Task:
    """A grounded STRIPS task with integer-encoded facts."""

    def __init__(self, operators, initial_state, goals):
        self.operators = operators
        self.initial_state = initial_state
        self.goals = goals

    def goal_reached(self, state):
        return self.goals <= state


class SearchNode:
    """A node in the search space, linked to its parent for plan extraction."""

    def __init__(self, state, parent, action, g):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = g

    def extract_solution(self):
        """Return the operator indices applied from the root to this node."""
        solution = []
        node = self
        while node.parent is not None:
            solution.append(node.action)
            node = node.parent
        solution.reverse()
        return solution


class Result:
    """The outcome of a search: whether a plan was found, its length and stats."""

    def __init__(self, found, plan_length, expanded):
        self.found = found
        self.plan_length = plan_length
        self.expanded = expanded


def read_ids(line):
    """Parse a whitespace-separated line of integers into a frozenset."""
    result = []
    for token in line.split():
        result.append(int(token))
    return frozenset(result)


def load_task(path):
    """Load a task dumped by ``dump_task.py``."""
    f = open(path)
    lines = f.readlines()
    f.close()

    header = lines[0].split()
    num_operators = int(header[1])
    initial_state = read_ids(lines[1])
    goals = read_ids(lines[2])

    operators = []
    pos = 3
    for _ in range(num_operators):
        name = lines[pos].strip()
        pre = read_ids(lines[pos + 1])
        add = read_ids(lines[pos + 2])
        dele = read_ids(lines[pos + 3])
        operators.append(Operator(name, pre, add, dele))
        pos += 4
    return Task(operators, initial_state, goals)


def breadth_first_search(task):
    """Run blind BFS, returning a ``Result``."""
    expanded = 0
    queue = deque()
    queue.append(SearchNode(task.initial_state, None, -1, 0))
    closed = set()
    closed.add(task.initial_state)
    while queue:
        expanded += 1
        node = queue.popleft()
        if task.goal_reached(node.state):
            return Result(True, len(node.extract_solution()), expanded)
        index = 0
        for op in task.operators:
            if op.applicable(node.state):
                successor = op.apply(node.state)
                if successor not in closed:
                    queue.append(SearchNode(successor, node, index, node.g + 1))
                    closed.add(successor)
            index += 1
    return Result(False, -1, expanded)


def main():
    args = sys.argv
    if len(args) < 2:
        print("usage: bfs_search TASKFILE")
        return
    task = load_task(args[1])

    start = time.time()
    result = breadth_first_search(task)
    elapsed = time.time() - start

    if result.found:
        print("Plan length: %d" % result.plan_length)
        print(
            "RESULT time=%f plan=%d expanded=%d"
            % (elapsed, result.plan_length, result.expanded)
        )
    else:
        print("No solution")
        print("RESULT time=%f plan=-1 expanded=%d" % (elapsed, result.expanded))


if __name__ == "__main__":
    main()
