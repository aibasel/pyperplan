"""
Tests for the successor_generator.py module
"""

import random

from pyperplan.successor_generator import SuccessorGenerator
from pyperplan.task import Operator


def reference_applicable(operators, state):
    """The naive applicability check the successor generator should match."""
    return [op for op in operators if op.applicable(state)]


op1 = Operator("op1", {"a"}, {"b"}, set())
op2 = Operator("op2", {"a", "b"}, {"c"}, set())
op3 = Operator("op3", {"b"}, {"a"}, set())
op4 = Operator("op4", set(), {"a"}, set())  # always applicable
operators = [op1, op2, op3, op4]


def test_no_operators():
    gen = SuccessorGenerator([])
    assert gen.get_applicable_operators(frozenset()) == []


def test_operator_without_preconditions_always_applies():
    gen = SuccessorGenerator(operators)
    assert gen.get_applicable_operators(frozenset()) == [op4]


def test_single_precondition():
    gen = SuccessorGenerator(operators)
    assert gen.get_applicable_operators(frozenset(["a"])) == [op1, op4]


def test_multiple_preconditions():
    gen = SuccessorGenerator(operators)
    assert gen.get_applicable_operators(frozenset(["a", "b"])) == [
        op1,
        op2,
        op3,
        op4,
    ]


def test_preserves_operator_order():
    gen = SuccessorGenerator(operators)
    assert gen.get_applicable_operators(frozenset(["b"])) == [op3, op4]


def test_matches_naive_scan_on_random_tasks():
    rng = random.Random(2026)
    facts = [f"f{i}" for i in range(12)]
    random_operators = []
    for i in range(60):
        preconditions = rng.sample(facts, rng.randint(0, 4))
        random_operators.append(Operator(f"op{i}", preconditions, {"f0"}, set()))
    gen = SuccessorGenerator(random_operators)
    for _ in range(200):
        state = frozenset(rng.sample(facts, rng.randint(0, len(facts))))
        assert gen.get_applicable_operators(state) == reference_applicable(
            random_operators, state
        )
