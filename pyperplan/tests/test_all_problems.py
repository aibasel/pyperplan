"""
Tests for parsing and grounding all problems
"""

from glob import glob
import os

import pytest

from pyperplan import planner
from pyperplan.search import breadth_first_search


benchmarks = os.path.abspath(
    os.path.join(os.path.abspath(__file__), "../../../benchmarks")
)

# Collect problem files
problems = sorted(glob(os.path.join(benchmarks, "*", "task*.pddl")))
first_problems = [prob for prob in problems if "task01" in prob]


def parse_problem(problem_file, domain_file=None):
    if domain_file is None:
        domain_file = planner.find_domain(problem_file)
    print("Parsing", problem_file)
    problem = planner._parse(domain_file, problem_file)
    return problem


def ground_problem(problem_file):
    problem = parse_problem(problem_file)
    print("Grounding", problem.name)
    task = planner._ground(problem)
    assert task is not None
    return task


def run_planner(problem_file):
    domain_file = planner.find_domain(problem_file)
    print("Searching solution for", domain_file, problem_file)
    assert (
        planner.search_plan(domain_file, problem_file, breadth_first_search, None)
        is not None
    )


@pytest.mark.slow
@pytest.mark.parametrize("problem", first_problems)
def test_ground_problems(problem):
    ground_problem(problem)


@pytest.mark.slow
@pytest.mark.parametrize("problem", first_problems)
def test_solve_smallest_problems(problem):
    """
    Solves the first instance of each domain
    """
    run_planner(problem)
