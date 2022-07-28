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

from .heuristic_base import Heuristic
from ..task import Operator, Task

from itertools import combinations


DEBUG = False
DEBUG_VERBOSE = False


def dualize(task):
    dual_operators = [Operator(f"dual-{op.name}", op.del_effects, op.add_effects, op.preconditions) for op in task.operators]
    return Task(f"dual-{task.name}", task.facts, task.facts - task.goals, task.facts - task.initial_state, dual_operators)


def can_regress(conjunction, action):
    conj = frozenset(conjunction)
    return not action.del_effects.intersection(conj) and action.add_effects.intersection(conj)


def regress(conjunction, action):
    assert can_regress(conjunction, action)
    return tuple(sorted((frozenset(conjunction) - action.add_effects) | action.preconditions))


def get_subsets(conjunction):
    subsets = [(fact,) for fact in conjunction]
    subsets.extend([comb for comb in combinations(conjunction, 2)])
    return subsets


class H2DualHeuristic(Heuristic):
    """
    Implements the h^2 heuristic.
    """

    def __init__(self, task):
        super().__init__()
        self.task = task
        self.dual_task = dualize(task)
        sorted_facts = sorted(task.facts)
        self.conjunctions = get_subsets(sorted_facts)
        self.facts_to_id = {value: index for index, value in enumerate(self.conjunctions)}
        if DEBUG:
            print(sorted_facts)
            print(self.dual_task.initial_state)
            print(self.dual_task.goals)
            print(self.dual_task.operators)
            print("conjunctions")
            for conj in self.conjunctions:
                print(conj)
        # print(f"conjunctions to ids: {self.facts_to_id}")
        self._initialize_h_values()
        converged = False
        while not converged:
            if DEBUG_VERBOSE:
                print("========= starting iteration to update h values ======")
            converged = True
            new_h_values = list(self.h_values)
            for conj in self.conjunctions:
                min_h = self.h_values[self._get_id(conj)]
                if min_h > 0:
                    if DEBUG_VERBOSE:
                        print(f"update {conj}, current h = {min_h}")
                    for action in self.task.operators:
                        if can_regress(conj, action):
                            regr = regress(conj, action)
                            h = self._compute_h(regr)
                            if DEBUG_VERBOSE:
                                print(f"regression through {action.name} led to {regr} which has h-value of {h}")
                            min_h = min(min_h, h+1)
                    if min_h != self.h_values[self._get_id(conj)]:
                        converged = False
                        new_h_values[self._get_id(conj)] = min_h
                        if DEBUG_VERBOSE:
                            print(f"updated h = {new_h_values[self._get_id(conj)]}")
            self.h_values = list(new_h_values)
            if DEBUG_VERBOSE:
                print()
        if DEBUG:
            for idx, conj in enumerate(self.conjunctions):
                assert self._get_id(conj) == idx
                print(f"h-value of {conj} = {self.h_values[idx]}")


    def _get_id(self, conj):
        assert isinstance(conj, tuple), f"{conj} is not a tuple, but {type(conj)}"
        assert conj in self.facts_to_id, f"{conj} is not a valid conjunction"
        return self.facts_to_id[conj]


    def _initialize_h_values(self):
        self.h_values = []
        for conj in self.conjunctions:
            if frozenset(conj).issubset(self.dual_task.initial_state):
                # print(f"{conj} is initially true")
                self.h_values.append(0)
            else:
                self.h_values.append(float('infinity'))
            assert self._get_id(conj) == len(self.h_values) - 1


    def _compute_h(self, conj):
        if len(conj) <= 2:
            return self.h_values[self._get_id(conj)]
        else:
            subsets = get_subsets(conj)
            max_h = 0
            for conj in subsets:
                max_h = max(max_h, self.h_values[self._get_id(conj)])
            return max_h


    def _dualize_state(self, state):
        return self.task.facts - state


    def __call__(self, node):
        state = node.state
        dual_state = self._dualize_state(state)
        if DEBUG:
            print(f"evaluate heuristic for {dual_state}")
        h = self._compute_h(tuple(sorted(dual_state)))
        if DEBUG:
            print(f"computed h-value: {h}")
        return h
