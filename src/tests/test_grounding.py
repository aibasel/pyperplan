#from grounding import Grounder
import grounding
from pddl.parser import Parser
from task import Operator
from pddl.pddl import Type, Predicate, Effect, Action, Domain, Problem


def assert_equal(result, expected):
    assert result == expected


def get_action(name, signature, precondition, addlist, dellist):
    effect = Effect()
    effect.addlist = set(addlist)
    effect.dellist = set(dellist)
    return Action(name, signature, precondition, effect)

"""
test domain and problem
"""

# types:
type_object = Type("object", None)
type_vehicle = Type("vehicle", type_object)
type_car = Type("car", type_vehicle)
type_truck = Type("truck", type_vehicle)
type_city = Type("city", type_object)
type_country = Type("country", type_object)
type_my_car = Type("my_car", type_vehicle)
type_color = Type("color", type_object)

types = {"object": type_object, "vehicle": type_vehicle, "car": type_car,
         "truck": type_truck, "city": type_city, "country": type_country,
         "my_car": type_my_car, "color": type_color}

# predicates:
predicate_car_orig = Predicate("at", [("car", types["car"]),
                                      ("orig", types["city"])])
predicate_car_dest = Predicate("at", [("car", types["car"]),
                                      ("dest", types["city"])])
predicate_veh_orig = Predicate("at", [("vehicle", types["vehicle"]),
                                      ("orig", types["city"])])
predicate_veh_dest = Predicate("at", [("vehicle", types["vehicle"]),
                                      ("dest", types["city"])])
predicate_in = Predicate("in", [("car", types["car"]), ("in", types["city"])])
#predicate which does not occur in any operator:
predicate_car_color = Predicate("car_color", [("car", types["car"]),
                                              ("color", types["color"])])
predicate_at = Predicate("at", [("vehicle", types["vehicle"]),
                                ("city", types["city"])])

predicates = {"at": predicate_car_dest, "in": predicate_in,
              "car_color": predicate_car_color}

# actions:
action_drive_car = get_action("DRIVE-CAR", [("car", [types["car"]]),
                         ("orig", [types["city"]]), ("dest", [types["city"]])],
                         [predicate_car_dest], [predicate_car_orig],
                         [predicate_car_dest])

actions = {"drive-car": action_drive_car}

# objects:
objects = {"red_car": types["car"], "green_car": types["car"],
           "blue_truck": types["truck"],  "freiburg": types["city"],
           "basel": types["city"], "green": types["color"],
           "yellow": types["color"]}

# initial and goal state:
initial_state = [Predicate("at", [("red_car", types["car"]),
                                  ("freiburg", types["city"])]),
                 Predicate("at", [("green_car", types["car"]),
                                  ("basel", types["city"])]),
                 Predicate("at", [("blue_truck", types["truck"]),
                                  ("freiburg", types["city"])]),
                 Predicate("at", [("yellow_truck", types["truck"]),
                                  ("basel", types["city"])])]

goal_state = [Predicate("at", [("red_car", types["car"]),
                               ("basel", types["city"])]),
                 Predicate("at", [("green_car", types["car"]),
                                  ("freiburg", types["city"])]),
                 Predicate("at", [("blue_truck", types["truck"]),
                                  ("basel", types["city"])]),
                 Predicate("at", [("yellow_truck", types["truck"]),
                                  ("freiburg", types["city"])])]

# domain and problem
standard_domain = Domain("test_domain_statics", types, predicates, actions)
standard_problem = Problem("test_problem_statics", standard_domain, objects,
                           initial_state, goal_state)


def test_statics1():
    """
    A static predicate is a predicate, which doesn't occur in an effect of an
    action.
    """
    type_object = Type("object", None)
    type_car = Type("car", type_vehicle)
    type_city = Type("city", type_object)
    type_country = Type("country", type_object)
    types = {"object": type_object, "car": type_car, "city": type_city,
             "country": type_country}

    predicate_orig = Predicate("at", [("car", types["car"]),
                                      ("dest", types["city"])])
    predicate_dest = Predicate("at", [("car", types["car"]),
                                      ("orig", types["city"])])
    predicate_in = Predicate("in", [("city", types["city"]),
                                    ("country", types["country"])])

    action_drive_car = get_action("DRIVE-CAR", [("car", [types["car"]]),
                             ("loc-orig", [types["city"]]),
                             ("loc-dest", [types["city"]])],
                             [predicate_orig], [predicate_dest],
                             [predicate_orig])

    expected = [("in", grounding._get_statics([predicate_in],
                                              [action_drive_car]), True),
                ("dest", grounding._get_statics([predicate_dest],
                                                [action_drive_car]), False),
                ("orig", grounding._get_statics([predicate_orig],
                                                [action_drive_car]), False)]

    for pre, statics, element in expected:
        yield in_statics, pre, statics, element


