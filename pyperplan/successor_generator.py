#
# This file is part of pyperplan.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#

"""A decision-tree successor generator in the style of Fast Downward.

The naive way to find the operators applicable in a state is to test every
operator's preconditions against the state, which costs time proportional to the
total number of operators. Fast Downward instead organizes the operators in a
decision tree that branches on individual facts, so that only the operators
whose preconditions can still be satisfied are visited.

Each inner node tests one fact. Its ``match_child`` holds the operators that
require this fact (and is only entered when the fact is true in the state),
while its ``no_match_child`` holds the operators that do not mention the fact
(and is always entered). Operators whose preconditions are all satisfied along
the path from the root sit in a node's ``immediate`` list.
"""


class NaiveSuccessorGenerator:
    """Find applicable operators by testing every operator in turn.

    This is the straightforward baseline: applicability is checked for each
    operator, so a query costs time proportional to the number of operators.
    """

    def __init__(self, operators):
        self._operators = list(operators)

    def get_applicable_operators(self, state):
        """Return the operators applicable in ``state``, in their original order."""
        return [op for op in self._operators if op.applicable(state)]


class _Node:
    """A node in the successor-generator decision tree.

    A leaf has ``fact is None`` and no children; it only contributes its
    ``immediate`` operators. An inner node branches on ``fact``.
    """

    __slots__ = ("fact", "immediate", "match_child", "no_match_child")

    def __init__(self):
        self.fact = None
        self.immediate = []
        self.match_child = None
        self.no_match_child = None


def _choose_fact(items):
    """Return the fact occurring in the most of the given preconditions.

    Branching on the most frequent fact keeps the tree shallow: it splits off as
    many operators as possible into the ``match_child`` at every step.
    """
    counts = {}
    for _, _, preconditions in items:
        for fact in preconditions:
            counts[fact] = counts.get(fact, 0) + 1
    return max(counts, key=counts.get)


class SuccessorGenerator:
    """Index a set of operators for fast applicability queries."""

    def __init__(self, operators):
        # Pair every operator with its original index so that we can return
        # applicable operators in their original order, matching the behavior of
        # a plain linear scan over ``operators``.
        items = [(index, op, op.preconditions) for index, op in enumerate(operators)]
        self._root = self._build(items)

    @staticmethod
    def _build(items):
        """Build the decision tree for ``items`` iteratively.

        ``items`` is a list of ``(index, operator, remaining_preconditions)``
        triples, where ``remaining_preconditions`` are the preconditions not yet
        tested on the path to the current node. An explicit work stack is used
        instead of recursion so that deep trees cannot exhaust the call stack.
        """
        root = _Node()
        stack = [(root, items)]
        while stack:
            node, node_items = stack.pop()
            remaining = []
            for index, op, preconditions in node_items:
                if preconditions:
                    remaining.append((index, op, preconditions))
                else:
                    node.immediate.append((index, op))
            if not remaining:
                continue  # Leaf: all operators here are unconditionally applicable.
            fact = _choose_fact(remaining)
            node.fact = fact
            match_items = []
            no_match_items = []
            for index, op, preconditions in remaining:
                if fact in preconditions:
                    match_items.append((index, op, preconditions - {fact}))
                else:
                    no_match_items.append((index, op, preconditions))
            node.match_child = _Node()
            node.no_match_child = _Node()
            stack.append((node.match_child, match_items))
            stack.append((node.no_match_child, no_match_items))
        return root

    def get_applicable_operators(self, state):
        """Return the operators applicable in ``state``, in their original order."""
        found = []
        stack = [self._root]
        while stack:
            node = stack.pop()
            found.extend(node.immediate)
            if node.fact is not None:
                stack.append(node.no_match_child)
                if node.fact in state:
                    stack.append(node.match_child)
        found.sort(key=lambda pair: pair[0])
        return [op for _, op in found]


SUCCESSOR_GENERATORS = {
    "naive": NaiveSuccessorGenerator,
    "tree": SuccessorGenerator,
}


def create_successor_generator(name, operators):
    """Return a successor generator of the given kind for ``operators``."""
    return SUCCESSOR_GENERATORS[name](operators)
