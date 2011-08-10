"""
Regression test for a bug where BFS could not find a plan for
parcprinter:task01.pddl
"""

optimal_plan = """\
initialize
blackfeeder-feed-letter sheet1
blackcontainer-toime-letter sheet1
blackprinter-simplex-letter sheet1 front image-1
blackcontainer-fromime-letter sheet1
endcap-move-letter sheet1
htmoverblack-move-letter sheet1
down-movetop-letter sheet1
htmovercolor-move-letter sheet1
up-movetop-letter sheet1
finisher1-stack-letter sheet1 dummy-sheet
"""
optimal_plan = [op.strip() for op in optimal_plan.splitlines()]

import os

import py

from task import Task, Operator

import pyperplan as planner
from search import breadth_first_search, searchspace

benchmarks = os.path.abspath(os.path.join(os.path.abspath(__file__),
                                          '../../../benchmarks'))

# Collect problem files
problem_file = os.path.join(benchmarks, 'parcprinter', 'task01.pddl')
domain_file = planner.find_domain(problem_file)

problem = planner._parse(domain_file, problem_file)
task = planner._ground(problem)

# Manually do the "search"
node = searchspace.make_root_node(task.initial_state)
for step, op_name in enumerate(optimal_plan, start=1):
    for op, successor_state in task.get_successor_states(node.state):
        if not op.name.strip('()') == op_name:
            continue
        node = searchspace.make_child_node(node, op, successor_state)

# Check that we reached the goal
assert len(task.goals - node.state) == 0
