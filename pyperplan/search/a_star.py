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
import random

from . import searchspace


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


def greedy_best_first_search(task, heuristic, use_relaxed_plan=False):
    """
    Searches for a plan in the given task using greedy best first search.

    @param task The task to be solved.
    @param heuristic A heuristic callable which computes the estimated steps
                     from a search node to reach the goal.
    """

    return astar_search(
        task, heuristic, ordered_node_greedy_best_first, use_relaxed_plan
    )


def weighted_astar_search(task, heuristic, weight=5, use_relaxed_plan=False):
    """
    Searches for a plan in the given task using A* search.

    @param task The task to be solved.
    @param heuristic  A heuristic callable which computes the estimated steps.
                      from a search node to reach the goal.
    @param weight A weight to be applied to the heuristics value for each node.
    """
    return astar_search(
        task, heuristic, ordered_node_weighted_astar(weight), use_relaxed_plan
    )


def astar_search(
    task, heuristic, make_open_entry=ordered_node_astar, use_relaxed_plan=False
):
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
    open = []
    state_cost = {task.initial_state: 0}
    node_tiebreaker = 0

    root = searchspace.make_root_node(task.initial_state)
    init_h = heuristic(root)
    heapq.heappush(open, make_open_entry(root, init_h, node_tiebreaker))
    logging.info("Initial h value: %f" % init_h)

    besth = float("inf")
    counter = 0
    expansions = 0

    while open:
        (f, h, _tie, pop_node) = heapq.heappop(open)
        if h < besth:
            besth = h
            logging.debug("Found new best h: %d after %d expansions" % (besth, counter))

        pop_state = pop_node.state
        # Only expand the node if its associated cost (g value) is the lowest
        # cost known for this state. Otherwise we already found a cheaper
        # path after creating this node and hence can disregard it.
        if state_cost[pop_state] == pop_node.g:
            expansions += 1

            if task.goal_reached(pop_state):
                logging.info("Goal reached. Start extraction of solution.")
                logging.info("%d Nodes expanded" % expansions)
                return pop_node.extract_solution()
            rplan = None
            if use_relaxed_plan:
                (rh, rplan) = heuristic.calc_h_with_plan(
                    searchspace.make_root_node(pop_state)
                )
                logging.debug("relaxed plan %s " % rplan)

            for op, succ_state in task.get_successor_states(pop_state):
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
                h = heuristic(succ_node)
                if h == float("inf"):
                    # don't bother with states that can't reach the goal anyway
                    continue
                old_succ_g = state_cost.get(succ_state, float("inf"))
                if succ_node.g < old_succ_g:
                    # We either never saw succ_state before, or we found a
                    # cheaper path to succ_state than previously.
                    node_tiebreaker += 1
                    heapq.heappush(open, make_open_entry(succ_node, h, node_tiebreaker))
                    state_cost[succ_state] = succ_node.g

        counter += 1
    logging.info("No operators left. Task unsolvable.")
    logging.info("%d Nodes expanded" % expansions)
    return None


def random_walk(task, heuristic, action_sequence, current_state, h_min, max_walk_len, restart_probability):
    walk_len = 0
    sampled_node = current_state
    # print(f"current heuristic min: {heuristic(sampled_node)}")
    restart_probability = restart_probability * 100

    while walk_len < max_walk_len:    # restart hardcoded threshold t_g = 100

        print(f"random_walk: current h = {heuristic(sampled_node)}, walk length = {walk_len}")
        sampled_state = sampled_node.state
        # print("test", sampled_state)
        sampled_actions = task.get_successor_states(sampled_state)
        num_applicable_actions = len(sampled_actions)
        
        # print("Test", actions)
        if num_applicable_actions == 0 or heuristic(sampled_node) == float("inf"):
            return sampled_node, walk_len    # dead end situation
        
        random_num = random.randint(0,num_applicable_actions-1)     # perform random action selection
        chosen_operator = sampled_actions[random_num][0]
        chosen_succ_state = sampled_actions[random_num][1]
        action_sequence.append((chosen_operator, chosen_succ_state))

        sampled_node = searchspace.make_child_node(sampled_node, chosen_operator, chosen_succ_state)    # the successor node object
        sampled_node_state = sampled_node.state
        h_succ = heuristic(sampled_node)
        succ_actions = task.get_successor_states(sampled_node_state)

        walk_len += 1   # setting counter for the restart threshold 

        if h_succ < h_min or task.goal_reached(sampled_node_state):
            # walk_len += 1
            # print(f"h decreased, walk length: {walk_len}")
            # print(f"current h = {heuristic(sampled_node)}, walk length = {walk_len}")
            return sampled_node, walk_len
        
        restart_rv = random.randint(1,100)
        if restart_rv <= restart_probability: 
            print(restart_rv, restart_probability, "test: restart probability condition hit", h_min, h_succ)
            print("len action seq", len(action_sequence))
            walk_len = 0
            return searchspace.make_root_node(task.initial_state), walk_len     # restarting probability condition based on r_p



    return sampled_node, walk_len