def test_statics2():
    type_object = Type("object", None)

    predicate_a = Predicate("a", [])
    predicate_b = Predicate("b", [])

    the_action = get_action("the-action", [], [predicate_a], [predicate_b], [])

    statics = grounding._get_statics([predicate_a, predicate_b], [the_action])

    assert predicate_a.name in statics and predicate_b.name not in statics


def in_statics(predicate, statics, element):
    if element:
        assert predicate in statics
    else:
        assert not predicate in statics


def test_type_map1():
    """type map: maps each type to a list of objects"""
    type_object = Type("object", None)
    type_vehicle = Type("vehicle", type_object)
    type_car = Type("car", type_vehicle)
    type_truck = Type("truck", type_vehicle)
    type_city = Type("city", type_object)

    objects = {"red_car": type_car, "green_car": type_car,
               "blue_truck": type_truck, "motorbike": type_vehicle,
               "freiburg": type_city, "basel": type_city}

    type_map = grounding._create_type_map(objects)

    expected = [("red_car", type_map[type_car]),
                ("green_car", type_map[type_car]),
                ("blue_truck", type_map[type_truck]),
                ("red_car", type_map[type_vehicle]),
                ("green_car", type_map[type_vehicle]),
                ("blue_truck", type_map[type_vehicle]),
                ("motorbike", type_map[type_vehicle]),
                ("freiburg", type_map[type_city]),
                ("basel", type_map[type_city]),
                ("green_car", type_map[type_object]),
                ("motorbike", type_map[type_object]),
                ("basel", type_map[type_object])]

    for object, object_list in expected:
        yield in_object_set, object, object_list


def test_type_map2():
    type_object = Type("object", None)
    objects = {"object1": type_object}
    type_map = grounding._create_type_map(objects)
    assert "object1" in type_map[type_object]


def in_object_set(object, object_list):
    assert object in object_list


def test_collect_facts():
    op1 = Operator("op1", {"var1"}, {}, {"var3"})
    op2 = Operator("op2", {"var2"}, {"var3"}, {})
    op3 = Operator("op3", {}, {"var1"}, {"var4"})
    assert {"var1", "var2", "var3", "var4"} == grounding._collect_facts(
                                                               [op1, op2, op3])


def test_operators():

    # action with signature with 2 types
    action_drive_vehicle = get_action("DRIVE-VEHICLE",
                                      [("vehicle", [types["car"],
                                                    types["truck"]]),
                                       ("orig", [types["city"]]),
                                       ("dest", [types["city"]])],
                                      [predicate_veh_orig],
                                      [predicate_veh_dest],
                                      [predicate_veh_orig])

    # action with predicate in add & delete list
    action_add_delete = get_action("STAY", [("car", [types["car"]]),
                                            ("in", [types["city"]])],
                                   [predicate_in], [predicate_in],
                                   [predicate_in])

    # action with constant input
    action_constant = get_action("CONSTANT-ACTION",
                                 [("my_car", [types["my_car"]]),
                                  ("city", [types["city"]])],
                                 [],
                                 [Predicate("in", [("basel", [types["city"]]),
                                                   ("switzerland",
                                                    [types["country"]])])], [])

    # action with only delete effects
    action_only_delete = get_action("LEAVE",
                                    [("car", [types["car"]]),
                                     ("in", [types["city"]])],
                                    [predicate_in], [], [predicate_in])

    # action with delete effect which does not occur in precondition
    action_delete = get_action("DELETE", [("car", [types["car"]]),
                                          ("orig", [types["city"]]),
                                          ("dest", [types["city"]])],
                               [], [predicate_car_orig], [predicate_car_dest])

    type_map = grounding._create_type_map(objects)

    grounded_initial_state = grounding._get_partial_state(initial_state)

    grounded_drive_car = list(
        grounding._ground_action(action_drive_car, type_map, [],
                                 grounded_initial_state))
    grounded_drive_vehicle = list(
        grounding._ground_action(action_drive_vehicle, type_map, [],
                                 grounded_initial_state))
    grounded_add_delete = list(
        grounding._ground_action(action_add_delete, type_map, [],
                                 grounded_initial_state))
    grounded_only_delete = list(
        grounding._ground_action(action_only_delete, type_map, [],
                                 grounded_initial_state))
    grounded_delete = list(
        grounding._ground_action(action_delete, type_map, [],
                                 grounded_initial_state))

    domain = Domain("test_domain", types,
                    {"in": Predicate("in", [("city", types["city"]),
                                            ("country", types["country"])])},
                    {"action-constant": action_constant},
                    {"my_car": types["car"]})

    problem = Problem("test_problem", domain, objects, initial_state,
                      goal_state)
    task = grounding.ground(problem)
    grounded_constant = task.operators

    expected = [("(DRIVE-CAR red_car freiburg basel)", grounded_drive_car),
                ("(DRIVE-VEHICLE blue_truck freiburg basel)",
                 grounded_drive_vehicle),
                ("(STAY red_car freiburg)", grounded_add_delete),
                ("(LEAVE red_car freiburg)", grounded_only_delete),
                ("(DELETE red_car freiburg basel)", grounded_delete)]

    for operator, grounded_operators in expected:
        yield operator_grounded, operator, grounded_operators


