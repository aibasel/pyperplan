from task import Task, Operator
from heuristics.relaxation import *
from pddl.parser import Parser
from search import a_star, enforced_hillclimbing_search
from search import make_root_node
from .heuristic_test_instances import *
import grounding
import py.test


def test_relaxation_heuristic_constructor():
    op1 = Operator('op1', {'A'}, {'B'}, set())
    op2 = Operator('op2', {'B'}, {'C'}, set())

    init = frozenset(['A'])
    goals = frozenset(['C'])
    task = Task('task1', {'A', 'B', 'C'}, init, goals, [op1, op2])

    rh = hAddHeuristic(task)
    rop1 = RelaxedOperator(op1.name, ['A'], ['B'])

    assert(len(rh.operators) == 2)
    assert(len(rh.facts) == 3)
    assert(rh.facts['A'].precondition_of[0].name == rop1.name)


def test_heuristics():

    # simple task: two operators have to be applied
    task1 = Task('task1', {'A', 'B', 'C'}, ['A'], ['C', 'B'],
                 [Operator('op1', {'A'}, {'B'}, set()),
                  Operator('op2', {'B'}, {'C'}, set()),
                  Operator('op3', {'B'}, {'A'}, set())])

    # initial state is part of the goal state: one operator has to be applied
    task2 = Task('task2', {'A', 'B', 'C'}, ['A', 'B'], ['B', 'C'],
                 [Operator('op1', {'A'}, {'B'}, set()),
                  Operator('op2', {'B'}, {'C'}, set())])

    # task with one operator with two preconditions
    task3 = Task('task3', {'A', 'B', 'C'}, ['A', 'B'], ['C'],
                 [Operator('op1', {'A', 'B'}, {'C'}, set())])

    # task with one operator with two effects
    task4 = Task('task4', {'A', 'B', 'C'}, ['A'], ['C', 'B'],
                 [Operator('op1', {'A'}, {'B', 'C'}, set())])

    # task with one operator with equal precondition and effect,
    task4b = Task('task4b', {'A', 'B', 'C'}, ['A'], ['C', 'B'],
                 [Operator('op1', {'A'}, {'A', 'B', 'C'}, set())])

    # task with one operator with several effects,
    # 2 operators have to be applied
    task5 = Task('task5', {'A', 'B', 'C', 'D', 'E', 'F'}, ['A'], ['E', 'F'],
                 [Operator('op1', {'A'}, {'B', 'C', 'D', 'E'}, set()),
                  Operator('op2', {'C'}, {'F'}, set())])

    # task with one operator with several preconditions
    task6 = Task('task6', {'A', 'B', 'C', 'D', 'E'}, ['A'], ['E'],
                 [Operator('op1', {'A'}, {'B'}, set()),
                  Operator('op2', {'B'}, {'C'}, set()),
                  Operator('op3', {'A'}, {'D'}, set()),
                  Operator('op4', {'A', 'C', 'B', 'D'}, {'E'}, set())])

    # task with empty initial state: no operator can be applied
    task7 = Task('task7', {'A', 'B', 'C'}, [], ['C'],
                 [Operator('op1', {'A'}, {'B'}, set()),
                  Operator('op2', {'B'}, {'C'}, set())])

    # task with initial state = goal state: no operator has to be applied
    task8 = Task('task8', {'A', 'B', 'C'}, ['C'], ['C'],
                 [Operator('op1', {'A'}, {'B'}, set()),
                  Operator('op2', {'B'}, {'C'}, set())])

    # task with operator with empty precondition
    task9 = Task('task9', {'A', 'B', 'C'}, [], ['C'],
                 [Operator('op1', {}, {'B'}, set()),
                  Operator('op2', {'B'}, {'C'}, set())])

    # a more complex task
    task10 = Task('task10', {'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'g'}, ['v1'],
                  ['g'],
                  [Operator('op1', {'v1'}, {'v2'}, set()),
                   Operator('op2', {'v2'}, {'v3'}, set()),
                   Operator('op3', {'v3'}, {'v4', 'v5'}, set()),
                   Operator('op4', {'v4', 'v5'}, {'g'}, set()),
                   Operator('op5', {'v2'}, {'v6'}, set()),
                   Operator('op6', {'v6'}, {'v5'}, set())])

    # another complex task
    task12 = Task('task12', {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'},
                  ['A', 'B'], ['F', 'G', 'H'],
                  [Operator('op1', {'A'}, {'C'}, set()),
                   Operator('op2', {'C', 'D'}, {'F'}, set()),
                   Operator('op3', {'D', 'E'}, {'G', 'H'}, set()),
                   Operator('op4', {'B'}, {'D', 'E'}, set()),
                   Operator('op5', {'I'}, {'H'}, set())])

    # task with no goal:
    task13 = Task('task13', {'A', 'B', 'C'}, ['A', 'B'], [],
                  [Operator('op1', {'A', 'B'}, {'C'}, set())])
    # task with no reachable goal:
    task14 = Task('task14', {'A', 'B', 'C'}, ['A'], ['B', 'C'],
                  [Operator('op1', {'A'}, {'B'}, set())])

    inf = float('inf')
    # columns:           h_add         h_max         h_sa          h_ff
    expected = [(task1,  3,            2,            2,            2),
                (task2,  1,            1,            1,            1),
                (task3,  1,            1,            1,            1),
                (task4,  2,            1,            1,            1),
                (task4b, 2,            1,            1,            1),
                (task5,  3,            2,            2,            2),
                (task6,  5,            3,            4,            4),
                (task7,  inf,          inf,          inf,        inf),
                (task8,  0,            0,            0,            0),
                (task9,  2,            2,            2,            2),
                (task10, 7,            4,            4,            4),
                (task12, 9,            2,            4,            4),
                (task13, 0,            0,            0,            0),
                (task14, inf,          inf,          inf,        inf)]

    for (task, expected_hAdd, expected_hMax, expected_hSA,
         expected_hFF) in expected:
        yield compare_h_values, hAddHeuristic, task, expected_hAdd
        yield compare_h_values, hMaxHeuristic, task, expected_hMax
        yield compare_h_values, hSAHeuristic, task, expected_hSA
        yield compare_h_values, hFFHeuristic, task, expected_hFF


def compare_h_values(Heuristic, task, expected):
    rh = Heuristic(task)
    h_value = rh(make_root_node(task.initial_state))
    print("Wrong value for", task.name, "with", str(Heuristic),
          ". Expected", expected, ", but got", h_value)
    assert h_value == expected


def test_hAdd_blocksworld_initial_state():
    parser = Parser('')
    parser.domInput = blocks_dom
    parser.probInput = blocks_problem_1

    domain = parser.parse_domain(False)
    problem = parser.parse_problem(domain, False)

    task = grounding.ground(problem)

    heuristic = hAddHeuristic(task)
    h_val = heuristic(make_root_node(task.initial_state))
    assert h_val, False == 6.


@py.test.mark.slow
def test_hMax_blocksworld_complete_astar():
    true_h_values = [2, 3, 2, 3, 2, 1, 0]
    plan_length = 6
    yield py.test.mark.slow(gen_blocks_test_astar), hMaxHeuristic, \
        true_h_values, plan_length


@py.test.mark.slow
def test_hAdd_blocksworld_complete_astar():
    true_h_values = [6, 8, 4, 5, 2, 1, 0]
    plan_length = 6
    yield py.test.mark.slow(gen_blocks_test_astar), hAddHeuristic, \
        true_h_values, plan_length


@py.test.mark.slow
def test_hSA_blocksworld_complete_astar():
    true_h_values = [6, 6, 4, 4, 2, 1, 0]
    plan_length = 6
    yield py.test.mark.slow(gen_blocks_test_astar), hSAHeuristic, \
        true_h_values, plan_length


@py.test.mark.slow
def test_hFF_blocksworld_complete_astar():
    true_h_values = [6, 6, 4, 4, 2, 1, 0]
    plan_length = 6
    yield py.test.mark.slow(gen_blocks_test_astar), hFFHeuristic, \
        true_h_values, plan_length


@py.test.mark.slow
def test_hMax_blocksworld_complete_enforced_hillclimbing():
    true_h_values = [2, 3, 2., 3, 2, 1, 0]
    plan_length = 6
    yield py.test.mark.slow(gen_blocks_test_astar), hMaxHeuristic, \
        true_h_values, plan_length
