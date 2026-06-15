"""Smoke tests that every registered search algorithm and heuristic works.

These tests iterate over the planner's ``SEARCHES`` and ``HEURISTICS``
registries, so any newly added search algorithm or heuristic is covered
automatically. Each combination is run on a small blocksworld task and the
resulting plan is replayed to check that it actually reaches the goal.
"""

import pytest

from pyperplan import grounding
from pyperplan.pddl.parser import Parser
from pyperplan.planner import HEURISTICS, SEARCHES
from pyperplan.search import minisat

from .heuristic_test_instances import blocks_dom

# Searches that do not take a heuristic (mirrors pyperplan/__main__.py).
BLIND_SEARCHES = {"bfs", "ids", "sat"}

# A tiny task (plan: pick up A, stack it on B) that is fast for every search,
# including the SAT planner.
blocks_problem_tiny = """\
(define (problem BLOCKS-2-0)
(:domain BLOCKS)
(:objects A B - block)
(:INIT (CLEAR A) (CLEAR B) (ONTABLE A) (ONTABLE B) (HANDEMPTY))
(:goal (AND (ON A B)))
)
"""


@pytest.fixture
def task():
    parser = Parser("")
    parser.dom_input = blocks_dom
    parser.prob_input = blocks_problem_tiny
    domain = parser.parse_domain(read_from_file=False)
    problem = parser.parse_problem(domain, read_from_file=False)
    return grounding.ground(problem)


def assert_valid_plan(task, plan):
    """Assert that ``plan`` is applicable in ``task`` and reaches the goal."""
    assert plan is not None, "no plan found"
    state = task.initial_state
    for op in plan:
        assert op.applicable(state), f"operator {op.name} not applicable"
        state = op.apply(state)
    assert task.goal_reached(state), "plan does not reach the goal"


@pytest.mark.parametrize("heuristic_name", sorted(HEURISTICS))
def test_heuristic_finds_plan(task, heuristic_name):
    heuristic = HEURISTICS[heuristic_name](task)
    plan = SEARCHES["astar"](task, heuristic)
    assert_valid_plan(task, plan)


@pytest.mark.parametrize("search_name", sorted(SEARCHES))
def test_search_finds_plan(task, search_name):
    if search_name == "sat" and not minisat.minisat_available():
        pytest.skip("minisat missing")
    search = SEARCHES[search_name]
    if search_name in BLIND_SEARCHES:
        plan = search(task)
    else:
        plan = search(task, HEURISTICS["hff"](task))
    assert_valid_plan(task, plan)


def teardown_module(module):
    # The SAT planner writes these files to the working directory.
    from pyperplan import tools

    for filename in (minisat.INPUT, minisat.OUTPUT):
        tools.remove(filename)
