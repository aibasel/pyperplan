"""
Unit Testing for the search space module
"""

from search.searchspace import make_root_node, make_child_node


# Construct a small tree in order to perform some needed test methods

root = make_root_node("state1")
child1 = make_child_node(root, "action1", "state2")
child2 = make_child_node(root, "action2", "state3")
grandchild1 = make_child_node(child1, "action3", "state4")
grandchild2 = make_child_node(child2, "action4", "state5")


def test_extract_solution():
    """
    Tests whether extract_solution method within class searchspace returns the
    list of actions starting from the root
    """
    assert root.extract_solution() == []
    assert grandchild1.extract_solution() == ["action1", "action3"]
    assert grandchild2.extract_solution() == ["action2", "action4"]


def test_g_values():
    """
    Tests whether the distance of the node from the root is computed properly
    """
    assert root.g == 0
    assert child1.g == 1
    assert grandchild2.g == 2


def test_states():
    """Tests the states of the node """
    assert root.state == "state1"
    assert child2.state == "state3"
    assert grandchild1.state == "state4"


# Hint: We do not need a test method to check whether the node contains the
# right action since this is done implicitly by the test_extract_solution
# method, i.e., if this test passes, it will imply that each node contains the
# right action
