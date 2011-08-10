#!/usr/bin/python3
from pddl.parser import *
from pddl.lisp_parser import parse_lisp_iterator
from pddl.errors import BraceError, ParseError

from py.test import raises

### helper functions


def objectsTest(objects):
    assert [o.name for o in objects] == ['apn1', 'apt2', 'apt1', 'pos2',
                                         'pos1', 'cit2', 'cit1', 'tru2',
                                         'tru1', 'obj23', 'obj22', 'obj21',
                                         'obj13', 'obj12', 'obj11']
    typeSet = set([o.typeName for o in objects])
    assert  typeSet == set(['airplane', 'airport', 'location', 'city', 'truck',
                            'package'])


### test cases

def test_parseAction():
    test = ["""
    (:action pick-up
             :parameters (?x - block)
             :precondition (and (clear ?x) (ontable ?x) (handempty))
             :effect
             (and (not (ontable ?x))
                   (not (clear ?x))
                   (not (handempty))
                   (holding ?x)))
    """]
    iter = parse_lisp_iterator(test)
    action = parse_action_stmt(iter)
    assert action.name == "pick-up"
    assert action.parameters[0].name == "?x"
    assert action.parameters[0].types[0] == "block"
    pre = action.precond.formula
    assert pre.key == 'and'
    assert [c.key for c in pre.children] == ['clear', 'ontable', 'handempty']
    assert pre.children[0].children[0].key.name == '?x'
    assert pre.children[1].children[0].key.name == '?x'
    assert pre.children[2].children == []
    eff = action.effect.formula
    assert eff.key == 'and'
    assert [c.key for c in eff.children] == ['not', 'not', 'not', 'holding']
    assert eff.children[0].children[0].key == 'ontable'
    assert [c.key.name for c in eff.children[0].children[0].children] == ['?x']


def test_parsePredicates():
    test = ["""
    (:predicates (on ?x - block ?y - block)
               (ontable ?x - block)
               (clear ?x - plane)
               (handempty)
               (holding ?x - block)
               )
    """]
    iter = parse_lisp_iterator(test)
    pred = parse_predicates_stmt(iter)
    assert [p.name for p in pred.predicates] == ['on', 'ontable', 'clear',
                                                   'handempty', 'holding']
    assert [p.parameters[0].name for p in pred.predicates
            if p.parameters != []] == ['?x', '?x', '?x', '?x']
    assert [p.parameters[0].types[0] for p in pred.predicates
            if p.parameters != []] == ['block', 'block', 'plane', 'block']
    assert [p.parameters[1].types[0] for p in pred.predicates
            if len(p.parameters) > 1] == ['block']


def test_parseTypes():
    test = ["""
    (:types truck
          airplane - vehicle
          package
          vehicle - physobj
          airport
          location - place
          city
          place
          physobj - object)
    """]
    iter = parse_lisp_iterator(test)
    types = parse_types_stmt(iter)
    assert [t.name for t in types] == ['truck', 'airplane', 'package',
                                       'vehicle', 'airport', 'location',
                                       'city', 'place', 'physobj']
    assert [t.parent for t in types
            if t.parent != None] == ['vehicle', 'vehicle', 'physobj',
                                     'physobj', 'place', 'place', 'object',
                                     'object', 'object']


def test_parsePredicatesLogistics():
    test = ["""
        (:predicates  (in-city ?loc - place ?city - city)
                (at ?obj - physobj ?loc - place)
                (in ?pkg - package ?veh - vehicle))
    """]
    iter = parse_lisp_iterator(test)
    pred = parse_predicates_stmt(iter)
    assert [p.name for p in pred.predicates] == ['in-city', 'at', 'in']
    assert [p.parameters[0].name
            for p in pred.predicates
            if p.parameters != []] == ['?loc', '?obj', '?pkg']
    assert [p.parameters[0].types[0]
            for p in pred.predicates
            if p.parameters != []] == ['place', 'physobj', 'package']


