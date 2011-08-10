"""
Tests for the task.py module
"""
import py

from task import Task, Operator

s1 = frozenset(['var1'])
s2 = frozenset(['var2'])
s3 = frozenset(['var1', 'var2'])
op1 = Operator('op1', {'var1'}, {'var2'}, set())
op2 = Operator('op1', {'var1'}, set(), set())
op3 = Operator('op1', {'var2'}, {'var1'}, set())

# Operator that makes var2 true and false
op4 = Operator('op1', {'var1'}, {'var2'}, {'var2'})


init = frozenset(['var1'])
goals = frozenset(['var1', 'var2'])
task1 = Task('task1', {'var1', 'var2', 'var3'}, init, goals, [op1, op2, op3])


def test_op_applicable1():
    assert op1.applicable(s1)


def test_op_applicable2():
    assert not op1.applicable(s2)


def test_op_applicable3():
    assert op1.applicable(s3)


def test_op_application1():
    assert op1.apply(s1) == {'var1', 'var2'}


def test_op_application2():
    with py.test.raises(AssertionError):
        op1.apply(s2)


def test_op_application3():
    """ Test that delete-effects are applied before add-effects """
    assert op4.apply(s1) == {'var1', 'var2'}


def test_task_successors1():
    # op3 is not applicable
    assert task1.get_successor_states(init) == \
        [(op1, {'var1', 'var2'}), (op2, {'var1'})]


def test_task_successors2():
    # no precondition of any operator is satisfied
    assert task1.get_successor_states({'var3'}) == []


def test_task_goal_reached1():
    assert not task1.goal_reached(init)


def test_task_goal_reached2():
    assert task1.goal_reached({'var1', 'var2'})
