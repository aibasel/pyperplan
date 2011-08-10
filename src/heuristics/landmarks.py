#
# This file is part of pyperplan.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#

"""
Landmarks Heuristic
"""

import copy
from collections import defaultdict

from heuristics.heuristic_base import Heuristic


def _get_relaxed_task(task):
    """
    Removes the delete effects of every operator in task
    """
    relaxed_task = copy.deepcopy(task)
    for op in relaxed_task.operators:
        op.del_effects = set()
    return relaxed_task


def get_landmarks(task):
    """ Returns a set of landmarks.

    In this implementation a fact is a landmark if the goal facts cannot be
    reached without it.
    """
    task = _get_relaxed_task(task)
    landmarks = set(task.goals)
    possible_landmarks = task.facts - task.goals

    for fact in possible_landmarks:
        current_state = task.initial_state
        goal_reached = current_state >= task.goals

        while not goal_reached:
            previous_state = current_state

            for op in task.operators:
                if op.applicable(current_state) and fact not in op.add_effects:
                    current_state = op.apply(current_state)
                    if current_state >= task.goals:
                        break
            if (previous_state == current_state and
                not current_state >= task.goals):
                landmarks.add(fact)
                break

            goal_reached = current_state >= task.goals
    return landmarks


def compute_landmark_costs(task, landmarks):
    """
    Compute uniform cost partitioning for actions depending on the landmarks
    they achieve.
    """
    op_to_lm = defaultdict(set)
    for operator in task.operators:
        for landmark in landmarks:
            if landmark in operator.add_effects:
                op_to_lm[operator].add(landmark)
    min_cost = defaultdict(lambda: float('inf'))
    for operator, landmarks in op_to_lm.items():
        landmarks_achieving = len(landmarks)
        for landmark in landmarks:
            min_cost[landmark] = min(min_cost[landmark],
                                     1 / landmarks_achieving)
    return min_cost


class LandmarkHeuristic(Heuristic):
    def __init__(self, task):
        self.task = task

        self.landmarks = get_landmarks(task)
        assert self.task.goals <= self.landmarks
        self.costs = compute_landmark_costs(task, self.landmarks)

    def __call__(self, node):
        """ Returns the heuristic value for "node". """
        if node.parent is None:
            # At the beginning only the initial facts are achieved
            node.unreached = self.landmarks - self.task.initial_state
        else:
            # A new node reaches the facts in its add_effects
            node.unreached = node.parent.unreached - node.action.add_effects
        # We always want to keep the goal facts unreached if they are not true
        # in the current state, even if they have been reached before
        unreached = node.unreached | (self.task.goals - node.state)

        h = sum(self.costs[landmark] for landmark in unreached)
        return h
