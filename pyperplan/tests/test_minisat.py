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


def test_cnf_writer(tmp_path, monkeypatch):
    """Characterize CnfWriter.write so refactors stay behavior-preserving.

    Exercises a bare literal, single- and multi-literal conjunctions (which are
    collapsed via auxiliary AND variables), and an iff literal (which adds its
    own auxiliary clauses). Does not require minisat.
    """
    monkeypatch.chdir(tmp_path)
    formula = [
        "lit0",
        [["a", "b", "c"], ["d"]],
        [["x<->y", "e"]],
    ]
    mapping = minisat.CnfWriter().write(formula)
    assert mapping == {
        "lit0": 1,
        "a": 3,
        "b": 4,
        "c": 6,
        "d": 7,
        "x": 9,
        "y": 10,
        "e": 12,
    }
    cnf = (tmp_path / minisat.INPUT).read_text()
    assert cnf == (
        "1 0\n"
        "-2 3 0\n"
        "-2 4 0\n"
        "-3 -4 2 0\n"
        "-5 2 0\n"
        "-5 6 0\n"
        "-2 -6 5 0\n"
        "5 7 0\n"
        "8 9 10 0\n"
        "8 -9 -10 0\n"
        "-8 9 -10 0\n"
        "-8 -9 10 0\n"
        "-11 8 0\n"
        "-11 12 0\n"
        "-8 -12 11 0\n"
        "11 0\n"
    )


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