def monte_carlo_rrw_search(
    task, heuristic, max_walk_len=100, restart_probability=0.2, time_limit=3000, make_open_entry=ordered_node_greedy_best_first, use_relaxed_plan=False,
):
    """
    Searches for a plan in the given task using monte carlo RRW search.

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
    state_cost = {task.initial_state: 0}
    node_tiebreaker = 0

    root = searchspace.make_root_node(task.initial_state)  # setting root node s_0

    init_h = heuristic(root)  # setting initial heuristic
    h_min = heuristic(root)

    current_state = make_open_entry(root, init_h, node_tiebreaker)[-1]  # setting current state to initial state (returns (f, h, node_tiebreaker, node))


    logging.info("Initial h value: %f" % init_h)

    expansions = 0
    time = 0 # setting counter for overall search time limit
    num_walks = 0
    action_sequence = []
    walk_len = 0

    while time < time_limit: 
        sampled_node, walk_len = random_walk(task, heuristic, action_sequence, current_state, h_min, max_walk_len, restart_probability)   # sampled is a tuple containing (f, h, tiebreak, sampled_node). the sampled node itself is the last index
        h_sampled = heuristic(sampled_node)    # sampled_node is the node object
        # walk_len += 1
        print(f"monte_carlo_rrw_search: current h = {h_sampled}, walk length = {walk_len}")


        sampled_state = sampled_node.state

        num_applicable_actions = len(task.get_successor_states(sampled_state))

        if task.goal_reached(sampled_state):
            logging.info("Goal reached. Start extraction of solution.")
            logging.info("%d Nodes expanded" % expansions)
            print(f"length of plan: {len(action_sequence)}")
            # print([i[0] for i in action_sequence])        # checking the correct plan
            # sol = sampled_node.extract_solution()
            # print(sol)
            return sampled_node.extract_solution()  # TODO: look at details of extract_solution and chaining action sequences

        elif num_applicable_actions > 0 and h_sampled < h_min:  # successfully found new lowest h state, update current state to new lowest h state

            current_state = sampled_node
            # print(sampled)
            h_min = heuristic(sampled_node)
            # walk_len = 0
        

        
        else:   # restart r_p condition hit or max walk length hit 
            current_state = make_open_entry(root, init_h, node_tiebreaker)[-1]      # restart by setting current state = to initial state
            action_sequence = []
            h_min = heuristic(current_state)
            walk_len = 0
            print("restart condition hit", walk_len)

        num_walks += 1
        print(f"walk number {num_walks}")
        # print(f"current h = {heuristic(sampled_node)}, walk_length = {walk_len}")      # not
        time += 1
    #     (f, h, _tie, pop_node) = current_state #current_state returns (f, h, node_tiebreaker, node)
    #     # print(current_state)
    #     if h < h_min:
    #         h_min = h
    #         logging.debug("Found new best h: %d after %d expansions" % (h_min, counter))

    #     pop_state = pop_node.state
    #     # Only expand the node if its associated cost (g value) is the lowest
    #     # cost known for this state. Otherwise we already found a cheaper
    #     # path after creating this node and hence can disregard it.
    #     if state_cost[pop_state] == pop_node.g:
    #         expansions += 1

    #         if task.goal_reached(pop_state):
    #             logging.info("Goal reached. Start extraction of solution.")
    #             logging.info("%d Nodes expanded" % expansions)
    #             return pop_node.extract_solution()
    #         rplan = None
    #         if use_relaxed_plan:
    #             (rh, rplan) = heuristic.calc_h_with_plan(
    #                 searchspace.make_root_node(pop_state)
    #             )
    #             logging.debug("relaxed plan %s " % rplan)

    #         for op, succ_state in task.get_successor_states(pop_state):
    #             if use_relaxed_plan:
    #                 if rplan and not op.name in rplan:
    #                     # ignore this operator if we use the relaxed plan
    #                     # criterion
    #                     logging.debug(
    #                         "removing operator %s << not a "
    #                         "preferred operator" % op.name
    #                     )
    #                     continue
    #                 else:
    #                     logging.debug("keeping operator %s" % op.name)

    #             succ_node = searchspace.make_child_node(pop_node, op, succ_state)
    #             h = heuristic(succ_node)
    #             if h == float("inf"):
    #                 # don't bother with states that can't reach the goal anyway
    #                 continue
    #             old_succ_g = state_cost.get(succ_state, float("inf"))
    #             if succ_node.g < old_succ_g:
    #                 # We either never saw succ_state before, or we found a
    #                 # cheaper path to succ_state than previously.
    #                 node_tiebreaker += 1
    #                 heapq.heappush(open, make_open_entry(succ_node, h, node_tiebreaker))
    #                 state_cost[succ_state] = succ_node.g

    #     counter += 1
    #     time += 1
    # logging.info("No operators left. Task unsolvable.")
    # logging.info("%d Nodes expanded" % expansions)
    print("Time limit reached, failed to find a solution")
    return None