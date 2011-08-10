"""
Unit test for searchalgorithms_hillclimbing.py
"""

from search import enforced_hillclimbing_search
from . import dummy_task
from task import *


def test_enforced_hillclimbing_search_at_goal():
    """
    plan of length 0, start is equal to goal
    """
    task = dummy_task.get_search_space_at_goal()
    heuristic = dummy_task.DummyHeuristic(task)
    solution = enforced_hillclimbing_search(task, heuristic)
    print(solution)
    assert solution is not None
    assert len(solution) == 0


def test_enforced_hillclimbing_search_no_solution():
    """
    goal is not reachable
    """
    task = dummy_task.get_search_space_no_solution()
    heuristic = dummy_task.DummyHeuristic(task)
    solution = enforced_hillclimbing_search(task, heuristic)
    print(solution)
    assert solution is None


def test_enforced_hillclimbing_search_three_step():
    """
    plan with length 3
    """
    task = dummy_task.get_simple_search_space()
    heuristic = dummy_task.DummyHeuristic(task)
    solution = enforced_hillclimbing_search(task, heuristic)
    print(solution)
    assert solution is not None
    assert len(solution) == 3


def test_enforced_hillclimbing_search_four_step():
    """
    plan with length 4
    """
    task = dummy_task.get_simple_search_space_2()
    heuristic = dummy_task.DummyHeuristic(task)
    solution = enforced_hillclimbing_search(task, heuristic)
    print(solution)
    assert solution is not None
    assert len(solution) == 4
