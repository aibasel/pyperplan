from task import Task, Operator
from heuristics.lm_cut import LmCutHeuristic
from pddl.parser import Parser
from search import astar_search, enforced_hillclimbing_search
from .heuristic_test_instances import *
from search import make_root_node
import grounding


import py.test

"""
Test problems
"""


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


def _get_simple_task_unsolvable():
    """
    Unsolvable task.
    """
    op1 = Operator('op1', {'var1'}, {'var2'}, set())
    op2 = Operator('op2', {'var1'}, set(), set())
    op3 = Operator('op3', {'var2'}, {'var1'}, set())
    init = frozenset(['var1'])
    goals = frozenset(['var1', 'var3'])
    task1 = Task('task1', {'var1', 'var2', 'var3'}, init, goals,
                 [op1, op2, op3])
    return task1


def _get_simple_task_at_goal():
    """
    Goal is already reached in the initial state.
    """
    op1 = Operator('op1', {'var1'}, {'var2'}, set())
    op2 = Operator('op2', {'var1'}, set(), set())
    op3 = Operator('op3', {'var2'}, {'var1'}, set())
    init = frozenset(['var1'])
    goals = frozenset(['var1'])
    task1 = Task('task1', {'var1', 'var2', 'var3'}, init, goals,
                 [op1, op2, op3])
    return task1


def _get_simple_task_always_true():
    """
    Simple test task with one operator needed.
    """
    op1 = Operator('op1', {}, {'var2'}, set())
    op2 = Operator('op2', {'var1'}, set(), set())
    op3 = Operator('op3', {'var2'}, {'var1'}, set())
    init = frozenset(['var1'])
    goals = frozenset(['var1', 'var2'])
    task1 = Task('task1', {'var1', 'var2', 'var3'}, init, goals,
                 [op1, op2, op3])
    return task1


