import logging
import sys
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    stream=sys.stdout)

import py.test

from search import sat
from search import minisat
from task import Operator, Task
import tools


fact1 = "at-station"

op1 = Operator('op1', set(), {'a'}, set())
op2 = Operator('op2', set(), set(), {'c'})
op3 = Operator('op3', ['d'], ['a'], [])
op4 = Operator('op4', [], ['b'], [])

task1 = Task('task1', {'a'}, set(), {'a'}, [op1])
task2 = Task('task2', {'a', 'd'}, {'d'}, {'a'}, [op1, op3])
task3 = Task('task3', {'a', 'b'}, set(), {'a', 'b'}, [op1, op4])
task4 = Task('task4', {'a', 'd'}, {'d'}, {'a'}, [op3])
task5 = Task('trivial', {'a'}, {'a'}, {'a'}, [])

aux_a_iff_b = [['a<->b', 'a', 'b'], ['a<->b', 'not-a', 'not-b'],
          ['not-a<->b', 'a', 'not-b'], ['not-a<->b', 'not-a', 'b']]

aux_a_and_b = [['not-aANDb', 'a'], ['not-aANDb', 'b'], ['not-a', 'not-b',
                                                        'aANDb']]


def sort_formula(formula):
    # Move all literals to the front and all subformulas to the back.
    strings = [part for part in formula if isinstance(part, str)]
    lists = [part for part in formula if isinstance(part, list)]
    assert len(strings) + len(lists) == len(formula)
    return sorted(strings) + sorted(sort_formula(l) for l in lists)


def assert_true(value):
    assert value


def assert_false(value):
    assert not value


def assert_equal(result, expected):
    assert result == expected


def test_formula_string1():
    assert sat._formula_str(['a']) == '(a)'


def test_formula_string2():
    assert sat._formula_str(['a', 'b']) == '(a & b)'


def test_formula_string3():
    assert sat._formula_str(['a', ['b']]) == '(a & (b))'


def test_formula_string4():
    assert sat._formula_str(['a', ['b', 'c']]) == '(a & (b | c))'


def test_formula_string5():
    assert sat._formula_str(['a', ['b', ['c', 'd']]]) == '(a & (b | (c & d)))'


def test_index_fact1():
    assert sat.index_fact(fact1, 3) == "at-station-3"


def test_index_fact2():
    assert sat.index_fact(fact1, index=3, negated=True) == "not-at-station-3"


def test_fact_formula():
    pairs = [
             ((op1, 'a', 3), ['a-4']),
             ((op1, 'b', 3), ['b-4<->b-3']),
             ((op2, 'c', 3), ['not-c-4']),
             ((op2, 'b', 3), ['b-4<->b-3']),
            ]
    for input, expected in pairs:
        yield assert_equal, sat.get_formula_for_fact(*input), expected


def test_operator_formula1():
    assert sat.get_formula_for_operator(['a'], op1, 3) == ['a-4']


def test_operator_formula2():
    assert sat.get_formula_for_operator(['a', 'd'], op3, 3) == ['d-3', 'a-4',
                                                                'd-4<->d-3']


def test_plan_formula1():
    assert sat.get_plan_formula(task1, 1) == ['not-a-0', [['a-1']], 'a-1']


def test_plan_formula2():
    assert (sort_formula(sat.get_plan_formula(task2, 1)) ==
        ['a-1', 'd-0', 'not-a-0', [['a-1', 'd-0', 'd-1<->d-0'],
                                   ['a-1', 'd-1<->d-0']]])


def test_plan_formula3():
    assert (sort_formula(sat.get_plan_formula(task3, 1)) ==
        ['a-1', 'b-1', 'not-a-0', 'not-b-0', [['a-1', 'b-1<->b-0'],
                                              ['a-1<->a-0', 'b-1']]])


def test_plan_formula4():
    assert (sort_formula(sat.get_plan_formula(task4, 1)) ==
        ['a-1', 'd-0', 'not-a-0', [['a-1', 'd-0', 'd-1<->d-0']]])


def test_plan_formula5():
    assert sat.get_plan_formula(task5, 0) == ['a-0', 'a-0']


def test_plan_formula6():
    assert (sort_formula(sat.get_plan_formula(task2, 2)) ==
            ['a-2', 'd-0', 'not-a-0',
             [['a-1', 'd-0', 'd-1<->d-0'], ['a-1', 'd-1<->d-0']],
             [['a-2', 'd-1', 'd-2<->d-1'], ['a-2', 'd-2<->d-1']]])


def test_extract_plan():
    op1 = Operator('op1', [], ['a'], [])
    op2 = Operator('op2', ['a'], ['b'], [])
    op3 = Operator('op3', ['a', 'b'], ['c'], [])
    op4 = Operator('op4', [], ['a', 'b'], [])
    expected = [(['not-a-0', 'a-1'], [op1], [op1]),
                (['not-a-0', 'a-1', 'b-0', 'b-1'], [op1, op2], [op1]),
                (['not-a-0', 'a-1', 'not-b-0', 'not-b-1', 'a-2', 'b-2'],
                 [op1, op2], [op1, op2]),
                ([], [op1], []),
                (['a-0', 'not-b-0', 'not-c-0', 'a-1', 'b-1', 'not-c-1',
                  'a-2', 'b-2', 'c-2'], [op1, op2, op3], [op2, op3]),
                (['not-a-0, not-b-0', 'a-1', 'b-1'], [op1, op4], [op4])]

    for valuation, operators, plan in expected:
        extracted_plan = sat._extract_plan(operators, valuation)
        yield assert_equal, extracted_plan, plan


