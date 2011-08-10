from pddl.parser import Parser, parse_domain_def, parse_problem_def
import pddl.tree_visitor as pddl_tree_visitor
from pddl.tree_visitor import SemanticError
from pddl.lisp_parser import parse_lisp_iterator

from py.test import raises
import itertools


_domain_input = """
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; 4 Op-blocks world
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (domain BLOCKS)
  (:requirements :strips :typing)
  (:types block)
  (:predicates (on ?x - block ?y - block)
               (ontable ?x - block)
               (clear ?x - block)
               (handempty)
               (holding ?x - block)
               )
  (:constants horst block1 block2 - block)

  (:action pick-up
             :parameters (?x - block)
             :precondition (and (clear ?x) (ontable ?x) (handempty))
             :effect
             (and (not (ontable ?x))
                   (not (clear ?x))
                   (not (handempty))
                   (holding ?x)))

  (:action put-down
             :parameters (?x - block)
             :precondition (holding ?x)
             :effect
             (and (not (holding ?x))
                   (clear ?x)
                   (handempty)
                   (ontable ?x)))
  (:action stack
             :parameters (?x - block ?y - block)
             :precondition (and (holding ?x) (clear ?y))
             :effect
             (and (not (holding ?x))
                   (not (clear ?y))
                   (clear ?x)
                   (handempty)
                   (on ?x ?y)))
  (:action unstack
             :parameters (?x - block ?y - block)
             :precondition (and (on ?x ?y) (clear ?x) (handempty))
             :effect
             (and (holding ?x)
                   (clear ?y)
                   (not (clear ?x))
                   (not (handempty))
                   (not (on ?x ?y)))))
"""

_problem_input = """(define (problem BLOCKS-5-0)
(:domain BLOCKS)
(:objects B E A C D - block)
(:INIT (CLEAR D) (CLEAR C) (ONTABLE D) (ONTABLE A) (ON C E) (ON E B) (ON B A)
 (HANDEMPTY))
(:goal (AND (ON A E) (ON E B) (ON B D) (ON D C)))
)
"""

_parser = Parser('')

_parser.domInput = _domain_input
_parser.probInput = _problem_input

_domain = _parser.parse_domain(False)
_problem = _parser.parse_problem(_domain, False)


def test_default_pddl_visitor_domain():
    defaultVisitor = pddl_tree_visitor.PDDLVisitor()
    input = _domain_input.split('\n')
    iter = parse_lisp_iterator(input)
    domAST = parse_domain_def(iter)
    # and traverse the AST
    domAST.accept(defaultVisitor)


def test_default_pddl_visitor_problem():
    defaultVisitor = pddl_tree_visitor.PDDLVisitor()
    input = _problem_input.split('\n')
    iter = parse_lisp_iterator(input)
    probAST = parse_problem_def(iter)
    # and traverse the AST
    probAST.accept(defaultVisitor)


def test_action_set():
    assert set([a for a in _domain.actions]) == set(['pick-up', 'put-down',
                                                     'stack', 'unstack'])


def test_action_parameters():
    signatures = [a.signature for a  in _domain.actions.values()]
    #reduce(lambda x,y: x.extend(y), signatures)
    signatures = list(itertools.chain(*signatures))
    assert set([s[1][0].name for s in signatures]) == set(['block'])
    assert len(signatures) == 6


def test_action_precondition():
    preconditions = [a.precondition for a in _domain.actions.values()]
    preconditions = list(itertools.chain(*preconditions))
    all_precond = ['clear', 'ontable', 'handempty', 'holding', 'holding',
                   'clear', 'on', 'clear', 'handempty']
    all_precond_name = [p.name for p in preconditions]
    assert len(all_precond) == len(all_precond_name)
    assert set(all_precond) == set(all_precond_name)


def test_action_effects():
    effects_add = [a.effect.addlist for a in _domain.actions.values()]
    effects_del = [a.effect.dellist for a in _domain.actions.values()]
    effects_add = list(itertools.chain(*effects_add))
    effects_del = list(itertools.chain(*effects_del))
    all_effects_add = ['holding', 'clear', 'handempty', 'ontable', 'clear',
                       'handempty', 'on', 'holding', 'clear']
    all_effects_del = ['ontable', 'clear', 'handempty', 'holding', 'clear',
                       'holding', 'clear', 'handempty', 'on']
    all_effects_add_name = [e.name for e in effects_add]
    all_effects_del_name = [e.name for e in effects_del]
    assert len(all_effects_add) == len(all_effects_add_name)
    assert len(all_effects_del) == len(all_effects_del_name)
    assert set(all_effects_add) == set(all_effects_add_name)
    assert set(all_effects_del) == set(all_effects_del_name)