def operator_grounded(operator, grounded_operators):
    grounded = False
    for op in grounded_operators:
        if(operator == op.name):
            grounded = True
    assert grounded


def test_create_operator():
    statics = grounding._get_statics(standard_domain.predicates.values(),
                                     [action_drive_car])
    initial_state = [Predicate("at", [("ford", types["car"]),
                                      ("freiburg", types["city"])])]

    operator = grounding._create_operator(
        action_drive_car,
        {"car": "ford", "dest": "berlin", "orig": "freiburg"},
        [], initial_state)
    assert operator.name == "(DRIVE-CAR ford freiburg berlin)"
    assert operator.preconditions == {'(at ford berlin)'}
    assert operator.add_effects == {'(at ford freiburg)'}
    assert operator.del_effects == {'(at ford berlin)'}


def test_get_grounded_string():
    grounded_string = "(DRIVE-CAR ford freiburg berlin)"
    assert grounding._get_grounded_string(
        "DRIVE-CAR", ["ford", "freiburg", "berlin"]) == grounded_string


def test_ground():
    """
    predicate which does not occur in any operator: "car_color"

    -> does it occurs in a variable?
    -> does it occur in an operator?
    """
    task = grounding.ground(standard_problem)

    assert not any(var.startswith("car_color") for var in task.facts)

    for operators in task.operators:
        assert not any(pre.startswith("car_color")
                       for pre in operators.preconditions)
        assert not any(add.startswith("car_color")
                       for add in operators.add_effects)
        assert not any(dee.startswith("car_color")
                       for dee in operators.del_effects)


def test_regression():
    parser = Parser('')

    def parse_problem(domain, problem):
        parser.domInput = domain
        parser.probInput = problem
        domain = parser.parse_domain(False)
        return parser.parse_problem(domain, False)

    prob_05 = """
    ;; See domain file for description of this test.

    (define (problem regression-test-05)
      (:domain regression-test)
      (:objects y - object)
      (:init)
      (:goal (the-predicate x y)))
    """

    dom_05 = """
    ;; Expected behaviour: plan of length one found
    ;; Observed behaviour (r265): plan of length zero found

    (define (domain regression-test)
      (:requirements :typing) ;; work around problem in regression test #4.
      (:predicates (the-predicate ?v1 ?v2 - object))
      (:constants x - object)

      (:action theaction
       :parameters (?x - object)
       :precondition (and)
       :effect (the-predicate x ?x)
      )
    )
    """

    prob_06 = """
    ;; See domain file for description of this test.

    (define (problem regression-test-06)
      (:domain regression-test)
      (:objects y - object)
      (:init)
      (:goal (the-predicate y y)))

    """
    dom_06 = """
    ;; Expected behaviour: planner proves that no plan exists
    ;; Observed behaviour (r265): plan of length one found

    (define (domain regression-test)
      (:requirements :typing) ;; work around problem in regression test #4.
      (:predicates (the-predicate ?v1 ?v2 - object))
      (:constants x - object)

      (:action theaction
       :parameters (?x - object)
       :precondition (and)
       :effect (the-predicate x ?x)
      )
    )
    """

    # problem / domain 07 contains a different action compared
    # to the actions of domain 5 & 6
    prob_07 = prob_06

    dom_07 = """
    (define (domain regression-test)
      (:requirements :typing) ;; work around problem in regression test #4.
      (:predicates (the-predicate ?v1 ?v2 - object))
      (:constants y - object)

      (:action theaction
       :parameters (?x - object)
       :precondition (and)
       :effect (the-predicate y ?x)
      )
    )
    """

    # action of problem / domain 8 differs only in the variable name compared
    # to the actions of problem 5 and 6: After grounding there should be no
    # difference between the grounded actions
    prob_08 = prob_05

    dom_08 = """
    (define (domain regression-test)
      (:requirements :typing) ;; work around problem in regression test #4.
      (:predicates (the-predicate ?v1 ?v2 - object))
      (:constants x - object)

      (:action theaction
       :parameters (?z - object)
       :precondition (and)
       :effect (the-predicate x ?z)
      )
    )
    """

    parsed_problem5 = parse_problem(dom_05, prob_05)
    parsed_problem6 = parse_problem(dom_06, prob_06)
    parsed_problem7 = parse_problem(dom_07, prob_07)
    parsed_problem8 = parse_problem(dom_08, prob_08)

    #coded input:
    type_object = Type("object", None)
    types = {"object": type_object}
    predicates = {"the_predicate": Predicate("the-predicate",
                                             [("v1", type_object),
                                              ("v2", type_object)])}
    constants = {"x": type_object}
    actions = {"theaction": get_action("theaction",
                                       [("?x", [type_object])], [],
                                       [Predicate("the-predicate",
                                        [("x", type_object),
                                         ("?x", type_object)])], [])}
    domain = Domain("regression-test", types, predicates, actions, constants)
    problem5 = Problem("regression-test-05", domain, {"y": type_object}, [],
                       [Predicate("the-predicate", [("x", type_object),
                                                    ("y", type_object)])])
    problem6 = Problem("regression-test-06", domain, {"y": type_object}, [],
                       [Predicate("the-predicate", [("y", type_object),
                                                    ("y", type_object)])])

    parsed_task5 = grounding.ground(parsed_problem5)
    coded_task5 = grounding.ground(problem5)
    parsed_task6 = grounding.ground(parsed_problem6)
    coded_task6 = grounding.ground(problem6)
    parsed_task7 = grounding.ground(parsed_problem7)
    parsed_task8 = grounding.ground(parsed_problem8)

    expected = [(parsed_task5.operators, coded_task5.operators, True),
                (parsed_task6.operators, coded_task6.operators, True),
                (parsed_task5.operators, coded_task6.operators, True),
                (parsed_task5.operators, parsed_task7.operators, False),
                (parsed_task5.operators, parsed_task8.operators, True)]

    for operator1, operator2, expected_result in expected:
        yield compare_operators, operator1, operator2, expected_result


