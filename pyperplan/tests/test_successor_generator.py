"""
Tests for the successor_generator.py module
"""

import random

import pytest

from pyperplan.successor_generator import (
    NaiveSuccessorGenerator,
    SuccessorGenerator,
    create_successor_generator,
)
from pyperplan.task import Operator


def reference_applicable(operators, state):
    """The naive applicability check the successor generator should match."""
    return [op for op in operators if op.applicable(state)]


op1 = Operator("op1", {"a"}, {"b"}, set())
op2 = Operator("op2", {"a", "b"}, {"c"}, set())
op3 = Operator("op3", {"b"}, {"a"}, set())
op4 = Operator("op4", set(), {"a"}, set())  # always applicable
operators = [op1, op2, op3, op4]


# Run the behavioral tests against both successor generators.
@pytest.fixture(params=["naive", "tree"])
def make_generator(request):
    def factory(ops):
        return create_successor_generator(request.param, ops)

    return factory


def test_no_operators(make_generator):
    gen = make_generator([])
    assert gen.get_applicable_operators(frozenset()) == []


def test_operator_without_preconditions_always_applies(make_generator):
    gen = make_generator(operators)
    assert gen.get_applicable_operators(frozenset()) == [op4]


def test_single_precondition(make_generator):
    gen = make_generator(operators)
    assert set(gen.get_applicable_operators(frozenset(["a"]))) == {op1, op4}


def test_multiple_preconditions(make_generator):
    gen = make_generator(operators)
    assert set(gen.get_applicable_operators(frozenset(["a", "b"]))) == {
        op1,
        op2,
        op3,
        op4,
    }


def test_naive_preserves_operator_order():
    # Only the naive generator promises to keep the original operator order; the
    # tree generator returns operators in its (deterministic) traversal order.
    gen = NaiveSuccessorGenerator(operators)
    assert gen.get_applicable_operators(frozenset(["a", "b"])) == [op1, op2, op3, op4]


def test_factory_returns_requested_kind():
    assert isinstance(create_successor_generator("naive", []), NaiveSuccessorGenerator)
    assert isinstance(create_successor_generator("tree", []), SuccessorGenerator)


def test_generators_match_on_random_tasks(make_generator):
    rng = random.Random(2026)
    facts = [f"f{i}" for i in range(12)]
    random_operators = []
    for i in range(60):
        preconditions = rng.sample(facts, rng.randint(0, 4))
        random_operators.append(Operator(f"op{i}", preconditions, {"f0"}, set()))
    gen = make_generator(random_operators)
    for _ in range(200):
        state = frozenset(rng.sample(facts, rng.randint(0, len(facts))))
        # Both generators must report the same set of applicable operators; only
        # the naive one guarantees the original order.
        assert set(gen.get_applicable_operators(state)) == set(
            reference_applicable(random_operators, state)
        )
