import py.test

from search import minisat
from search import sat
from task import Operator, Task
import tools


def assert_true(value):
    assert value


def assert_false(value):
    assert not value


def assert_equal(result, expected):
    assert result == expected


def compare(input, expected_result):
    if not minisat.minisat_available():
        py.test.skip('minisat missing')
    solution = minisat.solve(input)
    assert solution == expected_result


def get_long_formula(len):
    formula = []
    result = []
    for i in range(len):
        formula.append(['v' + str(i)])
        result.append('v' + str(i))
    return (formula, result)


def test_minisat():
    expected = [([[]], []),
                ([['v1']], ['v1']),
                ([['not-v1']], ['not-v1']),
                ([['v1'], ['v2']], ['v1', 'v2']),
                ([['v1', 'v2'], ['not-v1']], ['not-v1', 'v2']),
                ([['a-0']], ['a-0']),
                (['a-0'], ['a-0']),
                get_long_formula(100)]

    for input, expected_result in expected:
        yield compare, input, expected_result


def teardown_module(module):
    for filename in (minisat.INPUT, minisat.OUTPUT):
        tools.remove(filename)
