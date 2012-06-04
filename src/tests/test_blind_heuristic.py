from heuristics.blind import BlindHeuristic

from search import searchspace
from task import *


def _get_simple_task():
    """
    Task with a goal with two facts and an operator with no effect.
    """
    op1 = Operator('op1', {'var1'}, {'var2'}, set())
    op2 = Operator('op2', {'var1'}, set(), set())
    op3 = Operator('op3', {'var2'}, {'var1'}, set())
    init = frozenset(['var1'])
    goals = frozenset(['var1', 'var2'])
    task1 = Task('task1', {'var1', 'var2', 'var3'}, init, goals,
                 [op1, op2, op3])
    return task1


def test_blind_heuristic_start():
    task = _get_simple_task()
    bh = BlindHeuristic(task)
    assert bh(searchspace.make_root_node(task.initial_state)) == 1


def test_blind_heuristic_goal():
    task = _get_simple_task()
    bh = BlindHeuristic(task)
    assert bh(searchspace.make_root_node(task.goals)) == 0
