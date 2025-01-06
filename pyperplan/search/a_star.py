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
Implements the A* (a-star) and weighted A* search algorithm.
"""

import heapq
import logging
import time
import os
import psutil

from . import searchspace
from .search_stat import SearchLimit, SearchResult

def ordered_node_astar(node, h, node_tiebreaker):
    """
    Creates an ordered search node (basically, a tuple containing the node
    itself and an ordering) for A* search.

    @param node The node itself.
    @param heuristic A heuristic function to be applied.
    @param node_tiebreaker An increasing value to prefer the value first
                           inserted if the ordering is the same.
    @returns A tuple to be inserted into priority queues.
    """
    f = node.g + h
    return (f, h, node_tiebreaker, node)


def ordered_node_weighted_astar(weight):
    """
    Creates an ordered search node (basically, a tuple containing the node
    itself and an ordering) for weighted A* search (order: g+weight*h).

    @param weight The weight to be used for h
    @param node The node itself
    @param h The heuristic value
    @param node_tiebreaker An increasing value to prefer the value first
                           inserted if the ordering is the same
    @returns A tuple to be inserted into priority queues
    """
    """
    Calling ordered_node_weighted_astar(42) actually returns a function (a
    lambda expression) which is the *actual* generator for ordered nodes.
    Thus, a call like
        ordered_node_weighted_astar(42)(node, heuristic, tiebreaker)
    creates an ordered node with weighted A* ordering and a weight of 42.
    """
    return lambda node, h, node_tiebreaker: (
        node.g + weight * h,
        h,
        node_tiebreaker,
        node,
    )


def ordered_node_greedy_best_first(node, h, node_tiebreaker):
    """
    Creates an ordered search node (basically, a tuple containing the node
    itself and an ordering) for greedy best first search (the value with lowest
    heuristic value is used).

    @param node The node itself.
    @param h The heuristic value.
    @param node_tiebreaker An increasing value to prefer the value first
                           inserted if the ordering is the same.
    @returns A tuple to be inserted into priority queues.
    """
    f = h
    return (f, h, node_tiebreaker, node)


def greedy_best_first_search(*args, **kwargs):
    """
    Searches for a plan in the given task using greedy best first search.

    @param task The task to be solved.
    @param heuristic A heuristic callable which computes the estimated steps
                     from a search node to reach the goal.
    """
    return astar_search(*args, ordered_node_greedy_best_first, early_goal_detection=True, **kwargs)


def weighted_astar_search(*args, weight=5, **kwargs):
    """
    Searches for a plan in the given task using A* search.

    @param task The task to be solved.
    @param heuristic  A heuristic callable which computes the estimated steps.
                      from a search node to reach the goal.
    @param weight A weight to be applied to the heuristics value for each node.
    """
    return astar_search(*args, ordered_node_weighted_astar(weight), **kwargs)


def astar_search(task, heuristic,
                 make_open_entry=ordered_node_astar,
                 use_relaxed_plan=False,
                 limit=SearchLimit(),
                 early_goal_detection=False,
                 **kwargs):
    """
    Searches for a plan in the given task using A* search.

    @param task The task to be solved
    @param heuristic  A heuristic callable which computes the estimated steps
                      from a search node to reach the goal.
    @param make_open_entry An optional parameter to change the bahavior of the
                           astar search. The callable should return a search
                           node, possible values are ordered_node_astar,
                           ordered_node_weighted_astar and
                           ordered_node_greedy_best_first with obvious
                           meanings.
    """
    logging.warning(f"unrecognized keywords for astar_search (ignored): {kwargs}")
    open = []
    state_g = {task.initial_state: 0}
    state_h = {}
    node_tiebreaker = 0

    root = searchspace.make_root_node(task.initial_state)
    init_h = heuristic(root)
    state_h[task.initial_state] = init_h
    heapq.heappush(open, make_open_entry(root, init_h, node_tiebreaker))
    logging.info("Initial h value: %f" % init_h)

    besth = float("inf")
    counter = 0
    result = SearchResult(
        expansions  = 0,
        generations = 0,
        evaluations = 1,
        elapsed     = 0.0)
    # The number of heuristic evaluations.
    # Note that this is not the number of g-value update, which is also called evaluations.
    # It is 1 because we have already evaluated init_h.

    time1 = time.process_time()
    def check_limit():
        result.rss = psutil.Process(os.getpid()).memory_info().rss
        result.elapsed = time.process_time() - time1
        return limit.satisfy(result)
    while open and check_limit():
        (f, h, _tie, pop_node) = heapq.heappop(open)
        if h < besth:
            besth = h
            logging.debug("Found new best h: %d after %d expansions" % (besth, counter))

        pop_state = pop_node.state
        # Only expand the node if its associated cost (g value) is the lowest
        # cost known for this state. Otherwise we already found a cheaper
        # path after creating this node and hence can disregard it.
        if state_g[pop_state] == pop_node.g:
            result.expansions += 1

            if task.goal_reached(pop_state):
                logging.info("Goal reached. Start extraction of solution.")
                logging.info("%d Nodes expanded" % result.expansions)
                result.goal_node = pop_node
                return result
            rplan = None
            if use_relaxed_plan:
                (rh, rplan) = heuristic.calc_h_with_plan(
                    searchspace.make_root_node(pop_state)
                )
                logging.debug("relaxed plan %s " % rplan)

            for op, succ_state in task.get_successor_states(pop_state):
                result.generations += 1
                if use_relaxed_plan:
                    if rplan and not op.name in rplan:
                        # ignore this operator if we use the relaxed plan
                        # criterion
                        logging.debug(
                            "removing operator %s << not a "
                            "preferred operator" % op.name
                        )
                        continue
                    else:
                        logging.debug("keeping operator %s" % op.name)

                succ_node = searchspace.make_child_node(pop_node, op, succ_state)

                if early_goal_detection and task.goal_reached(succ_state):
                    logging.info("Goal reached (early goal detection).")
                    logging.info("%d Nodes expanded" % result.expansions)
                    result.goal_node = succ_node
                    return result

                h = heuristic(succ_node)

                if succ_state not in state_h:
                    result.evaluations += 1
                    h = heuristic(succ_node)
                    state_h[succ_state] = h # cache heuristics
                else:
                    h = state_h[succ_state] # cached heuristics
                if h == float("inf"):
                    # don't bother with states that can't reach the goal anyway
                    continue
                old_succ_g = state_g.get(succ_state, float("inf"))
                if succ_node.g < old_succ_g:
                    # We either never saw succ_state before, or we found a
                    # cheaper path to succ_state than previously.
                    node_tiebreaker += 1
                    heapq.heappush(open, make_open_entry(succ_node, h, node_tiebreaker))
                    state_g[succ_state] = succ_node.g

        counter += 1
    logging.info("No operators left and task unsolvable, or exceeded the search limit")
    return result
