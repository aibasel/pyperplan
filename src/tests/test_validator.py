"""
Tests VAL. Tests are skipped if "validate" is not found on the system path.
"""

import os

import py

from pyperplan import validate_solution, validator_available
import tools


DOMAIN_FILE = 'DOMAIN.TEST'
PROBLEM_FILE = 'PROBLEM.TEST'
CORRECT_SOLN_FILE = 'CORRECT.SOLN.TEST'
FALSE_SOLN_FILE = 'FALSE.SOLN.TEST'


DOMAIN = """\
(define (domain gripper-strips)
   (:predicates (room ?r)
        (ball ?b)
        (gripper ?g)
        (at-robby ?r)
        (at ?b ?r)
        (free ?g)
        (carry ?o ?g))

   (:action move
       :parameters  (?from ?to)
       :precondition (and  (room ?from) (room ?to) (at-robby ?from))
       :effect (and  (at-robby ?to)
             (not (at-robby ?from))))

   (:action pick
       :parameters (?obj ?room ?gripper)
       :precondition  (and  (ball ?obj) (room ?room) (gripper ?gripper)
                (at ?obj ?room) (at-robby ?room) (free ?gripper))
       :effect (and (carry ?obj ?gripper)
            (not (at ?obj ?room))
            (not (free ?gripper))))

   (:action drop
       :parameters  (?obj  ?room ?gripper)
       :precondition  (and  (ball ?obj) (room ?room) (gripper ?gripper)
                (carry ?obj ?gripper) (at-robby ?room))
       :effect (and (at ?obj ?room)
            (free ?gripper)
            (not (carry ?obj ?gripper)))))
"""


PROBLEM = """\
(define (problem strips-gripper-x-1)
   (:domain gripper-strips)
   (:objects rooma roomb ball4 ball3 ball2 ball1 left right)
   (:init (room rooma)
          (room roomb)
          (ball ball4)
          (ball ball3)
          (ball ball2)
          (ball ball1)
          (at-robby rooma)
          (free left)
          (free right)
          (at ball4 rooma)
          (at ball3 rooma)
          (at ball2 rooma)
          (at ball1 rooma)
          (gripper left)
          (gripper right))
   (:goal (and (at ball4 roomb)
               (at ball3 roomb)
               (at ball2 roomb)
               (at ball1 roomb))))
"""


CORRECT_SOLN = """\
(pick ball1 rooma right)
(pick ball2 rooma left)
(move rooma roomb)
(drop ball1 roomb right)
(drop ball2 roomb left)
(move roomb rooma)
(pick ball3 rooma right)
(pick ball4 rooma left)
(move rooma roomb)
(drop ball3 roomb right)
(drop ball4 roomb left)
"""


FALSE_SOLN = """\
(pick ball1 rooma right)
(pick ball2 rooma left)
(move rooma roomb)
(drop ball1 roomb right)
(drop ball2 roomb left)
"""


def setup_module(module):
    """setup up any state specific to the execution of the given module."""
    for filename, content in [(DOMAIN_FILE, DOMAIN), (PROBLEM_FILE, PROBLEM),
                              (CORRECT_SOLN_FILE, CORRECT_SOLN),
                              (FALSE_SOLN_FILE, FALSE_SOLN)]:
        with open(filename, 'w') as f:
            f.write(content)


def test_validate_correct_plan():
    if not validator_available():
        py.test.skip('validate missing')
    assert validate_solution(DOMAIN_FILE, PROBLEM_FILE, CORRECT_SOLN_FILE)


def test_validate_false_plan():
    if not validator_available():
        py.test.skip('validate missing')
    assert not validate_solution(DOMAIN_FILE, PROBLEM_FILE, FALSE_SOLN_FILE)


def teardown_module(module):
    """
    teardown any state that was previously setup with a setup_module method.
    """
    for filename in [DOMAIN_FILE, PROBLEM_FILE, CORRECT_SOLN_FILE,
                     FALSE_SOLN_FILE]:
        tools.remove(filename)
