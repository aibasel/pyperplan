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

'''
Implements the breadth first search algorithm.
'''

from collections import deque
import logging

from . import searchspace


def breadth_first_search(planning_task):
    '''
    Searches for a plan on the given task using breadth first search and
    duplicate detection.

    @param planning_task: The planning task to solve.
    @return: The solution as a list of operators or None if the task is
    unsolvable.
    '''
    # counts the number of loops (only for printing)
    iteration = 0
    # fifo-queue storing the nodes which are next to explore
    queue = deque()
    queue.append(searchspace.make_root_node(planning_task.initial_state))
    # set storing the explored nodes, used for duplicate detection
    closed = {planning_task.initial_state}
    while queue:
        iteration += 1
        logging.debug("breadth_first_search: Iteration %d, #unexplored=%d"
                      % (iteration, len(queue)))
        # get the next node to explore
        node = queue.popleft()
        # exploring the node or if it is a goal node extracting the plan
        if planning_task.goal_reached(node.state):
            logging.info("Goal reached. Start extraction of solution.")
            logging.info("%d Nodes expanded" % iteration)
            return node.extract_solution()
        for operator, successor_state in planning_task.get_successor_states(
                                                                   node.state):
            # duplicate detection
            if successor_state not in closed:
                queue.append(searchspace.make_child_node(node, operator,
                                                         successor_state))
                 # remember the successor state
                closed.add(successor_state)
    logging.info("No operators left. Task unsolvable.")
    logging.info("%d Nodes expanded" % iteration)
    return None
