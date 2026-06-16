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

"""Implements the A* (a-star) and weighted A* search algorithms."""

import heapq
import logging
from collections.abc import Callable

from ..heuristics.heuristic_base import Heuristic
from ..task import Operator, State, Task
from . import searchspace
from .searchspace import SearchNode

# A priority-queue entry: (f, h, tiebreaker, node), ordered tuple-wise.
OpenEntry = tuple[float, float, int, SearchNode]
# A factory that builds an open-list entry from a node, its h-value and a
# tiebreaker counter.
MakeOpenEntry = Callable[[SearchNode, float, int], OpenEntry]


def ordered_node_astar(node: SearchNode, h: float, node_tiebreaker: int) -> OpenEntry:
    """Return a priority-queue entry ordering ``node`` by f = g + h (A*).

    The tuple ``(f, h, node_tiebreaker, node)`` orders nodes by f-value, then by
    h-value, then by ``node_tiebreaker`` (an increasing counter that prefers
    earlier-inserted nodes when the ordering is otherwise equal).
    """
    return (node.g + h, h, node_tiebreaker, node)


def ordered_node_weighted_astar(weight: float) -> MakeOpenEntry:
    """Return an entry factory for weighted A*, ordering nodes by g + weight * h.

    Calling ``ordered_node_weighted_astar(42)`` returns a function that builds
    the actual priority-queue entries. A call like
    ``ordered_node_weighted_astar(42)(node, h, tiebreaker)`` thus creates an
    entry with weighted A* ordering and a weight of 42.
    """
    return lambda node, h, node_tiebreaker: (
        node.g + weight * h,
        h,
        node_tiebreaker,
        node,
    )


def ordered_node_greedy_best_first(
    node: SearchNode, h: float, node_tiebreaker: int
) -> OpenEntry:
    """Return a priority-queue entry ordering ``node`` by h alone (greedy BFS)."""
    return (h, h, node_tiebreaker, node)


def greedy_best_first_search(
    task: Task, heuristic: Heuristic, use_relaxed_plan: bool = False
) -> list[Operator] | None:
    """Search for a plan in ``task`` using greedy best-first search.

    ``heuristic`` is a callable that estimates the number of steps from a search
    node to the goal.
    """
    return astar_search(
        task, heuristic, ordered_node_greedy_best_first, use_relaxed_plan
    )


def weighted_astar_search(
    task: Task,
    heuristic: Heuristic,
    weight: float = 5,
    use_relaxed_plan: bool = False,
) -> list[Operator] | None:
    """Search for a plan in ``task`` using weighted A* search.

    ``heuristic`` is a callable that estimates the number of steps to the goal,
    and ``weight`` is applied to that estimate for each node.
    """
    return astar_search(
        task, heuristic, ordered_node_weighted_astar(weight), use_relaxed_plan
    )


def astar_search(
    task: Task,
    heuristic: Heuristic,
    make_open_entry: MakeOpenEntry = ordered_node_astar,
    use_relaxed_plan: bool = False,
) -> list[Operator] | None:
    """Search for a plan in ``task`` using A* search.

    ``heuristic`` is a callable that estimates the number of steps from a search
    node to the goal. ``make_open_entry`` controls the search order; it builds
    the entries pushed onto the open list. Possible values are
    ``ordered_node_astar``, ``ordered_node_weighted_astar`` and
    ``ordered_node_greedy_best_first``.
    """
    open_list: list[OpenEntry] = []
    state_cost: dict[State, int] = {task.initial_state: 0}
    node_tiebreaker = 0

    root = searchspace.make_root_node(task.initial_state)
    init_h = heuristic(root)
    heapq.heappush(open_list, make_open_entry(root, init_h, node_tiebreaker))
    logging.info(f"Initial h value: {init_h:f}")

    besth: float = float("inf")
    counter = 0
    expansions = 0

    while open_list:
        (f, h, _tie, pop_node) = heapq.heappop(open_list)
        if h < besth:
            besth = h
            logging.debug(f"Found new best h: {besth} after {counter} expansions")

        pop_state = pop_node.state
        # Only expand the node if its associated cost (g value) is the lowest
        # cost known for this state. Otherwise we already found a cheaper
        # path after creating this node and hence can disregard it.
        if state_cost[pop_state] == pop_node.g:
            expansions += 1

            if task.goal_reached(pop_state):
                logging.info("Goal reached. Start extraction of solution.")
                logging.info(f"{expansions} Nodes expanded")
                return pop_node.extract_solution()
            rplan: set[str] | None = None
            if use_relaxed_plan:
                (rh, rplan) = heuristic.calc_h_with_plan(
                    searchspace.make_root_node(pop_state)
                )
                logging.debug(f"relaxed plan {rplan} ")

            for op, succ_state in task.get_successor_states(pop_state):
                if use_relaxed_plan:
                    if rplan and op.name not in rplan:
                        # Ignore this operator if it is not in the relaxed plan.
                        logging.debug(
                            f"removing operator {op.name} << not a preferred operator"
                        )
                        continue
                    else:
                        logging.debug(f"keeping operator {op.name}")

                # Only consider this successor if it reaches succ_state more
                # cheaply than any path seen so far. The heuristic is expensive,
                # so we avoid computing it for successors we would not enqueue.
                succ_g = pop_node.g + 1
                if succ_state in state_cost and succ_g >= state_cost[succ_state]:
                    continue
                succ_node = searchspace.make_child_node(pop_node, op, succ_state)
                h = heuristic(succ_node)
                if h == float("inf"):
                    # Don't bother with states that can't reach the goal anyway.
                    continue
                # We either never saw succ_state before, or we found a cheaper
                # path to succ_state than previously.
                node_tiebreaker += 1
                heapq.heappush(
                    open_list, make_open_entry(succ_node, h, node_tiebreaker)
                )
                state_cost[succ_state] = succ_g

        counter += 1
    logging.info("No operators left. Task unsolvable.")
    logging.info(f"{expansions} Nodes expanded")
    return None
