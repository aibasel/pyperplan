#
# This file is part of pyperplan.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#

import importlib
import logging
import os
import re
import subprocess
import sys
import time

from . import grounding, heuristics, search, tools
from .pddl.parser import Parser

SEARCHES = {
    "astar": search.astar_search,
    "wastar": search.weighted_astar_search,
    "gbfs": search.greedy_best_first_search,
    "bfs": search.breadth_first_search,
    "ehs": search.enforced_hillclimbing_search,
    "ids": search.iterative_deepening_search,
    "sat": search.sat_solve,
}


NUMBER = re.compile(r"\d+")


def get_heuristics():
    """
    Scan all Python modules in the "heuristics" directory for classes ending
    with "Heuristic".
    """
    heuristics = []
    src_dir = os.path.dirname(os.path.abspath(__file__))
    heuristics_dir = os.path.abspath(os.path.join(src_dir, "heuristics"))
    for filename in os.listdir(heuristics_dir):
        if not filename.endswith(".py"):
            continue
        name = "." + os.path.splitext(os.path.basename(filename))[0]
        module = importlib.import_module(name, package="pyperplan.heuristics")
        heuristics.extend(
            getattr(module, cls)
            for cls in dir(module)
            if cls.endswith("Heuristic")
            and cls != "Heuristic"
            and not cls.startswith("_")
        )
    return heuristics


def _get_heuristic_name(cls):
    name = cls.__name__
    assert name.endswith("Heuristic")
    return name[: -len("Heuristic")].lower()


HEURISTICS = {_get_heuristic_name(heur): heur for heur in get_heuristics()}


def validator_available():
    return tools.command_available(["validate", "-h"])


def find_domain(problem):
    """Guess the domain file that belongs to ``problem``.

    By default we use a file called "domain.pddl" in the same directory as the
    problem file. If the problem file's name contains digits, the first group of
    digits is interpreted as a number and the directory is searched for a file
    that contains both the word "domain" and that number. This matches domains
    where there is a separate domain file for each problem, e.g. the airport
    domain.

    ``problem`` is the path to a problem file. Returns the path to a domain file.
    """
    directory, name = os.path.split(problem)
    number = NUMBER.search(name).group(0)
    domain = os.path.join(directory, "domain.pddl")
    for file in os.listdir(directory):
        if "domain" in file and number in file:
            domain = os.path.join(directory, file)
            break
    if not os.path.isfile(domain):
        logging.error(f'Domain file "{domain}" can not be found')
        sys.exit(1)
    logging.info(f"Found domain {domain}")
    return domain


def _parse(domain_file, problem_file):
    parser = Parser(domain_file, problem_file)
    logging.info(f"Parsing Domain {domain_file}")
    domain = parser.parse_domain()
    logging.info(f"Parsing Problem {problem_file}")
    problem = parser.parse_problem(domain)
    logging.debug(domain)
    logging.info(f"{len(domain.predicates)} Predicates parsed")
    logging.info(f"{len(domain.actions)} Actions parsed")
    logging.info(f"{len(problem.objects)} Objects parsed")
    logging.info(f"{len(domain.constants)} Constants parsed")
    return problem


def _ground(
    problem, remove_statics_from_initial_state=True, remove_irrelevant_operators=True
):
    logging.info(f"Grounding start: {problem.name}")
    task = grounding.ground(
        problem, remove_statics_from_initial_state, remove_irrelevant_operators
    )
    logging.info(f"Grounding end: {problem.name}")
    logging.info(f"{len(task.facts)} Variables created")
    logging.info(f"{len(task.operators)} Operators created")
    return task


def _search(task, search, heuristic, use_preferred_ops=False):
    logging.info(f"Search start: {task.name}")
    if heuristic:
        if use_preferred_ops:
            solution = search(task, heuristic, use_preferred_ops)
        else:
            solution = search(task, heuristic)
    else:
        solution = search(task)
    logging.info(f"Search end: {task.name}")
    return solution


def write_solution(solution, filename):
    assert solution is not None
    with open(filename, "w") as file:
        for op in solution:
            print(op.name, file=file)


def search_plan(
    domain_file, problem_file, search, heuristic_class, use_preferred_ops=False
):
    """Parse the input files into a planning task and search for a solution.

    domain_file: The path to a domain file.
    problem_file: The path to a problem file in the domain given by
        ``domain_file``.
    search: A callable that performs a search on the task's search space.
    heuristic_class: A class implementing the heuristic_base.Heuristic
        interface.

    Returns a list of actions that solve the problem, or None if no solution
    exists.
    """
    overall_start_time = time.process_time()
    problem = _parse(domain_file, problem_file)
    task = _ground(problem)
    heuristic = None
    if heuristic_class is not None:
        heuristic = heuristic_class(task)
    search_start_time = time.process_time()
    if use_preferred_ops and isinstance(heuristic, heuristics.hFFHeuristic):
        solution = _search(task, search, heuristic, use_preferred_ops=True)
    else:
        solution = _search(task, search, heuristic)
    logging.info(f"Search time: {time.process_time() - search_start_time:.2f}")
    logging.info(f"Overall time: {time.process_time() - overall_start_time:.2f}")
    return solution


def validate_solution(domain_file, problem_file, solution_file):
    if not validator_available():
        logging.info(
            "validate could not be found on the PATH so the plan can not be validated."
        )
        return

    cmd = ["validate", domain_file, problem_file, solution_file]
    exitcode = subprocess.call(cmd, stdout=subprocess.PIPE)

    if exitcode == 0:
        logging.info("Plan correct")
    else:
        logging.warning("Plan NOT correct")
    return exitcode == 0
