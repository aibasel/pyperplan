#!/usr/bin/python3
from pddl.parser import *
from pddl.lisp_parser import parse_lisp_iterator
from pddl.errors import BraceError, ParseError

from py.test import raises

## helper functions


def varListTest(varList):
    assert  [k.name for k in varList] == ['?x', '?y', '?z']
    assert  len([k for k in varList if k.typed]) == 3
    assert  [k.types[0] for k in varList] == ['block', 'foo', 'block']


def keywordListTest(keyList):
    assert  [k.name for k in keyList] == ['name', 'parameters', 'foo']


## the tests


def test_parseKeywordSimple():
    test = ['(:parameters )']
    iter = parse_lisp_iterator(test)
    key = parse_keyword(next(iter))
    assert key.name == 'parameters'


def test_parseKeywordComplex():
    test = [' ( :name)']
    iter = parse_lisp_iterator(test)
    key = parse_keyword(next(iter))
    assert key.name == 'name'


def test_parseKeywordList():
    test = ['(:name :parameters :foo )']
    iter = parse_lisp_iterator(test)
    keys = parse_keyword_list(iter)
    assert iter.empty()
    keywordListTest(keys)


def test_parseRequirements():
    test = ['(:requirements :name :parameters :foo )']
    iter = parse_lisp_iterator(test)
    req = parse_requirements_stmt(iter)
    assert iter.empty()
    keywordListTest(req.keywords)


def test_parseRequirements2():
    test = ['(:predicates :name :parameters :foo )']
    iter = parse_lisp_iterator(test)
    with raises(ValueError):
        parse_requirements_stmt(iter)


def test_parseVariableNoTyping():
    test = [' ( ?x)']
    iter = parse_lisp_iterator(test)
    key = parse_variable(next(iter))
    assert key.name == '?x'
    assert key.typed == False
    assert key.types == None


def test_parseVariableTyping():
    test = [' ( ?x - block)']
    iter = parse_lisp_iterator(test)
    vlist = parse_typed_var_list(iter)
    assert len(vlist) == 1
    assert vlist[0].name == '?x'
    assert vlist[0].typed == True
    assert vlist[0].types[0] == 'block'


def test_parseVariableList():
    test = [' ( ?x - block ?y - foo ?z - block  )']
    iter = parse_lisp_iterator(test)
    key = parse_typed_var_list(iter)
    varListTest(key)


def test_parseParameters():
    test = ['(:parameters ( ?x - block ?y - foo ?z - block  ))']
    iter = parse_lisp_iterator(test)
    key = parse_parameters(iter)
    varListTest(key)


def test_parseParameters2():
    test = ['(:predicates ( ?x - block ?y - foo ?z - block  ))']
    iter = parse_lisp_iterator(test)
    with raises(ValueError):
        parse_parameters(iter)


def test_parseTypes():
    test = ['(:types block plane key)']
    iter = parse_lisp_iterator(test)
    tlist = parse_types_stmt(iter)
    assert [t.name for t in tlist] == ['block', 'plane', 'key']


def test_parseTypesFail():
    test = ['(:types :block plane key)']
    iter = parse_lisp_iterator(test)
    with raises(ValueError):
        parse_types_stmt(iter)


def test_parseTypesFail2():
    test = ['(:predicates :block plane key)']
    iter = parse_lisp_iterator(test)
    with raises(ValueError):
        parse_types_stmt(iter)


def test_parseDomainStatement():
    test = ['(domain supertest-23-v0)']
    iter = parse_lisp_iterator(test)
    dom = parse_domain_stmt(iter)
    assert dom.name == 'supertest-23-v0'


def test_parseDomainStatementFail():
    test = ['(domaiin supertest-23-v0)']
    iter = parse_lisp_iterator(test)
    with raises(ValueError):
        parse_domain_stmt(iter)


def test_parsePredicate():
    test = ['(on ?x ?y)']
    iter = parse_lisp_iterator(test)
    pred = parse_predicate(iter)
    assert pred.name == 'on'
    assert [x.name for x in pred.parameters] == ['?x', '?y']


def test_parsePredicateMixed():
    test = ['(on ?x - block ?y)']
    iter = parse_lisp_iterator(test)
    pred = parse_predicate(iter)
    assert pred.name == 'on'
    assert [x.name for x in pred.parameters] == ['?x', '?y']
    assert [x.types[0] for x in pred.parameters
            if x.types != None] == ['block']