def test_parseDomainDef():
    test = ["""
    (define (domain BLOCKS)
  (:requirements :strips :typing)
  (:types block)
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
    """]
    iter = parse_lisp_iterator(test)
    dom = parse_domain_def(iter)
    assert dom.name == 'blocks'
    assert [key.name
            for key in dom.requirements.keywords] == ['strips', 'typing']
    assert [t.name for t in dom.types] == ['block']
    pred = dom.predicates
    assert [p.name
            for p in pred.predicates] == ['on', 'ontable', 'clear',
                                           'handempty', 'holding']
    assert [p.parameters[0].name
            for p in pred.predicates
            if p.parameters != []] == ['?x', '?x', '?x', '?x']
    assert [p.parameters[0].types[0]
            for p in pred.predicates
            if p.parameters != []] == ['block', 'block', 'block', 'block']
    assert [p.parameters[1].types[0] for p in pred.predicates
            if len(p.parameters) > 1] == ['block']
    assert len(dom.actions) == 4
    action = dom.actions[3]
    assert action.name == 'unstack'
    assert action.parameters[0].name == '?x'
    assert action.parameters[0].types[0] == 'block'
    assert action.parameters[1].name == '?y'
    assert action.parameters[1].types[0] == 'block'
    pre = action.precond.formula
    assert pre.key == 'and'
    assert [c.key for c in pre.children] == ['on', 'clear', 'handempty']
    assert pre.children[0].children[0].key.name == '?x'
    assert pre.children[0].children[1].key.name == '?y'
    assert pre.children[1].children[0].key.name == '?x'
    assert pre.children[2].children == []
    eff = action.effect.formula
    assert eff.key == 'and'
    assert [c.key
            for c in eff.children] == ['holding', 'clear', 'not', 'not', 'not']


def test_parseDomainDef2():
    test = ["""
    (define (domain BLOCKS)
  (:requirements :strips :typing)
  (:types block)
  (:predicates (on ?x - block ?y - block)
               (ontable ?x - block)
               (clear ?x - block)
               (handempty)
               (holding ?x - block)
               )
    (:unkownKeyword lksdf)
    )
    """]
    iter = parse_lisp_iterator(test)
    with raises(ValueError):
        dom = parse_domain_def(iter)


def test_parseDomainDef():
    test = ["""
    (define (domain BLOCKS)
  (:requirements :strips :typing)
  (:types block)
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
                   (not (on ?x ?y))))
   (:unkownKeyword lksdf)
                   )
    """]
    iter = parse_lisp_iterator(test)
    with raises(ValueError):
        dom = parse_domain_def(iter)


def test_predList2():
    test = ["""
    (:predicates (at ?x - (either person aircraft) ?c - city)
             (in ?p - person ?a - aircraft)
             (fuel-level ?a - aircraft ?l - flevel)
             (next ?l1 ?l2 - flevel))
    """]
    iter = parse_lisp_iterator(test)
    pred = parse_predicates_stmt(iter)
    assert [p.name
            for p in pred.predicates] == ['at', 'in', 'fuel-level', 'next']
    assert [p.parameters[0].name for p in pred.predicates
            if p.parameters != []] == ['?x', '?p', '?a', '?l1']
    assert [p.parameters[0].types[0] for p in pred.predicates
            if p.parameters[0].types != None] == ['person', 'person',
                                                   'aircraft', 'flevel']


def test_predList3():
    test = ["""
    (:predicates (at ?x - (notEither person aircraft) ?c - city)
             (in ?p - person ?a - aircraft)
             (fuel-level ?a - aircraft ?l - flevel)
             (next ?l1 ?l2 - flevel))
    """]
    iter = parse_lisp_iterator(test)
    with raises(ValueError):
        pred = parse_predicates_stmt(iter)


def test_predList4():
    test = ["""
    (:predicates (at ?x - (either person aircraft) ?c - city)
             (in p - person a - aircraft)
             (fuel-level ?a - aircraft ?l - flevel)
             (next ?l1 ?l2 - flevel))
    """]
    iter = parse_lisp_iterator(test)
    with raises(ValueError):
        pred = parse_predicates_stmt(iter)


def test_parseObjectsStmt():
    test = ["""(:objects
      apn1 - airplane
      apt2 apt1 - airport
       pos2 pos1 - location
       cit2 cit1 - city
       tru2 tru1 - truck
       obj23 obj22 obj21 obj13 obj12 obj11 - package)"""]
    iter = parse_lisp_iterator(test)
    objects = parse_objects_stmt(iter)
    objectsTest(objects)


