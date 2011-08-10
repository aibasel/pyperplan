from pddl.parser import *

_parser = Parser('')


def test_untyped_constants():
    domain_input = """
    (define (domain regression-test)
      (:predicates (the-predicate ?v))
      (:constants x)

      (:action dummy-action
       :parameters ()
       :precondition (and)
       :effect (and)
      )
    )
    """

    problem_input = """
    (define (problem regression-test-04)
      (:domain regression-test)
      (:init (the-predicate x))
      (:goal (the-predicate x)))
    """
    _parser.domInput = domain_input
    _parser.probInput = problem_input

    domain = _parser.parse_domain(False)
    problem = _parser.parse_problem(domain, False)

    _parser.domInput = domain_input
    domain = _parser.parse_domain(False)

    assert domain.constants.keys() == {"x"}


def test_empty_actions():
    domain_input = """
    (define (domain regression-test)
    (:predicates (trivial-goal))
    )
    """
    _parser.domInput = domain_input
    domain = _parser.parse_domain(False)

    assert not domain.actions