def test_parsePredicateList():
    test = ['((on ?x - block ?y) (put ?x ?z) (true))']
    iter = parse_lisp_iterator(test)
    predlist = parse_predicate_list(iter)
    assert [x.name for x in predlist] == ['on', 'put', 'true']


def test_parseFormula():
    test = ['(and (on ?x table) (true) (free ?x))']
    iter = parse_lisp_iterator(test)
    print(iter)
    formula = parse_formula(iter)
    assert formula.key == 'and'
    assert [c.key for c in formula.children] == ['on', 'true', 'free']
    assert [c.key.name for c in formula.children[0].children
            if c.type == TypeVariable] == ['?x']
    assert [c.key for c in formula.children[0].children
            if c.type == TypeConstant] == ['table']
    assert [c.key.name for c in formula.children[2].children
            if c.type == TypeVariable] == ['?x']
    assert [c for c in formula.children[1].children] == []


def test_parseFormulaFail():
    test = ['(and (on ?x table) (:true) (free ?x))']
    iter = parse_lisp_iterator(test)
    with raises(ValueError):
        parse_formula(iter)


def test_parseFormulaLispFail2():
    test = ['(and (on ?x table) (true) (free( ?x))']
    with raises(ParseError):
        iter = parse_lisp_iterator(test)


def test_parse_variable():
    test = ['(x)']
    iter = parse_lisp_iterator(test)
    with raises(ValueError):
        parse_variable(next(iter))


def test_lisp_parser_start_brace():
    test = ['test string)']
    with raises(ParseError):
        iter = parse_lisp_iterator(test)


def test_parse_keyword_raise():
    test = ['(?test)']
    iter = parse_lisp_iterator(test)
    with raises(ValueError):
        parse_keyword(next(iter))


def test_parse_objects_stmt_fail():
    test = ['(:predicates blubb blubb)']
    iter = parse_lisp_iterator(test)
    with raises(ValueError):
        parse_objects_stmt(iter)


def test_parse_constants_stmt_fail():
    test = ['(:predicates blubb blubb)']
    iter = parse_lisp_iterator(test)
    with raises(ValueError):
        parse_constants_stmt(iter)


def test_parse_problem_domain_stmt_fail():
    test = ['(:predicates blubb blubb)']
    iter = parse_lisp_iterator(test)
    with raises(ValueError):
        parse_problem_domain_stmt(iter)


def test_parse_precondition_stmt_fail():
    test = ['(:predicates blubb blubb)']
    iter = parse_lisp_iterator(test)
    with raises(ValueError):
        parse_precondition_stmt(iter)


def test_parse_effect_stmt_fail():
    test = ['(:predicates blubb blubb)']
    iter = parse_lisp_iterator(test)
    with raises(ValueError):
        parse_effect_stmt(iter)


def test_parse_action_stmt_fail():
    test = ['(:predicates blubb blubb)']
    iter = parse_lisp_iterator(test)
    with raises(ValueError):
        parse_action_stmt(iter)


def test_parse_predicates_stmt_fail():
    test = ['(:actions blubb blubb)']
    iter = parse_lisp_iterator(test)
    with raises(ValueError):
        parse_predicates_stmt(iter)


def test_parse_domain_def_fail():
    test = ['(definiere (domain BLOCKS))']
    iter = parse_lisp_iterator(test)
    with raises(ValueError):
        parse_domain_def(iter)


def test_parse_problem_def_fail():
    test = ['(definiere problem)']
    iter = parse_lisp_iterator(test)
    with raises(ValueError):
        parse_problem_def(iter)


def test_parse_problem_name_fail():
    test = ['(domain test)']
    iter = parse_lisp_iterator(test)
    with raises(ValueError):
        parse_problem_name(iter)


def test_parse_init_stmt_fail():
    test = ['(:goal ssdfsdf)']
    iter = parse_lisp_iterator(test)
    with raises(ValueError):
        parse_init_stmt(iter)


def test_parse_goal_stmt_fail():
    test = ['(:init ssdfsdf)']
    iter = parse_lisp_iterator(test)
    with raises(ValueError):
        parse_goal_stmt(iter)
