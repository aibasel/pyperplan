"""
Unit test for searchalgorithms.py
"""

from search import breadth_first_search
from . import dummy_task


def test_breadth_first_search_at_goal():
    # plan of length 0, start == goal
    task = dummy_task.get_search_space_at_goal()
    solution = breadth_first_search(task)
    print(solution)
    assert solution != None
    assert len(solution) == 0


def test_breadth_first_search_no_solution():
    # plan with no solution
    task = dummy_task.get_search_space_no_solution()
    solution = breadth_first_search(task)
    print(solution)
    assert solution == None


def test_breadth_first_search_three_step():
    # plan of length 3
    task = dummy_task.get_simple_search_space()
    solution = breadth_first_search(task)
    print(solution)
    assert solution != None
    assert len(solution) == 3


def test_breadth_first_search_four_step():
    # plan of length 4
    task = dummy_task.get_simple_search_space_2()
    solution = breadth_first_search(task)
    print(solution)
    assert solution != None
    assert len(solution) == 4