def test_domain_name():
    assert _domain.name == 'blocks'


def test_predicates():
    pred_names = [p for p in _domain.predicates]
    pred_sig = [p.signature for p in _domain.predicates.values()]
    pred_sig = list(itertools.chain(*pred_sig))
    pred_sig_types = [p[1][0].name for p in pred_sig]
    assert set(pred_sig_types) == set(['block'])
    assert set(pred_names) == set(['on', 'ontable', 'clear', 'handempty',
                                   'holding'])


def test_constants():
    pred_constants = [c for c in _domain.constants.values()]
    assert set([o
                for o in _domain.constants.keys()]) == set(['horst', 'block1',
                                                            'block2'])
    assert [t.name for t in _domain.constants.values()] == ['block', 'block',
                                                            'block']


def test_parent_type_undefined():
    _domain_input_2 = """
    (define (domain BLOCKS)
  (:requirements :strips :typing)
  (:types block - parent
          object)
  (:predicates (on ?x - block ?y - block)
               (ontable ?x - block)
               (clear ?x - block)
               (handempty)
               (holding ?x - block)
               )
  (:action pick-up
             :parameters (?x - block)
             :precondition (and (clear ?x) (ontable ?x) (handempty))
             :effect
             (and (not (ontable ?x))
                   (not (clear ?x))
                   (not (handempty))
                   (holding ?x)))
                   )
"""
    with raises(SemanticError):
        _parser.domInput = _domain_input_2
        _domain_2 = _parser.parse_domain(False)


def test_double_action():
    _domain_input_2 = """
    (define (domain BLOCKS)
  (:requirements :strips :typing)
  (:types block
          object)
  (:predicates (on ?x - block ?y - block)
               (ontable ?x - block)
               (clear ?x - block)
               (handempty)
               (holding ?x - block)
               )
  (:action pick-up
             :parameters (?x - block)
             :precondition (and (clear ?x) (ontable ?x) (handempty))
             :effect
             (and (not (ontable ?x))
                   (not (clear ?x))
                   (not (handempty))
                   (holding ?x)))
 (:action pick-up
             :parameters (?x - block)
             :precondition (and (clear ?x) (ontable ?x) (handempty))
             :effect
             (and (not (ontable ?x))
                   (not (clear ?x))
                   (not (handempty))
                   (holding ?x)))
                   )
"""
    with raises(SemanticError):
        _parser.domInput = _domain_input_2
        _domain_2 = _parser.parse_domain(False)


def test_double_predicate():
    _domain_input_2 = """
    (define (domain BLOCKS)
  (:requirements :strips :typing)
  (:types block
          object)
  (:predicates (on ?x - block ?y - block)
               (on ?x - block)
               )
 (:action pick-up
             :parameters (?x - block)
             :precondition (and (clear ?x) (ontable ?x) (handempty))
             :effect
             (and (not (ontable ?x))
                   (not (clear ?x))
                   (not (handempty))
                   (holding ?x)))
                   )
"""
    with raises(SemanticError):
        _parser.domInput = _domain_input_2
        _domain_2 = _parser.parse_domain(False)


def test_unkown_type_in_predicate():
    _domain_input_2 = """
    (define (domain BLOCKS)
  (:requirements :strips :typing)
  (:types block
          object)
  (:predicates (on ?x ?y )
               (down ?x - horst)
               )
 (:action pick-up
             :parameters (?x - block)
             :precondition (and (clear ?x) (ontable ?x) (handempty))
             :effect
             (and (not (ontable ?x))
                   (not (clear ?x))
                   (not (handempty))
                   (holding ?x)))
                   )
"""
    with raises(SemanticError):
        _parser.domInput = _domain_input_2
        _domain_2 = _parser.parse_domain(False)


def test_precondition_predicates_singature_wrong():
    _domain_input_2 = """
    (define (domain BLOCKS)
  (:requirements :strips :typing)
  (:types block object)
  (:predicates (on ?x - block ?y - block ) )
 (:action pick-up
             :parameters (?x - block)
             :precondition (and (on ?x) )
             :effect
             (and (not (ontable ?x))
                   (not (clear ?x))
                   (not (handempty))
                   (holding ?x)))
                   )
"""
    with raises(SemanticError):
        _parser.domInput = _domain_input_2
        _domain_2 = _parser.parse_domain(False)


