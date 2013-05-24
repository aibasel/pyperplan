from task import Task, Operator
from pddl.parser import Parser
from search import searchspace
from search import astar_search
from search import enforced_hillclimbing_search
import grounding


blocks_dom = """\
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
                 )
"""


blocks_problem_1 = """\
(define (problem BLOCKS-4-0)
(:domain BLOCKS)
(:objects D B A C - block)
(:INIT (CLEAR C) (CLEAR A) (CLEAR B) (CLEAR D) (ONTABLE C) (ONTABLE A)
 (ONTABLE B) (ONTABLE D) (HANDEMPTY))
(:goal (AND (ON D C) (ON C B) (ON B A)))
)
"""


def _gen_h_values(initial_state, plan, heuristic):
    node = searchspace.SearchNode(initial_state, None, None, None)
    for op in plan:
        h_val = heuristic(node)
        yield h_val
        node = searchspace.SearchNode(op.apply(node.state), None, None, None)
    h_val = heuristic(node)
    yield h_val


def gen_heuristic_test(dom, prob, search_class, heuristic_class, h_values_plan,
                       plan_length=None):
    parser = Parser('')
    parser.domInput = dom
    parser.probInput = prob

    domain = parser.parse_domain(False)
    problem = parser.parse_problem(domain, False)

    task = grounding.ground(problem)

    heuristic = heuristic_class(task)
    plan = search_class(task, heuristic)
    if plan_length:
        assert len(plan) == plan_length
    # run through plan and validate heuristic value
    # the true_h_values are taken from fast downward with astar and lm cut
    # heuristic
    computed_h_values = list(_gen_h_values(task.initial_state, plan, heuristic))
    assert h_values_plan == computed_h_values


# test generator for the first blocks problem instance
def gen_blocks_test1(search_class, heuristic_class, h_values_plan,
                     plan_length=None):
    gen_heuristic_test(blocks_dom, blocks_problem_1, search_class,
                       heuristic_class, h_values_plan, plan_length=None)


def gen_blocks_test_astar(heuristic_class, h_values_plan, plan_length):
    return gen_blocks_test1(astar_search, heuristic_class, h_values_plan,
                            plan_length)


def gen_blocks_test_ehc(heuristic_class, h_values_plan, plan_length):
    return gen_blocks_test1(enforced_hillclimbing_search, heuristic_class,
                            h_values_plan, plan_length)
