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
Implements the iterative deepening search algorithm.
"""

from collections import deque
import logging


def iterative_deepening_search(task, *args):
    """
    Searches for a plan on a task using iterative deepening search. Uses loop
    detection.
    The function creates an object of the IterativeDeepeningSearchAlgorithm
    class and calls the corresponding search function.

    @param task: The planning task to solve.
    @param args: Additional arguments for the search.
    @return: The solution as a list of operators or None if the task is
    unsolvable.
    """
    searcher = IterativeDeepeningSearchAlgorithm()
    return searcher.search(task, *args)


class IterativeDeepeningSearchAlgorithm:
    """
    Searches for a plan on a task using iterative deepening search.
    """

    def __init__(self):
        # stores the maximal reachable depth, needed to terminate if the goal
        # is not reachable
        self.maxreacheddepth = 0
        # number of explored nodes during search
        self.explorednodes = 0

    def search(self, task, maxdepth=1000000):
        """
        Searches for a plan on a task using iterative deepening search. Uses
        loop detection.

        @param task: The planning task to solve.
        @param maxdepth: Limit the search to a fixed depth. If there is no plan
                         in this depth then returns None.
        @return: The solution as a list of operators or None if the task is
                 unsolvable.
        """
        # testing the first case, initial is a goal
        if task.goal_reached(task.initial_state):
            self.print_search_results(0, 0)
            return []
        # loop detection
        path = set()
        # actual search depth
        depth = 1
        # run until at goal or fail to explore to the given depth
        while depth < maxdepth:
            self.maxreacheddepth = 0
            self.explorednodes = 0
            plan = self.deepening_search_step(task, task.initial_state, depth, 0, path)
            if plan is not None:
                # plan comes in the wrong order
                plan.reverse()
                self.print_search_results(depth, len(plan))
                return plan
            # can not explore until depth?
            if self.maxreacheddepth < depth:
                # can not get any goal state
                logging.debug("Dead end. Task unsolvable.")
                self.print_search_results(depth, -1)
                return None
            # try to find a plan ones deeper
            depth += 1
        logging.debug("Emergency brake. Loop? Increase maxdepth.")
        self.print_search_results(depth, -1)
        return None

    def print_search_results(self, depth, planlength):
        logging.info(
            "iterative_deepening_search: depth=%d planlength=%d " % (depth, planlength)
        )
        logging.info("%d Nodes expanded" % self.explorednodes)

    def deepening_search_step(self, task, state, depth, step, path):
        """
        Helper function for the search, each call is a step on the a path to
        the goal. Allows easy and fast backtracking.

        @param task: The planning task to solve.
        @param state: The current state on the path.
        @param depth: The maximal search depth in the actual iteration.
        @param step: The current search step.
        @param path: The current set of states on the path, needed for the loop
                     detection.
        @return: The solution as a list of operators or None if the task is
        unsolvable.
        """
        if step < depth:
            nextstep = step + 1
            # remember the actual state
            path.add(state)
            for operator, successor_state in task.get_successor_states(state):
                self.explorednodes += 1
                # already on path? Yes then it is an loop, so ignore the
                # successor and return to the caller without a plan
                if successor_state not in path:
                    if task.goal_reached(successor_state):
                        logging.info("Goal reached. Start extraction of " "solution.")
                        self.maxreacheddepth = nextstep
                        return [operator]
                    else:
                        plan = self.deepening_search_step(
                            task, successor_state, depth, nextstep, path
                        )
                        if plan is not None:
                            # extracting the plan and terminating
                            plan.append(operator)
                            return plan
            # found no plan on the explored path and children
            # remove the actual state
            path.remove(state)
            if self.maxreacheddepth < step:
                self.maxreacheddepth = step
        else:
            # can not finish search on this path, because
            self.maxreacheddepth = step
            # found no plan on this sub tree of possible paths
        return None
