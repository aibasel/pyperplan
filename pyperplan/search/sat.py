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

"""Solve a planning task by encoding it as a sequence of SAT formulas."""

import logging
from collections import defaultdict
from typing import Any

from ..task import Operator, Task
from . import minisat

# Maximum number of steps in a plan.
HORIZON = 1000


def _formula_str(formula: Any, sep: str = "&") -> str:
    """Return a representation of ``formula`` for pretty-printing."""
    next_sep = "|" if sep == "&" else "&"
    items = [
        item if isinstance(item, str) else _formula_str(item, next_sep)
        for item in formula
    ]
    return f"({f' {sep} '.join(items)})"


def index_fact(fact: str | int, index: int, negated: bool = False) -> str:
    """Return a representation of ``fact`` tagged with the step number.

    Negated facts get a leading ``not-``.
    """
    name = str(fact)
    if negated:
        name = "not-" + name
    return f"{name}-{index}"


def makes_true(operator: Operator, fact: str) -> bool:
    """Return True iff ``operator`` makes ``fact`` true."""
    return fact in operator.add_effects


def makes_false(operator: Operator, fact: str) -> bool:
    """Return True iff ``operator`` makes ``fact`` false."""
    return fact in operator.del_effects


def get_formula_for_fact(op: Operator, fact: str, index: int) -> list[str]:
    """Return a formula for ``fact`` in the step ``index``."""
    if makes_true(op, fact):
        return [index_fact(fact, index + 1)]
    if not makes_false(op, fact):
        # a'<->a == (~a' v a) & (~a v a')
        return ["<->".join([index_fact(fact, index + 1), index_fact(fact, index)])]
    return [index_fact(fact, index + 1, negated=True)]


def get_formula_for_operator(
    facts: frozenset[str], op: Operator, index: int
) -> list[str]:
    """Return a formula for the operator ``op`` in the step ``index``."""
    formula = [index_fact(fact, index) for fact in sorted(op.preconditions)]
    for fact in facts:
        formula += get_formula_for_fact(op, fact, index)
    return formula


def get_plan_formula(task: Task, horizon: int) -> list[Any]:
    """Return a formula for a given task and number of steps."""
    init_true = sorted(task.initial_state)
    init_false = sorted(task.facts - task.initial_state)
    pos = [index_fact(fact, 0) for fact in init_true]
    neg = [index_fact(fact, 0, negated=True) for fact in init_false]
    formula: list[Any] = pos + neg
    for length in range(horizon):
        disjunction = [
            get_formula_for_operator(task.facts, op, length) for op in task.operators
        ]
        formula.append(disjunction)
    goal = [index_fact(fact, horizon) for fact in sorted(task.goals)]
    formula.extend(goal)
    return formula


def _extract_plan(operators: list[Operator], valuation: list[str]) -> list[Operator]:
    """Turn a valuation into a list of operators.

    ``valuation`` is a list of facts (e.g. ['a-0', 'not-a-1', 'a-2']).
    """
    logging.debug(f"Length of valuation: {len(valuation)}")

    # Divide facts into positive and negative ones
    pos_facts: defaultdict[int, set[str]] = defaultdict(set)
    neg_facts: defaultdict[int, set[str]] = defaultdict(set)
    plan_length = -1
    for fact in valuation:
        if "<->" in fact or "AND" in fact:
            continue
        parts = fact.split("-")
        depth = int(parts[-1])
        plan_length = max(plan_length, depth)
        if fact.startswith("not-"):
            varname = "-".join(parts[1:-1])
            neg_facts[depth].add(varname)
        else:
            varname = "-".join(parts[0:-1])
            pos_facts[depth].add(varname)
    logging.debug(f"Positive facts: {pos_facts}")
    logging.debug(f"Negative facts: {neg_facts}")

    plan = []
    for step in range(1, plan_length + 1):
        current_state = frozenset(pos_facts[step - 1])
        next_state = frozenset(pos_facts[step])
        actual_op = None
        for op in operators:
            if op.applicable(current_state) and op.apply(current_state) == next_state:
                actual_op = op
                break
        assert actual_op, f"Valuation: {valuation}, Ops: {operators}"
        plan.append(actual_op)
    return plan


def sat_solve(task: Task, max_steps: int = HORIZON) -> list[Operator] | None:
    """Solve a planning task with a SAT solver.

    Returns a list of operators, or None if no valid plan could be found with at
    most ``max_steps`` steps.
    """
    logging.info(f"Maximum number of plan steps: {max_steps}")
    for horizon in range(max_steps + 1):
        logging.info(f"Horizon: {horizon}")
        valuation = minisat.solve(get_plan_formula(task, horizon))
        if valuation:
            return _extract_plan(task.operators, valuation)
    logging.info("Try increasing the maximum number of steps")
    return None
