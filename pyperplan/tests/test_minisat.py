import pytest

from pyperplan import tools
from pyperplan.search import minisat


def get_long_formula(len):
    formula = []
    result = []
    for i in range(len):
        formula.append(["v" + str(i)])
        result.append("v" + str(i))
    return (formula, result)


@pytest.mark.skipif(not minisat.minisat_available(), reason="minisat missing")
@pytest.mark.parametrize(
    "formula,expected",
    [
        ([[]], []),
        ([["v1"]], ["v1"]),
        ([["not-v1"]], ["not-v1"]),
        ([["v1"], ["v2"]], ["v1", "v2"]),
        ([["v1", "v2"], ["not-v1"]], ["not-v1", "v2"]),
        ([["a-0"]], ["a-0"]),
        (["a-0"], ["a-0"]),
        get_long_formula(100),
    ],
)
def test_minisat(formula, expected):
    assert minisat.solve(formula) == expected


def teardown_module(module):
    for filename in (minisat.INPUT, minisat.OUTPUT):
        tools.remove(filename)
