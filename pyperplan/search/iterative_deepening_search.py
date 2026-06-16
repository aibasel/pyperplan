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

"""Implements the iterative deepening search algorithm."""

import logging

from ..task import Operator, State, Task


def iterative_deepening_search(task: Task, *args: int) -> list[Operator] | None:
    """Search for a plan on ``task`` using iterative deepening search.

    Uses loop detection. Creates an ``IterativeDeepeningSearchAlgorithm`` and
    delegates to its ``search`` method. Returns the solution as a list of
    operators, or None if the task is unsolvable.
    """
    searcher = IterativeDeepeningSearchAlgorithm()
    return searcher.search(task, *args)


class IterativeDeepeningSearchAlgorithm:
    """Searches for a plan on a task using iterative deepening search."""

    def __init__(self) -> None:
        # Maximal reachable depth, needed to terminate if the goal is
        # unreachable.
        self.maxreacheddepth = 0
        # Number of explored nodes during the search.
        self.explorednodes = 0

    def search(self, task: Task, maxdepth: int = 1000000) -> list[Operator] | None:
        """Search for a plan on ``task`` using iterative deepening search.

        Uses loop detection. ``maxdepth`` limits the search to a fixed depth; if
        there is no plan within that depth, None is returned. Returns the
        solution as a list of operators, or None if the task is unsolvable.
        """
        # Special case: the initial state already satisfies the goal.
        if task.goal_reached(task.initial_state):
            self.print_search_results(0, 0)
            return []
        # States on the current path, used for loop detection.
        path: set[State] = set()
        depth = 1
        # Run until we reach the goal or fail to explore up to the given depth.
        while depth < maxdepth:
            self.maxreacheddepth = 0
            self.explorednodes = 0
            plan = self.deepening_search_step(task, task.initial_state, depth, 0, path)
            if plan is not None:
                plan.reverse()  # The plan is built up in reverse order.
                self.print_search_results(depth, len(plan))
                return plan
            if self.maxreacheddepth < depth:
                # We could not explore up to the target depth, so no goal state
                # is reachable.
                logging.debug("Dead end. Task unsolvable.")
                self.print_search_results(depth, -1)
                return None
            depth += 1
        logging.debug("Emergency brake. Loop? Increase maxdepth.")
        self.print_search_results(depth, -1)
        return None

    def print_search_results(self, depth: int, planlength: int) -> None:
        logging.info(
            f"iterative_deepening_search: depth={depth} planlength={planlength} "
        )
        logging.info(f"{self.explorednodes} Nodes expanded")

    def deepening_search_step(
        self,
        task: Task,
        state: State,
        depth: int,
        step: int,
        path: set[State],
    ) -> list[Operator] | None:
        """Take one step on a path to the goal during depth-limited search.

        Each call advances by one step and supports easy backtracking.

        state: The current state on the path.
        depth: The maximal search depth in the current iteration.
        step: The current search step.
        path: The set of states on the current path, used for loop detection.

        Returns the (reversed) solution as a list of operators, or None if no
        plan was found below ``state`` within the depth limit.
        """
        if step < depth:
            nextstep = step + 1
            path.add(state)
            for operator, successor_state in task.get_successor_states(state):
                self.explorednodes += 1
                # Skip successors already on the path; they would form a loop.
                if successor_state not in path:
                    if task.goal_reached(successor_state):
                        logging.info("Goal reached. Start extraction of solution.")
                        self.maxreacheddepth = nextstep
                        return [operator]
                    else:
                        plan = self.deepening_search_step(
                            task, successor_state, depth, nextstep, path
                        )
                        if plan is not None:
                            plan.append(operator)
                            return plan
            # Found no plan below this state, so backtrack.
            path.remove(state)
            if self.maxreacheddepth < step:
                self.maxreacheddepth = step
        else:
            # Reached the depth limit without finding a plan on this path.
            self.maxreacheddepth = step
        return None