def check_plan(task, expected):
    if not minisat.minisat_available():
        py.test.skip('minisat missing')
    computed = sat.sat_solve(task, max_steps=5)
    assert computed == expected


def test_sat_solve():
    op1 = Operator('op1', set(), {'a'}, set())
    op2 = Operator('op2', set('a'), set('b'), set())
    op3 = Operator('op3', set(), {'a', 'b', 'c'}, set())
    op4 = Operator('op4', {'b'}, {'c'}, set())
    op5 = Operator('op5', {'b', 'c'}, {'d'}, set())
    op6 = Operator('op6', {'d'}, {'e', 'f'}, set())
    op7 = Operator('op7', {'a', 'c', 'f'}, {'g'}, set())

    task0 = Task('task0', {'a'}, {'a'}, {'a'}, [op1, op2])
    task1 = Task('task1', {'a'}, set(), {'a'}, [op1, op2])
    task2 = Task('task2', {'a', 'b'}, set(), {'b'}, [op1, op2])
    task3 = Task('task3', {'a', 'b', 'c'}, set(), {'c'}, [op1, op2])
    task4 = Task('task4', {'a', 'b', 'c'}, set(), {'c'}, [op1, op2, op3])
    task5 = Task('task5', {'a', 'b', 'c'}, set(), {'c'},
                 [op1, op2, op4])
    task6 = Task('task6', {'a', 'b', 'c', 'd'}, {'a'}, {'d'},
                 [op2, op4, op5])
    task7 = Task('task7c', {'a', 'b', 'c', 'd'}, {'a'}, {'d'},
                 [op3, op5])
    task8 = Task('task8', {'a', 'b', 'c', 'd', 'e', 'f', 'g'}, {'a'}, {'g'},
                 [op2, op3, op4, op5, op6, op7])

    op_a = Operator('op_a', set(), {'a'}, set())
    op_b = Operator('op_b', {'a'}, {'b'}, set())
    op_c = Operator('op_c', {'b'}, {'c'}, set())
    op_d = Operator('op_d', {'c'}, {'d'}, set())
    op_e = Operator('op_e', {'d'}, {'e'}, set())
    op_f = Operator('op_f', {'e'}, {'f'}, set())

    task_d = Task('task_a', {'a', 'b', 'c', 'd'}, set(), {'d'},
                  [op_a, op_b, op_c, op_d])
    task_e = Task('task_b', {'a', 'b', 'c', 'd', 'e'}, set(), {'e'},
                  [op_a, op_b, op_c, op_d, op_f])

    op_facts = Operator('op_facts', set(), {'a', 'b', 'c', 'd', 'e', 'f', 'g',
                                            'h', 'i', 'j', 'k', 'l', 'm', 'n',
                                            'o', 'p', 'q', 'r', 's', 't', 'u',
                                            'v', 'w'}, set())

    task_facts = Task('task_facts', {'a', 'b', 'c', 'd', 'e', 'f', 'g',
                                     'h', 'i', 'j', 'k', 'l', 'm', 'n',
                                     'o', 'p', 'q', 'r', 's', 't', 'u',
                                     'v', 'w'}, set(), {'v', 'w'}, [op_facts])

    op_delete_pre = Operator('delete_pre', {'a'}, {'b'}, {'a'})
    task_op_delete_pre = Task('op_delete_pre', {'a', 'b'}, {'a'}, {'b'},
                              [op_delete_pre])

    # Miconic: prob00.pddl (2 floors, 1 person):
    # <Op (depart f1 p0), PRE: frozenset({'(lift-at f1)', '(boarded p0)'}),
    #   ADD: frozenset({'(served p0)'}), DEL: frozenset({'(boarded p0)'})>,
    # <Op (board f0 p0), PRE: frozenset({'(lift-at f0)'}),
    #   ADD: frozenset({'(boarded p0)'}), DEL: frozenset()>,
    # <Op (up f0 f1), PRE: frozenset({'(lift-at f0)'}),
    #   ADD: frozenset({'(lift-at f1)'}), DEL: frozenset({'(lift-at f0)'})>]
    op_depart = Operator('depart', {'high', 'boarded'}, {'served'},
                         {'boarded'})
    op_board = Operator('board', {'low'}, {'boarded'}, set())
    op_up = Operator('up', {'low'}, {'high'}, {'low'})
    task_simple_miconic = Task('miconic-simple',
                               {'low', 'high', 'boarded', 'served'},
                               {'low'}, {'served'},
                               [op_depart, op_board, op_up])

    expected = [(task0, []),
                (task1, [op1]),
                (task2, [op1, op2]),
                (task3, None),
                (task4, [op3]),
                (task5, [op1, op2, op4]),
                (task6, [op2, op4, op5]),
                (task7, [op3, op5]),
                (task_facts, [op_facts]),
                (task_op_delete_pre, [op_delete_pre]),
                (task_simple_miconic, [op_board, op_up, op_depart])
                ]

    for task, plan in expected:
        yield check_plan, task, plan


def teardown_module(module):
    for filename in (minisat.INPUT, minisat.OUTPUT):
        tools.remove(filename)
