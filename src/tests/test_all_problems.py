"""
Tests for parsing and grounding all problems
"""

import os
import sys
from glob import glob

import py.test

import pyperplan as planner
from search import breadth_first_search


benchmarks = os.path.abspath(os.path.join(os.path.abspath(__file__),
                                          '../../../benchmarks'))

# Collect problem files
problems = sorted(glob(os.path.join(benchmarks, '*', 'task*.pddl')))
first_problems = [prob for prob in problems if 'task01' in prob]


def check_equal(result, expected):
    assert expected == result


def check_not_none(result):
    assert result is not None


def parse_problem(problem_file, domain_file=None):
    if domain_file is None:
        domain_file = planner.find_domain(problem_file)
    print('Parsing', problem_file)
    problem = planner._parse(domain_file, problem_file)
    return problem


def ground_problem(problem_file):
    problem = parse_problem(problem_file)
    print('Grounding', problem.name)
    task = planner._ground(problem)
    assert task is not None
    return task


def run_planner(problem_file):
    domain_file = planner.find_domain(problem_file)
    print('Searching solution for', domain_file, problem_file)
    assert planner.search_plan(domain_file, problem_file, breadth_first_search,
                               None) is not None


def test_ground_problems():
    for problem_file in first_problems:
        yield py.test.mark.slow(ground_problem), problem_file


def test_solve_smallest_problems():
    """
    Solves the first instance of each domain
    """
    for prob in first_problems:
        yield py.test.mark.slow(run_planner), prob
