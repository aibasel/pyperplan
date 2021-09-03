from collections import defaultdict
import logging

from . import minisat


# Max number of steps in a plan
HORIZON = 1000


def _formula_str(formula, sep="&"):
    """Returns a representation of 'formula' for prettyprinting"""
    next_sep = "|" if sep == "&" else "&"
    items = [
        item if (type(item) == str) else _formula_str(item, next_sep)
        for item in formula
    ]
    return "({})".format(f" {sep} ".join(items))


def index_fact(fact, index, negated=False):
    """
    Returns a representation of 'fact' containing the step number and a
    leading 'not-' if the fact is negated
    """
    name = str(fact)
    if negated:
        name = "not-" + name
    return "%s-%d" % (name, index)


def makes_true(operator, fact):
    """Returns true iff 'operator' makes 'fact' true"""
    return fact in operator.add_effects


def makes_false(operator, fact):
    """Returns true iff 'operator' makes 'fact' false"""
    return fact in operator.del_effects


def get_formula_for_fact(op, fact, index):
    """Returns a formula for 'fact' in the step 'index'"""
    if makes_true(op, fact):
        return [index_fact(fact, index + 1)]
    if not makes_false(op, fact):
        # a'<->a == (~a' v a) & (~a v a')
        return ["<->".join([index_fact(fact, index + 1), index_fact(fact, index)])]
    return [index_fact(fact, index + 1, negated=True)]


def get_formula_for_operator(facts, op, index):
    """Returns a formula for the operator 'op' in the step 'index'"""
    precondition = list(sorted(op.preconditions))
    formula = [index_fact(fact, index) for fact in precondition]
    for fact in facts:
        formula += get_formula_for_fact(op, fact, index)
    return formula


def get_plan_formula(task, horizon):
    """Returns a formula for a given task and number of steps"""
    init_true = list(sorted(task.initial_state))
    init_false = list(sorted(task.facts - task.initial_state))
    pos = [index_fact(fact, 0) for fact in init_true]
    neg = [index_fact(fact, 0, negated=True) for fact in init_false]
    formula = list(pos) + list(neg)
    for length in range(horizon):
        disjunction = []
        for op in task.operators:
            disjunction.append(get_formula_for_operator(task.facts, op, length))
        formula.append(disjunction)
    goal = [index_fact(fact, horizon) for fact in list(sorted(task.goals))]
    formula.extend(goal)
    return formula


def _extract_plan(operators, valuation):
    """Turns a valuation into a list of operators.

    valuation is a list of facts (e.g. ['a-0', 'not-a-1', 'a-2'])
    """
    logging.debug("Length of valuation: {}".format(len(valuation)))

    # Divide facts into positive and negative ones
    pos_facts = defaultdict(set)
    neg_facts = defaultdict(set)
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
        current_state = pos_facts[step - 1]
        next_state = pos_facts[step]
        actual_op = None
        for op in operators:
            if op.applicable(current_state) and op.apply(current_state) == next_state:
                actual_op = op
                break
        assert actual_op, f"Valuation: {valuation}, Ops: {operators}"
        plan.append(actual_op)
    return plan


def sat_solve(task, max_steps=HORIZON):
    """Solves a planning task with a sat-solver.

    Returns a list of operators or None if no valid plan could be found
    with <= 'HORIZON' steps
    """
    logging.info(f"Maximum number of plan steps: {max_steps}")
    for horizon in range(max_steps + 1):
        logging.info(f"Horizon: {horizon}")
        valuation = minisat.solve(get_plan_formula(task, horizon))
        if valuation:
            plan = _extract_plan(task.operators, valuation)
            return plan
    logging.info("Try increasing the maximum number of steps")
    return None