def compare_operators(operators1, operators2, expected):

    def compare_operator(operator1, operator2):
        return (operator1.name == operator2.name and
                operator1.preconditions == operator2.preconditions and
                operator1.add_effects == operator2.add_effects and
                operator1.del_effects == operator2.del_effects)

    for operator1 in operators1:
        if(not(any(compare_operator(operator1, operator2)
                   for operator2 in operators2))):
            return False == expected
    return True == expected


def test_add_del_effects():
    parser = Parser('')

    def parse_problem(domain, problem):
        parser.domInput = domain
        parser.probInput = problem
        domain = parser.parse_domain(False)
        return parser.parse_problem(domain, False)

    dom_pddl = """
    (define (domain dom)
      (:requirements :typing)
      (:predicates (ok ?v - object))

      (:action theaction
       :parameters (?x - object)
       :precondition {0}
       :effect {1}
      )
    )
    """

    prob_pddl = """
    ;; See domain file for description of this test.

    (define (problem prob)
      (:domain dom)
      (:objects y - object)
      (:init)
      (:goal (ok y)))
    """

    tests = [
        # Only add effect
        ('(and)', '(ok ?x)', set(), {'(ok y)'}, set()),
        # Only delete effect
        ('(and)', '(and (not (ok ?x)))', set(), set(), {'(ok y)'}),
        # Both add and delete effect
        ('(and)', '(and (ok ?x) (not (ok ?x)))', set(), {'(ok y)'}, set()),
        # Precondition and add effect
        ('(and (ok ?x))', '(ok ?x)', {'(ok y)'}, set(), set()),
        # Precondition and delete effect
        ('(and (ok ?x))', '(and (not (ok ?x)))', {'(ok y)'}, set(),
         {'(ok y)'}),
        # Precondition and both add and delete effect
        ('(and (ok ?x))', '(and (ok ?x) (not (ok ?x)))', {'(ok y)'}, set(),
         set()),
            ]

    for pre_in, eff_in, pre_exp, add_exp, del_exp in tests:
        dom = dom_pddl.format(pre_in, eff_in)
        problem = parse_problem(dom, prob_pddl)

        domain = problem.domain
        actions = domain.actions.values()
        predicates = domain.predicates.values()

        # Objects
        objects = problem.objects
        objects.update(domain.constants)

        # Get the names of the static predicates
        statics = grounding._get_statics(predicates, actions)

        # Create a map from types to objects
        type_map = grounding._create_type_map(objects)

        # Transform initial state into a specific
        init = grounding._get_partial_state(problem.initial_state)

        # Ground actions
        operators = grounding._ground_actions(actions, type_map, statics, init)

        yield assert_equal, len(operators), 1
        op = operators[0]
        yield assert_equal, op.preconditions, pre_exp
        yield assert_equal, op.add_effects, add_exp
        yield assert_equal, op.del_effects, del_exp
