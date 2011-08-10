from heuristics import landmarks
from task import Task, Operator
from search import make_root_node


def test_compute_landmark_costs():
    op1 = Operator('op1', set(), {'A', 'C'}, set())
    op2 = Operator('op2', set(), {'B', 'C'}, set())
    op3 = Operator('op3', set(), {'D'}, set())
    task = Task('task1', set(), set(), set(), [op1, op2, op3])
    costs = landmarks.compute_landmark_costs(task, ['A', 'C', 'D'])
    print(costs)
    expected = {'A': 0.5, 'C': 0.5, 'D': 1}
    assert expected == costs


def test_relaxed_task():
    op1 = Operator('op1', {'A'}, {'A', 'C'}, {'B', 'C'})
    task = Task('task1', set(), set(), set(), [op1])
    relaxed_task = landmarks._get_relaxed_task(task)
    assert len(relaxed_task.operators[0].del_effects) == 0


def test_landmarks_goals():
    task = Task('task1', set(), set(), {'A'}, [])
    assert landmarks.get_landmarks(task) == {'A'}


def test_landmarks1():
    op1 = Operator('op1', set(), {'A'}, set())
    op2 = Operator('op2', {'A'}, {'B'}, set())
    task = Task('task1', {'A', 'B'}, set(), {'B'}, [op1, op2])
    assert landmarks.get_landmarks(task) == {'A', 'B'}


def test_heuristics():
    # simple task: two operators have to be applied
    task1 = Task('task1', {'A', 'B', 'C'}, frozenset({'A'}),
                 frozenset({'C', 'B'}),
                 [Operator('op1', {'A'}, {'B'}, set()),
                  Operator('op2', {'B'}, {'C'}, set()),
                  Operator('op3', {'B'}, {'A'}, set())])

    # initial state is part of the goal state: one operator has to be applied
    task2 = Task('task2', {'A', 'B', 'C'}, frozenset(['A', 'B']),
                 frozenset(['B', 'C']),
                 [Operator('op1', {'A'}, {'B'}, set()),
                  Operator('op2', {'B'}, {'C'}, set())])

    # task with one operator with two preconditions
    task3 = Task('task3', {'A', 'B', 'C'}, frozenset(['A', 'B']),
                 frozenset(['C']),
                 [Operator('op1', {'A', 'B'}, {'C'}, set())])

    # task with one operator with two effects
    task4 = Task('task4', {'A', 'B', 'C'}, frozenset(['A']),
                 frozenset(['C', 'B']),
                 [Operator('op1', {'A'}, {'B', 'C'}, set())])

    # task with one operator with equal precondition and effect,
    task4b = Task('task4b', {'A', 'B', 'C'}, frozenset(['A']),
                  frozenset(['C', 'B']),
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

    # columns:           landmarks      lm_costs                h
    expected = [(task1,  {'B', 'C'},    {'B': 1, 'C': 1},       2),
                (task2,  {'B', 'C'},    {'B': 1, 'C': 1},       1),
                (task3,  {'C'},         {'C': 1},               1),
                (task4,  {'B', 'C'},    {'B': 0.5, 'C': 0.5},       1),
                ]

    for task, expected_landmarks, expected_lmc, exptected_h in expected:
        assert landmarks.get_landmarks(task) == expected_landmarks
        assert landmarks.compute_landmark_costs(
                                      task, expected_landmarks) == expected_lmc
        assert landmarks.LandmarkHeuristic(task)(make_root_node(
                                            task.initial_state)) == exptected_h


def compare_h_values(Heuristic, task, expected):
    rh = Heuristic(task)
    h_value = rh(make_root_node(task.initial_state))
    print("Wrong value for", task.name, "with", str(Heuristic),
          ". Expected", expected, ", but got", h_value)
    assert h_value == expected