def _get_intermediate_task():
    """
    Intermediate test task with four operators needed.
    """
    op1 = Operator('op1', {'v1'}, {'v2'}, set())
    op2 = Operator('op2', {'v2'}, {'v3'}, set())
    op3 = Operator('op3', {'v3'}, {'v4', 'v5'}, set())
    op4 = Operator('op4', {'v4', 'v5'}, {'g'}, set())
    op5 = Operator('op5', {'v2'}, {'v6'}, set())
    op6 = Operator('op6', {'v6'}, {'v5'}, set())
    init = frozenset(['v1'])
    goals = frozenset(['g'])
    task1 = Task('task1', {'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'g'}, init,
                 goals, [op1, op2, op3, op4, op5, op6])
    return task1


def _get_intermediate_task2():
    """
    Intermediate task
    """
    op1 = Operator('op1', {'v1'}, {'v2'}, set())
    op2 = Operator('op2', {'v2'}, {'v3'}, set())
    op3 = Operator('op3', {'v3'}, {'v4', 'v5'}, set())
    op4 = Operator('op4', {'v7', 'v5'}, {'g'}, set())
    op7 = Operator('op7', {'v4'}, {'v7'}, set())
    op5 = Operator('op5', {'v2'}, {'v6'}, set())
    op6 = Operator('op6', {'v6'}, {'v5'}, set())
    init = frozenset(['v1'])
    goals = frozenset(['g'])
    task1 = Task('task1', {'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'g'},
                 init, goals, [op1, op2, op3, op4, op5, op6, op7])
    return task1


def _get_intermediate_task_two_initial_facts():
    """
    Intermediate task with two initial facts
    """
    op2 = Operator('op2', {'v1', 'v2'}, {'v3'}, set())
    op3 = Operator('op3', {'v3'}, {'v4', 'v5'}, set())
    op4 = Operator('op4', {'v7', 'v5'}, {'g'}, set())
    op7 = Operator('op7', {'v4'}, {'v7'}, set())
    op5 = Operator('op5', {'v2'}, {'v6'}, set())
    op6 = Operator('op6', {'v6'}, {'v5'}, set())
    init = frozenset(['v1', 'v2'])
    goals = frozenset(['g'])
    task1 = Task('task1', {'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'g'},
                 init, goals, [op2, op3, op4, op5, op6, op7])
    return task1


def _get_intermediate_task_two_paths():
    """
    Intermediate task with two possible paths.
    """
    op1 = Operator('op1', {'v1'}, {'v2'}, set())
    op2 = Operator('op2', {'v2'}, {'v3'}, set())
    op3 = Operator('op3', {'v3'}, {'v4', 'v5'}, set())
    op4 = Operator('op4', {'v7', 'v5'}, {'g'}, set())
    op7 = Operator('op7', {'v4'}, {'v7'}, set())
    op5 = Operator('op5', {'v2'}, {'v4', 'v5'}, set())
    init = frozenset(['v1'])
    goals = frozenset(['g'])
    task1 = Task('task1', {'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'g'},
                 init, goals, [op1, op2, op3, op4, op5, op7])
    return task1

"""
Tests
"""


def test_lm_cut_relaxed_operators():
    # define a simple test task
    task1 = _get_simple_task()
    # test the relaxed operator generation
    heuristic = LmCutHeuristic(task1)
    assert heuristic.relaxed_facts['GOAL']
    assert heuristic.relaxed_facts['var1']
    assert heuristic.relaxed_facts['var2']
    assert heuristic.relaxed_facts['var3']
    assert 'GOALOP' in [o.name
                        for o in heuristic.relaxed_facts['GOAL'].effect_of]
    assert not heuristic.relaxed_facts['GOAL'].precondition_of
    assert ([o.name
            for o in heuristic.relaxed_facts['var1'].precondition_of] ==
            ['op1', 'op2', 'GOALOP'])
    assert ([o.name for o in heuristic.relaxed_facts['var1'].effect_of] ==
            ['op3'])
    assert ([o.name
            for o in heuristic.relaxed_facts['var2'].precondition_of] ==
            ['op3', 'GOALOP'])
    assert ([o.name for o in heuristic.relaxed_facts['var2'].effect_of] ==
            ['op1'])
    assert heuristic.relaxed_facts['var3'].precondition_of == []
    assert heuristic.relaxed_facts['var3'].effect_of == []
    assert heuristic.relaxed_ops['GOALOP']
    assert heuristic.relaxed_ops['op1']
    assert heuristic.relaxed_ops['op2']
    assert heuristic.relaxed_ops['op3']
    assert heuristic.relaxed_ops['GOALOP'].cost == 0
    assert (sorted(f.name
                   for f in heuristic.relaxed_ops['GOALOP'].precondition) ==
            ['var1', 'var2'])
    assert [f.name
            for f in heuristic.relaxed_ops['GOALOP'].effects] == ['GOAL']
    assert heuristic.relaxed_ops['op1'].cost == 1
    assert [f.name
            for f in heuristic.relaxed_ops['op1'].precondition] == ['var1']
    assert [f.name for f in heuristic.relaxed_ops['op1'].effects] == ['var2']
    assert heuristic.relaxed_ops['op2'].cost == 1
    assert [f.name
            for f in heuristic.relaxed_ops['op2'].precondition] == ['var1']
    assert heuristic.relaxed_ops['op2'].effects == []
    assert heuristic.relaxed_ops['op3'].cost == 1
    assert [f.name
            for f in heuristic.relaxed_ops['op3'].precondition] == ['var2']
    assert [f.name for f in heuristic.relaxed_ops['op3'].effects] == ['var1']
    assert not 'ALWAYSTRUE' in heuristic.relaxed_facts


def test_lm_cut_relaxed_operators2():
    # define a simple test task
    task1 = _get_simple_task_always_true()
    # test the relaxed operator generation
    heuristic = LmCutHeuristic(task1)
    assert 'ALWAYSTRUE' in heuristic.relaxed_facts


def test_lm_cut_hmax_simple():
    # define a simple test task
    task1 = _get_simple_task()
    heuristic = LmCutHeuristic(task1)
    heuristic.compute_hmax(task1.initial_state)
    assert heuristic.relaxed_facts['var1'].hmax_value == 0.
    assert heuristic.relaxed_facts['var2'].hmax_value == 1.
    assert heuristic.relaxed_facts['var3'].hmax_value == float('inf')
    assert heuristic.relaxed_facts['GOAL'].hmax_value == 1.


def test_lm_cut_hmax_intermediate():
    task1 = _get_intermediate_task()
    heuristic = LmCutHeuristic(task1)
    heuristic.compute_hmax(task1.initial_state)
    assert heuristic.relaxed_facts['v1'].hmax_value == 0.
    assert heuristic.relaxed_facts['v2'].hmax_value == 1.
    assert heuristic.relaxed_facts['v3'].hmax_value == 2.
    assert heuristic.relaxed_facts['v6'].hmax_value == 2.
    assert heuristic.relaxed_facts['v4'].hmax_value == 3.
    assert heuristic.relaxed_facts['v5'].hmax_value == 3.
    assert heuristic.relaxed_facts['g'].hmax_value == 4.
    assert heuristic.relaxed_ops['op1'].hmax_supporter.name == 'v1'
    assert heuristic.relaxed_ops['op2'].hmax_supporter.name == 'v2'
    assert heuristic.relaxed_ops['op3'].hmax_supporter.name == 'v3'
    assert heuristic.relaxed_ops['op4'].hmax_supporter.name in {'v4', 'v5'}
    assert heuristic.relaxed_ops['op5'].hmax_supporter.name == 'v2'
    assert heuristic.relaxed_ops['op6'].hmax_supporter.name == 'v6'


def test_lm_cut_hmax_intermediate2():
    task1 = _get_intermediate_task2()
    heuristic = LmCutHeuristic(task1)
    heuristic.compute_hmax(task1.initial_state)
    assert heuristic.relaxed_facts['v1'].hmax_value == 0.
    assert heuristic.relaxed_facts['v2'].hmax_value == 1.
    assert heuristic.relaxed_facts['v3'].hmax_value == 2.
    assert heuristic.relaxed_facts['v6'].hmax_value == 2.
    assert heuristic.relaxed_facts['v4'].hmax_value == 3.
    assert heuristic.relaxed_facts['v5'].hmax_value == 3.
    assert heuristic.relaxed_facts['v7'].hmax_value == 4.
    assert heuristic.relaxed_facts['g'].hmax_value == 5.
    assert heuristic.relaxed_ops['op1'].hmax_supporter.name == 'v1'
    assert heuristic.relaxed_ops['op2'].hmax_supporter.name == 'v2'
    assert heuristic.relaxed_ops['op3'].hmax_supporter.name == 'v3'
    assert heuristic.relaxed_ops['op4'].hmax_supporter.name == 'v7'
    assert heuristic.relaxed_ops['op5'].hmax_supporter.name == 'v2'
    assert heuristic.relaxed_ops['op6'].hmax_supporter.name == 'v6'


def test_lm_cut_hmax_intermediate_two_paths():
    task1 = _get_intermediate_task_two_paths()
    heuristic = LmCutHeuristic(task1)
    heuristic.compute_hmax(task1.initial_state)
    assert heuristic.relaxed_facts['v1'].hmax_value == 0.
    assert heuristic.relaxed_facts['v2'].hmax_value == 1.
    assert heuristic.relaxed_facts['v3'].hmax_value == 2.
    assert heuristic.relaxed_facts['v6'].hmax_value == float('inf')
    assert not heuristic.relaxed_facts['v6'] in heuristic.reachable
    assert heuristic.relaxed_facts['v4'].hmax_value == 2.
    assert heuristic.relaxed_facts['v5'].hmax_value == 2.
    assert heuristic.relaxed_facts['v7'].hmax_value == 3.
    assert heuristic.relaxed_facts['g'].hmax_value == 4.
    assert heuristic.relaxed_ops['op1'].hmax_supporter.name == 'v1'
    assert heuristic.relaxed_ops['op2'].hmax_supporter.name == 'v2'
    assert heuristic.relaxed_ops['op3'].hmax_supporter.name == 'v3'
    assert heuristic.relaxed_ops['op4'].hmax_supporter.name == 'v7'
    assert heuristic.relaxed_ops['op5'].hmax_supporter.name == 'v2'


def test_lm_cut_mark_single_goal():
    task = _get_intermediate_task()
    heuristic = LmCutHeuristic(task)
    heuristic.compute_hmax(task.initial_state)
    heuristic.compute_goal_plateau(heuristic.explicit_goal)
    assert {f.name
            for f in heuristic.goal_plateau} == {heuristic.explicit_goal, 'g'}


def test_lm_cut_unsolvable():
    task = _get_simple_task_unsolvable()
    heuristic = LmCutHeuristic(task)
    h_val = heuristic(make_root_node(task.initial_state))
    heuristic.compute_goal_plateau(heuristic.explicit_goal)
    assert h_val == float('inf')


def test_lm_cut_at_goal():
    task = _get_simple_task_at_goal()
    heuristic = LmCutHeuristic(task)
    h_val = heuristic(make_root_node(task.initial_state))
    heuristic.compute_goal_plateau(heuristic.explicit_goal)
    assert h_val == 0.


def test_lm_cut_mark_multiple_goal():
    task = _get_intermediate_task()
    heuristic = LmCutHeuristic(task)
    heuristic.compute_hmax(task.initial_state)
    # artificially alter operator costs to get a larger goal plateau
    heuristic.relaxed_ops['op4'].cost = 0.
    heuristic.compute_goal_plateau(heuristic.explicit_goal)
    assert ({f.name for f in heuristic.goal_plateau} in
            [{heuristic.explicit_goal, 'v4', 'g'},
             {heuristic.explicit_goal, 'v5', 'g'}])


def test_two_times_hmax_same_result():
    task = _get_intermediate_task()
    heuristic = LmCutHeuristic(task)
    heuristic.compute_hmax(task.initial_state)
    heuristic.compute_hmax(task.initial_state)
    # artificially alter operator costs to get a larger goal plateau
    heuristic.relaxed_ops['op4'].cost = 0.
    heuristic.compute_goal_plateau(heuristic.explicit_goal)
    assert ({f.name for f in heuristic.goal_plateau} in
            [{heuristic.explicit_goal, 'v4', 'g'},
             {heuristic.explicit_goal, 'v5', 'g'}])


def test_lm_cut_compute_single_cut():
    task1 = _get_intermediate_task_two_paths()
    heuristic = LmCutHeuristic(task1)
    heuristic.compute_hmax(task1.initial_state)
    heuristic.goal_plateau.clear()
    heuristic.compute_goal_plateau(heuristic.explicit_goal)
    cut = heuristic.find_cut(task1.initial_state)
    assert [op.name for op in cut] == ['op4']


def test_lm_cut_heuristic_value():
    task1 = _get_intermediate_task_two_paths()
    heuristic = LmCutHeuristic(task1)
    h_val = heuristic(make_root_node(task1.initial_state))
    assert h_val == 4.


def test_lm_cut_heuristic_value_two_initial_facts():
    task1 = _get_intermediate_task_two_initial_facts()
    heuristic = LmCutHeuristic(task1)
    h_val = heuristic(make_root_node(task1.initial_state))
    assert h_val == 4.


def test_lm_cut_heuristic_value_simple_task_always_true():
    task1 = _get_simple_task_always_true()
    heuristic = LmCutHeuristic(task1)
    h_val = heuristic(make_root_node(task1.initial_state))
    #print('Printing goal plateau')
    #for f in heuristic.goal_plateau:
    #    print(repr(f))
    #print('Printing cut')
    #for op in cut:
    #    print(repr(op))
    assert h_val == 1.


def test_lm_cut_blocksworld_initial_state():
    parser = Parser('')
    parser.domInput = blocks_dom
    parser.probInput = blocks_problem_1

    domain = parser.parse_domain(False)
    problem = parser.parse_problem(domain, False)

    task = grounding.ground(problem)

    heuristic = LmCutHeuristic(task)
    h_val = heuristic(make_root_node(task.initial_state))
    assert h_val == 6.


def test_lm_cut_blocksworld_complete_astar():
    # run through plan and validate heuristic value
    # the true_h_values are taken from fast downward with astar and lm cut
    # heuristic
    true_h_values = [6., 5., 4., 3., 2., 1., 0.]
    plan_length = 6
    yield py.test.mark.slow(gen_blocks_test_astar), LmCutHeuristic, \
        true_h_values, plan_length


def test_lm_cut_blocksworld_complete_enforced_hillclimbing():
    true_h_values = [6.0, 5.0, 5.0, 4.0, 5.0, 5.0, 6.0, 5.0, 4.0, 3.0, 2.0,
                     1.0, 0.0]
    plan_length = 16
    # TODO: Result is currently undeterministic.
    #yield py.test.mark.slow(gen_blocks_test_ehc), LmCutHeuristic, \
    #    true_h_values, plan_length
