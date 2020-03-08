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

"""
Building the search node and associated methods
"""


class SearchNode:
    """
    The SearchNode class implements recursive data structure to build a
    search space for planning algorithms. Each node links to is parent
    node and contains informations about the state, action to arrive
    the node and the path length in the count of applied operators.
    """

    def __init__(self, state, parent, action, g):
        """
        Construct a search node

        @param state: The state to store in the search space.
        @param parent: The parent node in the search space.
        @param action: The action which produced the state.
        @param g: The path length of the node in the count of applied
                  operators.
        """
        self.state = state
        self.parent = parent
        self.action = action
        self.g = g

    def extract_solution(self):
        """
        Returns the list of actions that were applied from the initial node to
        the goal node.
        """
        solution = []
        while self.parent is not None:
            solution.append(self.action)
            self = self.parent
        solution.reverse()
        return solution


def make_root_node(initial_state):
    """
    Construct an initial search node. The root node of the search space
    does not links to a parent node, does not contains an action and the
    g-value is zero.

    @param initial_state: The initial state of the search space.
    """
    return SearchNode(initial_state, None, None, 0)


def make_child_node(parent_node, action, state):
    """
    Construct a new search node containing the state and the applied action.
    The node is linked to the given parent node.
    The g-value is set to the parents g-value + 1.
    """
    return SearchNode(state, parent_node, action, parent_node.g + 1)
