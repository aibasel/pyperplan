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

from itertools import combinations


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


class H2Heuristic(Heuristic):
    """
    Implements the h^2 heuristic.
    """

    def __init__(self, task):
        super().__init__()
        self.task = task
        print(task.facts)
        print(task.initial_state)
        print(task.goals)
        print(task.operators)
        sorted_facts = sorted(task.facts)
        print(sorted_facts)
        self.conjunctions = get_subsets(sorted_facts)
        self.facts_to_id = {value: index for index, value in enumerate(self.conjunctions)}
        print(f"conjunctions: {self.conjunctions}")
        print(f"conjunctions to ids: {self.facts_to_id}")


    def _get_id(self, conj):
        assert isinstance(conj, tuple), f"{conj} is not a tuple, but {type(conj)}"
        assert conj in self.facts_to_id, f"{conj} is not a valid conjunction"
        return self.facts_to_id[conj]


    def _get_initial_h_values(self, state):
        h_values = []
        for conj in self.conjunctions:
            if frozenset(conj).issubset(state):
                # print(f"{conj} is initially true")
                h_values.append(0)
            else:
                h_values.append(float('infinity'))
            assert self._get_id(conj) == len(h_values) - 1
        return h_values


    def _compute_h(self, h_values, conj):
        if len(conj) <= 2:
            return h_values[self._get_id(conj)]
        else:
            subsets = get_subsets(conj)
            max_h = 0
            for conj in subsets:
                max_h = max(max_h, h_values[self._get_id(conj)])
            return max_h


    def __call__(self, node):
        state = node.state
        print(f"evaluate heuristic for {state}")
        h_values = self._get_initial_h_values(state)
        converged = False
        while not converged:
            print("========= starting iteration to update h values ======")
            converged = True
            for conj in self.conjunctions:
                min_h = h_values[self._get_id(conj)]
                if min_h > 0:
                    print(f"update {conj}, current h = {min_h}")
                    for action in self.task.operators:
                        if can_regress(conj, action):
                            regr = regress(conj, action)
                            # print(f"regression through {action} led to {regr}")
                            h = self._compute_h(h_values, regr) + 1
                            min_h = min(min_h, h)
                    if min_h != h_values[self._get_id(conj)]:
                        converged = False
                        h_values[self._get_id(conj)] = min_h
                        print(f"updated h = {h_values[self._get_id(conj)]}")
            print()
        return self._compute_h(h_values, tuple(sorted(state)))
