'''
Unit test for searchalgortihms.py

TODO: Duplicate pruning tests

@author: Gruppe3
'''

from search import iterative_deepening_search
from . import dummy_task


def test_iterative_deepening_search_at_goal():
    # plan of length 0, start == goal
    task = dummy_task.get_search_space_at_goal()
    solution = iterative_deepening_search(task)
    print(solution)
    assert solution is not None
    assert len(solution) == 0


def test_iterative_deepening_search_no_solution():
    # plan with no solution
    task = dummy_task.get_search_space_no_solution()
    solution = iterative_deepening_search(task, 10)
    print(solution)
    assert solution is None


def test_iterative_deepening_search_three_step():
    # plan of length 3
    task = dummy_task.get_simple_search_space()
    solution = iterative_deepening_search(task)
    print(solution)
    assert solution is not None
    assert len(solution) == 3


def test_iterative_deepening_search_four_step():
    # plan of length 4
    task = dummy_task.get_simple_search_space_2()
    solution = iterative_deepening_search(task)
    print(solution)
    assert solution is not None
    assert len(solution) == 4
