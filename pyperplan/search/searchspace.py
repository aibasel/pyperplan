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

"""The search node and associated helper functions."""


class SearchNode:
    """A node in the search space of a planning algorithm.

    Nodes form a recursive data structure: each node links to its parent node
    and stores the state, the action that led to it, and the path length ``g``
    measured as the number of applied operators.
    """

    def __init__(self, state, parent, action, g):
        """
        state: The state to store in the search space.
        parent: The parent node in the search space.
        action: The action that produced the state.
        g: The path length of the node, i.e. the number of applied operators.
        """
        self.state = state
        self.parent = parent
        self.action = action
        self.g = g

    def extract_solution(self):
        """Return the actions applied from the initial node to this node."""
        solution = []
        node = self
        while node.parent is not None:
            solution.append(node.action)
            node = node.parent
        solution.reverse()
        return solution


def make_root_node(initial_state):
    """Construct the root search node.

    The root node has no parent and no action, and its g-value is zero.
    """
    return SearchNode(initial_state, None, None, 0)


def make_child_node(parent_node, action, state):
    """Construct a child of ``parent_node`` reached via ``action``.

    The child stores ``state`` and its g-value is the parent's g-value plus one.
    """
    return SearchNode(state, parent_node, action, parent_node.g + 1)
