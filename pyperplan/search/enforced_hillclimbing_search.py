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
Implements the enforced hill climbing search algorithm.
"""

from collections import deque
import logging

from . import searchspace


def enforced_hillclimbing_search(planning_task, heuristic, use_preferred_ops=False):
    """
    Searches for a plan on the given task using enforced hill climbing and
    duplicate detection.

    @param planning_task: The planning task to solve.
    @return: The solution as a list of operators or None if no solution was
    found. Note that enforced hill climbing is an incomplete algorith, so it
    may fail to find a solution even though the task is solvable.
    """
    # counts the number of loops (only for printing)
    iteration = 0
    # fifo-queue storing the nodes which are next to explore
    queue = deque()
    initial_node = searchspace.make_root_node(planning_task.initial_state)
    queue.append(initial_node)
    best_heuristic_value = heuristic(initial_node)
    logging.info("Initial h value: %f" % best_heuristic_value)
    # set storing the explored nodes, used for duplicate detection
    closed = set()
    visited = set()
    while queue:
        iteration += 1
        # get the next node to explore
        node = queue.popleft()
        # remember the successor state
        closed.add(node.state)
        visited.add(node.state)
        # exploring the node or if it is a goal node extracting the plan
        if planning_task.goal_reached(node.state):
            logging.info("Goal reached. Start extraction of solution.")
            logging.info("%d Nodes expanded" % len(visited))
            return node.extract_solution()

        # for the preferred operator version --> recompute heuristic and
        # relaxed plan
        if use_preferred_ops:
            (rh, rplan) = heuristic.calc_h_with_plan(node)
            logging.debug("relaxed plan %s " % rplan)

        for operator, successor_state in planning_task.get_successor_states(node.state):

            # for the preferred operator version ignore all non preferred
            # operators
            if use_preferred_ops:
                if rplan and not operator.name in rplan:
                    # ignore this operator if we use the relaxed plan criterion
                    logging.debug(
                        "removing operator %s << not a preferred "
                        "operator" % operator.name
                    )
                    continue
                else:
                    logging.debug("keeping operator %s" % operator.name)

            # duplicate detection
            if successor_state not in closed:
                successor_node = searchspace.make_child_node(
                    node, operator, successor_state
                )
                heuristic_value = heuristic(successor_node)
                if heuristic_value == float("inf"):
                    continue
                elif heuristic_value < best_heuristic_value:
                    # Just take the first successor node that has a lower
                    # heuristic value than the current best_heuristic_value
                    # and ignore the other successor nodes.
                    logging.debug(
                        "Found new best h: %f after %d expansions"
                        % (heuristic_value, iteration)
                    )
                    queue.clear()
                    closed.clear()
                    best_heuristic_value = heuristic_value
                    queue.append(successor_node)
                    break
                else:
                    queue.append(successor_node)
    logging.info("Enforced hill climbing failed")
    logging.info("%d Nodes expanded" % len(visited))
    return None
