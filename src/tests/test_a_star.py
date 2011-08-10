from search import a_star, searchspace
from . import dummy_task
import py.test


# create 4 dummy tasks
task1 = dummy_task.get_search_space_at_goal()
task2 = dummy_task.get_simple_search_space()
task3 = dummy_task.get_simple_search_space_2()
task4 = dummy_task.get_search_space_no_solution()

# call the heuristic for each task
h1 = dummy_task.DummyHeuristic(task1)
h2 = dummy_task.DummyHeuristic(task2)
h3 = dummy_task.DummyHeuristic(task3)
h4 = dummy_task.DummyHeuristic(task4)

# create root node for each task
root1 = searchspace.make_root_node(task1.initial_state)
root2 = searchspace.make_root_node(task2.initial_state)
root3 = searchspace.make_root_node(task3.initial_state)
root4 = searchspace.make_root_node(task4.initial_state)


# Testing each function if it returns the correct values

def test_ordered_node_astar1():
    h_val = h1(root1)
    assert a_star.ordered_node_astar(root1, h_val, 0) == (0, 0, 0, root1)


def test_ordered_node_astar2():
    h_val = h2(root2)
    assert a_star.ordered_node_astar(root2, h_val, 0) == (5, 5, 0, root2)


def test_ordered_node_astar3():
    h_val = h3(root3)
    assert a_star.ordered_node_astar(root3, h_val, 0) == (4, 4, 0, root3)


def test_ordered_node_astar4():
    h_val = h4(root4)
    assert a_star.ordered_node_astar(root4, h_val, 0) == (15, 15, 0, root4)


def test_ordered_node_weighted_astar1():
    h_val = h1(root1)
    actual = a_star.ordered_node_weighted_astar(5)(root1, h_val, 0)
    assert actual == (0, 0, 0, root1)


def test_ordered_node_weighted_astar2():
    h_val = h2(root2)
    actual = a_star.ordered_node_weighted_astar(5)(root2, h_val, 0)
    assert actual == (25, 5, 0, root2)


def test_ordered_node_weighted_astar3():
    h_val = h3(root3)
    actual = a_star.ordered_node_weighted_astar(5)(root3, h_val, 0)
    assert actual == (20, 4, 0, root3)


def test_ordered_node_weighted_astar4():
    h_val = h4(root4)
    assert a_star.ordered_node_weighted_astar(5)(root4, h_val, 0) == (75, 15,
                                                                      0, root4)


def test_ordered_node_greedy_best_first1():
    h_val = h1(root1)
    assert a_star.ordered_node_greedy_best_first(root1, h_val, 0) == (0, 0, 0,
                                                                      root1)


def test_ordered_node_greedy_best_first2():
    h_val = h2(root2)
    assert a_star.ordered_node_greedy_best_first(root2, h_val, 0) == (5, 5, 0,
                                                                      root2)


def test_ordered_node_greedy_best_first3():
    h_val = h3(root3)
    assert a_star.ordered_node_greedy_best_first(root3, h_val, 0) == (4, 4, 0,
                                                                      root3)


def test_ordered_node_greedy_best_first4():
    h_val = h4(root4)
    assert a_star.ordered_node_greedy_best_first(root4, h_val, 0) == (15, 15,
                                                                      0, root4)


def test_astar_search1():
    """ The initial state is the goal state, so the plan is an empty list"""
    assert a_star.astar_search(task1, h1,
                               make_open_entry=a_star.ordered_node_astar) == []


def test_astar_search2():
    """ The plan has length 3 """
    assert len(a_star.astar_search(
                    task2, h2, make_open_entry=a_star.ordered_node_astar)) == 3


def test_astar_search3():
    assert len(a_star.astar_search(
                    task3, h3, make_open_entry=a_star.ordered_node_astar)) == 4


def test_astar_search4():
    """ The task is unsolvable """
    assert a_star.astar_search(task4,
                         h4, make_open_entry=a_star.ordered_node_astar) is None
