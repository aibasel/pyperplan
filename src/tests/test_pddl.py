from pddl.pddl import Type, Predicate, Domain, Problem


def test_type():
    test = Type("test", "parent")
    assert(str(test) == repr(test))


def test_predicate():
    test = Predicate("test", list(("a", list())))
    assert(str(test) == repr(test))


def test_domain():
    test = Domain('domain', dict(), list(), list(), dict())
    assert(str(test) == repr(test))


def test_problem():
    domain = Domain('domain', dict(), list(), list(), dict())
    test = Problem('problem', domain, dict(), list(), list())
    assert(str(test) == repr(test))
