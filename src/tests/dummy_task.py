# -*- coding: utf-8 -*-

# Test file with simple addition and subtraction Search_Spaces.
# States: integer numbers between 0 and 10.
# Actions: add 1, 2, sub 1

from heuristics.heuristic_base import Heuristic


class DummyHeuristic (Heuristic):
    def __init__(self, task):
        self.goal_state = task.goals

    def __call__(self, node):
        return abs(self.goal_state - node.state)


class Search_Space:
    """
    The Search_Space consisting of name, the initial state (starting number)
    and the goal. The stop-variable is for the purpose if the Search_Space
    reaches the 10, no further successor states are produced. This was
    necessary because no duplication detection was possible for this simple
    class. In this example only one goal state (representing a number) was
    used.
    """
    def __init__(self, name, initial_state, goals):
        self.name = name
        self.initial_state = initial_state
        self.goals = goals

    def init(self):
        """
        Returns the initial state.
        """
        return self.initial_state

    def goal_reached(self, state):
        """
        If goal is reached (start number and goal number are equal) return
        True.
        """
        return (self.goals == state)

    def get_successor_states(self, state):
        """
        Three operators were defined: Subtract one, Add one, Add two.
        For the 5to20-Search_Space that should represent an unsolvable
        Search_Space the production of successor states was stopped completely
        when the value 10 was reached, simulating the case that no new states
        (different from these of the duplicates) can be found.

        The number range goes from 0 to 10. So there is no successor state with
        a value smaller than 0 and bigger than 10.
        """
        successors = []
        if 0 < state:
            successors.append(("sub1", state - 1))
        if state < 9:
            successors.append(("add2", state + 2))
        if state < 10:
            successors.append(("add1", state + 1))
        return successors


def get_simple_search_space():
    """
    Simple Search_Space that can be solved by applying 3 actions, two additions
    of two and one addition of one.
    Start number: 5
    Goal number: 10
    """
    return Search_Space("5+2+2+1", 5, 10)


def get_simple_search_space_2():
    """
    Simple Search_Space that can be solved by applying 4 actions, four
    subtractions of one.
    Start number: 5
    Goal number: 1
    """
    return Search_Space("5-1-1-1-1", 5, 1)


def get_search_space_at_goal():
    """
    Simple Search_Space that can be solved without applying any actions. Goal
    state is already reached in the start state.
    Start number: 5
    Goal number: 5
    """
    return Search_Space("5+nothing", 5, 5)


def get_search_space_no_solution():
    """
    Simple Search_Space that cannot be solved by applying actions, because goal
    number lies outside the number range.
    Start number: 5
    Goal number: 20
    """
    return Search_Space("5to20", 5, 20)