def test_parseInitStmt():
    test = ["""
    (:INIT (CLEAR C) (CLEAR A H) (CLEAR B) (CLEAR D) (ONTABLE C) (ONTABLE A)
     (ONTABLE B) (ONTABLE D) (HANDEMPTY))"""]
    iter = parse_lisp_iterator(test)
    init = parse_init_stmt(iter)
    assert [p.name
            for p in init.predicates] == ['clear', 'clear', 'clear', 'clear',
                                          'ontable', 'ontable', 'ontable',
                                          'ontable', 'handempty']
    assert [p.parameters
            for p in init.predicates] == [['c'], ['a', 'h'], ['b'], ['d'],
                                          ['c'], ['a'], ['b'], ['d'], []]


def test_parseGoalStmt():
    test = ["""(:goal (AND (ON D C) (ON C B) (ON B A)))"""]
    iter = parse_lisp_iterator(test)
    goal = parse_goal_stmt(iter)
    f = goal.formula
    assert f.key == 'and'
    assert [c.key for c in f.children] == ['on', 'on', 'on']
    assert [c2[0].key
            for c2 in [c1.children for c1 in f.children]] == ['d', 'c', 'b']
    assert [c2[1].key
            for c2 in [c1.children for c1 in f.children]] == ['c', 'b', 'a']


def test_parseConstants():
    test = ["""
    (:constants
                north
                south - direction
                light
                medium
                heavy - airplanetype
                seg_pp_0_60
                seg_ppdoor_0_40
                seg_tww1_0_200
                seg_twe1_0_200
                seg_tww2_0_50
                seg_tww3_0_50
                seg_tww4_0_50
                seg_rww_0_50
                seg_rwtw1_0_10
                seg_rw_0_400
                seg_rwe_0_50
                seg_twe4_0_50
                seg_rwte1_0_10
                seg_twe3_0_50
                seg_twe2_0_50
                seg_rwte2_0_10
                seg_rwtw2_0_10 - segment
                airplane_CFBEG - airplane
    )
    """]
    iter = parse_lisp_iterator(test)
    const = parse_constants_stmt(iter)
    nameList = ['north', 'south', 'light', 'medium', 'heavy']
    nameList += """seg_pp_0_60
                seg_ppdoor_0_40
                seg_tww1_0_200
                seg_twe1_0_200
                seg_tww2_0_50
                seg_tww3_0_50
                seg_tww4_0_50
                seg_rww_0_50
                seg_rwtw1_0_10
                seg_rw_0_400
                seg_rwe_0_50
                seg_twe4_0_50
                seg_rwte1_0_10
                seg_twe3_0_50
                seg_twe2_0_50
                seg_rwte2_0_10
                seg_rwtw2_0_10
                airplane_CFBEG""".split()
    nameList = [n.lower() for n in nameList]
    assert [c.name for c in const] == nameList
    ttest = [c.typeName for c in const][:5]
    assert ttest == ['direction', 'direction', 'airplanetype', 'airplanetype',
                     'airplanetype']


def test_parseProblemDef():
    test = ["""
    (define (problem logistics-4-1)
    (:domain logistics)
    (:objects
      apn1 - airplane
      apt2 apt1 - airport
      pos2 pos1 - location
      cit2 cit1 - city
      tru2 tru1 - truck
      obj23 obj22 obj21 obj13 obj12 obj11 - package)

    (:init (at apn1 apt2) (at tru1 pos1) (at obj11 pos1)
     (at obj12 pos1) (at obj13 pos1) (at tru2 pos2) (at obj21 pos2)
     (at obj22 pos2) (at obj23 pos2) (in-city pos1 cit1) (in-city apt1 cit1)
     (in-city pos2 cit2) (in-city apt2 cit2))

    (:goal (and (at obj12 apt2) (at obj13 apt1) (at obj21 apt2)
                (at obj11 pos2)))
    )
    """]
    iter = parse_lisp_iterator(test)
    prob = parse_problem_def(iter)
    assert prob.name == 'logistics-4-1'
    assert prob.domainName == 'logistics'
    objectsTest(prob.objects)
    predNames = [p.name for p in prob.init.predicates]
    assert len(predNames) == 13
    assert set(predNames) == set(['at', 'in-city'])