def test_precondition_predicates_not_defined():
    _domain_input_2 = """
    (define (domain BLOCKS)
  (:requirements :strips :typing)
  (:types block object)
  (:predicates (on ?x - block ?y - block ) )
 (:action pick-up
             :parameters (?x - block)
             :precondition (and (off ?x) )
             :effect
             (and (not (ontable ?x))
                   (not (clear ?x))
                   (not (handempty))
                   (holding ?x)))
                   )
"""
    with raises(SemanticError):
        _parser.domInput = _domain_input_2
        _domain_2 = _parser.parse_domain(False)


def test_precondition_not_cnf():
    _domain_input_2 = """
    (define (domain BLOCKS)
  (:requirements :strips :typing)
  (:types block object)
  (:predicates (on ?x - block ?y - block ) )
 (:action pick-up
             :parameters (?x - block)
             :precondition (or (on ?x ?y) )
             :effect
             (and (not (ontable ?x))
                   (not (clear ?x))
                   (not (handempty))
                   (holding ?x)))
                   )
"""
    with raises(SemanticError):
        _parser.domInput = _domain_input_2
        _domain_2 = _parser.parse_domain(False)


def test_effect_several_children_of_not():
    _domain_input_2 = """
    (define (domain BLOCKS)
  (:requirements :strips :typing)
  (:types block object)
  (:predicates (on ?x - block ?y - block ) )
 (:action pick-up
             :parameters (?x - block)
             :precondition (and (on ?x ?y) )
             :effect
             (and (not (ontable ?x) (ontable ?x))
                   (not (clear ?x))
                   (not (handempty))
                   (holding ?x)))
                   )
"""
    with raises(SemanticError):
        _parser.domInput = _domain_input_2
        _domain_2 = _parser.parse_domain(False)


def test_effect_unkown_predicate():
    _domain_input_2 = """
    (define (domain BLOCKS)
  (:requirements :strips :typing)
  (:types block object)
  (:predicates (on ?x - block ?y - block ) )
 (:action pick-up
             :parameters (?x - block)
             :precondition (and (on ?x ?y) )
             :effect
             (and (not (ontable ?x) )
                   (not (clear ?x))
                   (not (handempty))
                   (holding ?x)))
                   )
"""
    with raises(SemanticError):
        _parser.domInput = _domain_input_2
        _domain_2 = _parser.parse_domain(False)


def test_effect_predicates_singature_wrong():
    _domain_input_2 = """
    (define (domain BLOCKS)
  (:requirements :strips :typing)
  (:types block object)
  (:predicates (on ?x - block ?y - block ) )
 (:action pick-up
             :parameters (?x - block)
             :precondition (and (on ?x ?y) )
             :effect
             (and (not (on ?x) )
                   (not (clear ?x))
                   (not (handempty))
                   (holding ?x)))
                   )
"""

    with raises(SemanticError):
        _parser.domInput = _domain_input_2
        _domain_2 = _parser.parse_domain(False)


def test_effect_or():
    _domain_input_2 = """
    (define (domain BLOCKS)
  (:requirements :strips :typing)
  (:types block object)
  (:predicates (on ?x - block ?y - block ) )
 (:action pick-up
             :parameters (?x - block)
             :precondition (and (on ?x ?y) )
             :effect
             (or (not (on ?x ?y) )
                   ))
                   )
"""

    with raises(SemanticError):
        _parser.domInput = _domain_input_2
        _domain_2 = _parser.parse_domain(False)


def test_constants_unkown_type():
    _domain_input_2 = """
    (define (domain BLOCKS)
  (:requirements :strips :typing)
  (:types block object)
  (:constants horst block1 block2 - blocks)
  (:predicates (on ?x - block ?y - block ) )
 (:action pick-up
             :parameters (?x - block)
             :precondition (and (on ?x ?y) )
             :effect
             (and (not (on ?x ?y) )
                   ))
                   )
"""

    with raises(SemanticError):
        _parser.domInput = _domain_input_2
        _domain_2 = _parser.parse_domain(False)


def test_constants_multiple():
    _domain_input_2 = """
    (define (domain BLOCKS)
  (:requirements :strips :typing)
  (:types block object)
  (:constants horst horst block2 - block)
  (:predicates (on ?x - block ?y - block ) )
 (:action pick-up
             :parameters (?x - block)
             :precondition (and (on ?x ?y) )
             :effect
             (and (not (on ?x ?y) )
                   ))
                   )
"""
    with raises(SemanticError):
        _parser.domInput = _domain_input_2
        _domain_2 = _parser.parse_domain(False)


