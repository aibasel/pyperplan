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

"""Implements the breadth-first search algorithm."""

import logging
from collections import deque

from . import searchspace


def breadth_first_search(planning_task):
    """Search for a plan on the given task using breadth-first search.

    Duplicate states are detected and skipped. Returns the solution as a list of
    operators, or None if the task is unsolvable.
    """
    iteration = 0  # Number of expanded nodes (only used for logging).
    # FIFO queue storing the nodes that are next to explore.
    queue = deque()
    queue.append(searchspace.make_root_node(planning_task.initial_state))
    # Set of explored states, used for duplicate detection.
    closed = {planning_task.initial_state}
    while queue:
        iteration += 1
        logging.debug(
            f"breadth_first_search: Iteration {iteration}, #unexplored={len(queue)}"
        )
        node = queue.popleft()
        if planning_task.goal_reached(node.state):
            logging.info("Goal reached. Start extraction of solution.")
            logging.info(f"{iteration} Nodes expanded")
            return node.extract_solution()
        for operator, successor_state in planning_task.get_successor_states(node.state):
            if successor_state not in closed:
                queue.append(
                    searchspace.make_child_node(node, operator, successor_state)
                )
                closed.add(successor_state)
    logging.info("No operators left. Task unsolvable.")
    logging.info(f"{iteration} Nodes expanded")
    return None
