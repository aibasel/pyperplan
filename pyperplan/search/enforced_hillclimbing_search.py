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

"""Implements the enforced hill-climbing search algorithm."""

import logging
from collections import deque

from . import searchspace


def enforced_hillclimbing_search(planning_task, heuristic, use_preferred_ops=False):
    """Search for a plan on the given task using enforced hill climbing.

    Duplicate states are detected and skipped. Returns the solution as a list of
    operators, or None if no solution was found. Note that enforced hill
    climbing is incomplete, so it may fail to find a solution even though the
    task is solvable.
    """
    iteration = 0  # Number of expanded nodes (only used for logging).
    # FIFO queue storing the nodes that are next to explore.
    queue = deque()
    initial_node = searchspace.make_root_node(planning_task.initial_state)
    queue.append(initial_node)
    best_heuristic_value = heuristic(initial_node)
    logging.info(f"Initial h value: {best_heuristic_value:f}")
    # Set of explored states, used for duplicate detection.
    closed = set()
    visited = set()
    while queue:
        iteration += 1
        node = queue.popleft()
        closed.add(node.state)
        visited.add(node.state)
        if planning_task.goal_reached(node.state):
            logging.info("Goal reached. Start extraction of solution.")
            logging.info(f"{len(visited)} Nodes expanded")
            return node.extract_solution()

        # For the preferred operator version, recompute the relaxed plan.
        if use_preferred_ops:
            (rh, rplan) = heuristic.calc_h_with_plan(node)
            logging.debug(f"relaxed plan {rplan} ")

        for operator, successor_state in planning_task.get_successor_states(node.state):
            # For the preferred operator version, ignore non-preferred operators.
            if use_preferred_ops:
                if rplan and operator.name not in rplan:
                    logging.debug(
                        f"removing operator {operator.name} << not a preferred operator"
                    )
                    continue
                else:
                    logging.debug(f"keeping operator {operator.name}")

            if successor_state not in closed:  # Duplicate detection.
                successor_node = searchspace.make_child_node(
                    node, operator, successor_state
                )
                heuristic_value = heuristic(successor_node)
                if heuristic_value == float("inf"):
                    continue
                elif heuristic_value < best_heuristic_value:
                    # Take the first successor node with a lower heuristic value
                    # than the current best and ignore the other successors.
                    logging.debug(
                        f"Found new best h: {heuristic_value:f} "
                        f"after {iteration} expansions"
                    )
                    queue.clear()
                    closed.clear()
                    best_heuristic_value = heuristic_value
                    queue.append(successor_node)
                    break
                else:
                    queue.append(successor_node)
    logging.info("Enforced hill climbing failed")
    logging.info(f"{len(visited)} Nodes expanded")
    return None