def test_problem_name_collision():
    _problem_input_2 = """(define (problem BLOCKS-5-0)
    (:domain huibuh)
    (:objects B E A C D - block)
    (:INIT (CLEAR D) (CLEAR C) (ONTABLE D) (ONTABLE A) (ON C E) (ON E B)
     (ON B A) (HANDEMPTY))
    (:goal (AND (ON A E) (ON E B) (ON B D) (ON D C)))
    )
    """

    with raises(SemanticError):
        _parser.probInput = _problem_input_2
        _problem = _parser.parse_problem(_domain, False)


def test_problem_object_unkown_type():
    _problem_input_2 = """(define (problem BLOCKS-5-0)
    (:domain BLOCKS)
    (:objects B - unkownType E A C D)
    (:INIT (CLEAR D) (CLEAR C) (ONTABLE D) (ONTABLE A) (ON C E) (ON E B)
     (ON B A) (HANDEMPTY))
    (:goal (AND (ON A E) (ON E B) (ON B D) (ON D C)))
    )
    """

    with raises(SemanticError):
        _parser.probInput = _problem_input_2
        _problem = _parser.parse_problem(_domain, False)


def test_problem_object_multiple():
    _problem_input_2 = """(define (problem BLOCKS-5-0)
    (:domain BLOCKS)
    (:objects B B E A C D)
    (:INIT (CLEAR D) (CLEAR C) (ONTABLE D) (ONTABLE A) (ON C E) (ON E B)
     (ON B A) (HANDEMPTY))
    (:goal (AND (ON A E) (ON E B) (ON B D) (ON D C)))
    )
    """
    with raises(SemanticError):
        _parser.probInput = _problem_input_2
        _problem = _parser.parse_problem(_domain, False)


def test_problem_object_multiple_2():
    _problem_input_2 = """(define (problem BLOCKS-5-0)
    (:domain BLOCKS)
    (:objects B -parent B - parent2 E A C D - object)
    (:INIT (CLEAR D) (CLEAR C) (ONTABLE D) (ONTABLE A) (ON C E) (ON E B)
     (ON B A) (HANDEMPTY))
    (:goal (AND (ON A E) (ON E B) (ON B D) (ON D C)))
    )
    """
    with raises(SemanticError):
        _parser.probInput = _problem_input_2
        _problem = _parser.parse_problem(_domain, False)


def test_problem_goal_unknown_predicate():
    _problem_input_2 = """(define (problem BLOCKS-5-0)
    (:domain BLOCKS)
    (:objects B E A C D)
    (:INIT (CLEAR D) (CLEAR C) (ONTABLE D) (ONTABLE A) (ON C E) (ON E B)
     (ON B A) (HANDEMPTY))
    (:goal (AND (OFF A E) (ON E B) (ON B D) (ON D C)))
    )
    """
    with raises(SemanticError):
        _parser.probInput = _problem_input_2
        _problem = _parser.parse_problem(_domain, False)


def test_problem_goal_predicate_signature():
    _problem_input_2 = """(define (problem BLOCKS-5-0)
    (:domain BLOCKS)
    (:objects B E A C D)
    (:INIT (CLEAR D) (CLEAR C) (ONTABLE D) (ONTABLE A) (ON C E) (ON E B)
     (ON B A) (HANDEMPTY))
    (:goal (AND (ON A E D) (ON E B) (ON B D) (ON D C)))
    )
    """
    with raises(SemanticError):
        _parser.probInput = _problem_input_2
        _problem = _parser.parse_problem(_domain, False)


def test_problem_goal_cnf():
    _problem_input_2 = """(define (problem BLOCKS-5-0)
    (:domain BLOCKS)
    (:objects B E A C D)
    (:INIT (CLEAR D) (CLEAR C) (ONTABLE D) (ONTABLE A) (ON C E) (ON E B)
     (ON B A) (HANDEMPTY))
    (:goal (OR (ON A E) (ON E B) (ON B D) (ON D C)))
    )
    """
    with raises(SemanticError):
        _parser.probInput = _problem_input_2
        _problem = _parser.parse_problem(_domain, False)


def test_problem_goal_single_predicate():
    _problem_input_2 = """(define (problem BLOCKS-5-0)
    (:domain BLOCKS)
    (:objects B E A C D)
    (:INIT (CLEAR D) (CLEAR C) (ONTABLE D) (ONTABLE A) (ON C E) (ON E B)
     (ON B A) (HANDEMPTY))
    (:goal (ON A E))
    )
    """
    _parser.probInput = _problem_input_2
    _problem = _parser.parse_problem(_domain, False)
