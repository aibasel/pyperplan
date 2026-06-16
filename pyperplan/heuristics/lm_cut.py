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

"""Implementation of the LM-cut heuristic."""

import logging
from heapq import heappop, heappush

from ..search.searchspace import SearchNode
from ..task import State, Task
from .heuristic_base import Heuristic


class RelaxedFact:
    def __init__(self, name: str) -> None:
        self.name = name
        self.hmax_value: float = float("inf")
        self.precondition_of: list[RelaxedOp] = []
        self.effect_of: list[RelaxedOp] = []

    # Order facts by their hmax value so they can be stored in a heap, which
    # only requires __lt__.
    def __lt__(self, other: "RelaxedFact") -> bool:
        return self.hmax_value < other.hmax_value

    def clear(self) -> None:
        self.hmax_value = float("inf")

    def dump(self) -> str:
        precond_of = [str(p) for p in self.precondition_of]
        effect_of = [str(e) for e in self.effect_of]
        return (
            f"< FACT name: {self.name}, hmax: {self.hmax_value:f}, "
            f"precond_of: {precond_of}, effect_of: {effect_of} >"
        )

    def __str__(self) -> str:
        return self.name

    # Defined as a method (rather than ``__repr__ = dump``) so the class can be
    # compiled with mypyc, which does not expose dunders via ``__dict__``.
    def __repr__(self) -> str:
        return self.dump()


class RelaxedOp:
    # The number of unsatisfied preconditions during cut-finding; set on the
    # operator from LmCutHeuristic.find_cut, declared here so the compiled
    # (mypyc) class accepts the assignment.
    precond_unsat: int

    def __init__(self, name: str, cost_zero: bool = False) -> None:
        self.name = name
        self.precondition: list[RelaxedFact] = []
        self.effects: list[RelaxedFact] = []
        # The most expensive predecessor.
        self.hmax_supporter: RelaxedFact | None = None
        self.hmax_value: float = float("inf")
        self.cost_zero = cost_zero
        # Used to check whether the operator can be applied.
        self.preconditions_unsat = 0
        self.cost = 0.0 if cost_zero else 1.0

    # Order operators by their hmax value so they can be stored in a heap, which
    # only requires __lt__.
    def __lt__(self, other: "RelaxedOp") -> bool:
        return self.hmax_value < other.hmax_value

    def clear(self, clear_op_cost: bool) -> None:
        """Reset the operator to its default values.

        Called during the hmax computation on each operator: clears
        ``preconditions_unsat`` and resets the cost to 1.
        """
        self.preconditions_unsat = len(self.precondition)
        if clear_op_cost and not self.cost_zero:
            self.cost = 1.0
        self.hmax_supporter = None
        self.hmax_value = float("inf")

    def dump(self) -> str:
        precond = [str(p) for p in self.precondition]
        effects = [str(e) for e in self.effects]
        return (
            f"< OPERATOR name: {self.name}, hmax_supp: {self.hmax_supporter}, "
            f"precond: {precond}, effects: {effects}, cost: {self.cost} >"
        )

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.dump()


class LmCutHeuristic(Heuristic):
    """Class and methods for computing the LM-cut heuristic value.

    We define some constant names for special facts and operators.
    NOTE: we use upper case names here as the PDDL tasks generally do not
    contain any upper case names. This way it is ensured that the denominators
    'ALWAYSTRUE', 'GOAL' and 'GOALOP' are always unique.
    """

    # Operators without preconditions get ALWAYSTRUE as their precondition.
    always_true = "ALWAYSTRUE"
    # We use these to model a single goal instead of multiple goals.
    explicit_goal = "GOAL"
    goal_operator_name = "GOALOP"

    def __init__(self, task: Task) -> None:
        self.relaxed_facts: dict[str, RelaxedFact] = {}
        self.relaxed_ops: dict[str, RelaxedOp] = {}
        # Holds both fact names (added from the start state) and RelaxedFact
        # objects (added during the forward pass); only the latter are queried.
        self.reachable: set[str | RelaxedFact] = set()
        self.goal_plateau: set[RelaxedFact] = set()
        self.dead_end = True

        self._compute_relaxed_facts_and_operators(task)

    def _compute_relaxed_facts_and_operators(self, task: Task) -> None:
        """Store all facts from the task as relaxed facts into our dict."""

        # little helper functions that build the relaxed operator graph
        def link_op_to_precondition(relaxed_op: RelaxedOp, factname: str) -> None:
            relaxed_op.precondition.append(self.relaxed_facts[factname])
            self.relaxed_facts[factname].precondition_of.append(relaxed_op)

        def link_op_to_effect(relaxed_op: RelaxedOp, factname: str) -> None:
            relaxed_op.effects.append(self.relaxed_facts[factname])
            self.relaxed_facts[factname].effect_of.append(relaxed_op)

        for fact in task.facts:
            self.relaxed_facts[fact] = RelaxedFact(fact)

        for op in task.operators:
            assert op.name not in self.relaxed_ops
            # build new relaxed operator from the task operator
            relaxed_op = RelaxedOp(op.name)
            # insert all preconditions into relaxed_op and
            # mark all preconditions in the relaxed_facts

            if not op.preconditions:
                # insert one fact that is always true if not already defined
                # --> this fact will be used for all operators with empty
                # preconditions
                if self.always_true not in self.relaxed_facts:
                    self.relaxed_facts[self.always_true] = RelaxedFact(self.always_true)
                link_op_to_precondition(relaxed_op, self.always_true)
            else:
                for fact in op.preconditions:
                    assert fact in self.relaxed_facts
                    link_op_to_precondition(relaxed_op, fact)
            # insert all effects into relaxed_op and
            # mark all effects in relaxed_facts
            for fact in op.add_effects:
                assert fact in self.relaxed_facts
                link_op_to_effect(relaxed_op, fact)
            # insert relaxed_op into hash
            self.relaxed_ops[op.name] = relaxed_op

        # insert explicit goal and goal operator
        goalfact = RelaxedFact(self.explicit_goal)
        goalop = RelaxedOp(self.goal_operator_name, True)
        self.relaxed_facts[self.explicit_goal] = goalfact
        self.relaxed_ops[self.goal_operator_name] = goalop

        link_op_to_effect(goalop, self.explicit_goal)

        # link all goals to the explicit goal
        for fact in task.goals:
            assert fact in self.relaxed_facts
            link_op_to_precondition(goalop, fact)

    def compute_hmax(self, state: State, clear_op_cost: bool = True) -> None:
        """Compute hmax values with a Dijkstra like procedure."""
        self.reachable.clear()
        facts_seen: set[RelaxedFact] = set()
        unexpanded: list[RelaxedFact] = []
        op_cleared: set[RelaxedOp] = set()
        fact_cleared: set[RelaxedFact] = set()
        start_state = set(state)
        if self.always_true in self.relaxed_facts:
            start_state.add(self.always_true)
        for fact in start_state:
            self.reachable.add(fact)
            fact_obj = self.relaxed_facts[fact]
            fact_obj.hmax_value = 0.0
            # mark all initial facts such that they are not cleared again!
            fact_cleared.add(fact_obj)
            facts_seen.add(fact_obj)
            heappush(unexpanded, fact_obj)
        while unexpanded:
            fact_obj = heappop(unexpanded)
            if fact_obj == self.relaxed_facts[self.explicit_goal]:
                self.dead_end = False
            # store fact as reachable
            self.reachable.add(fact_obj)
            hmax_value = fact_obj.hmax_value
            # update all operators that have this fact
            # as their precondition
            for op in fact_obj.precondition_of:
                # check if we have explored this operator in this iteration
                # --> if this is not the case then precond_fulfilled might
                # still contain facts from a previous heuristic computation
                # hence we need to clear it first!
                if op not in op_cleared:
                    op.clear(clear_op_cost)
                    op_cleared.add(op)
                op.preconditions_unsat -= 1
                # first check if all preconditions are fullfilled
                if op.preconditions_unsat == 0:
                    # update hmax_supporter if necessary
                    if (
                        op.hmax_supporter is None
                        or hmax_value > op.hmax_supporter.hmax_value
                    ):
                        op.hmax_supporter = fact_obj
                        # store for next hmax iteration
                        op.hmax_value = hmax_value + op.cost
                    assert op.hmax_supporter is not None
                    hmax_next = op.hmax_supporter.hmax_value + op.cost
                    for eff in op.effects:
                        if eff not in fact_cleared:
                            # clear fact if necessary
                            eff.clear()
                            fact_cleared.add(eff)
                        if hmax_next < eff.hmax_value:
                            eff.hmax_value = hmax_next
                        if eff not in facts_seen:
                            # enqueue effect if not already explored
                            facts_seen.add(eff)
                            heappush(unexpanded, eff)

    def compute_hmax_from_last_cut(
        self, state: State, last_cut: set[RelaxedOp]
    ) -> None:
        """This computes hmax values starting from the last cut.

        This saves us from recomputing the hmax values of all facts/operators
        that have not changed anyway.
        NOTE: a complete cut procedure needs to be finished (i.e. one cut must
        be computed) for this to work!
        """
        unexpanded: list[RelaxedOp] = []
        # Enqueue all operators from the last cut, whose hmax values need to be
        # recomputed.
        for op in last_cut:
            assert op.hmax_supporter is not None
            op.hmax_value = op.hmax_supporter.hmax_value + op.cost
            heappush(unexpanded, op)
        while unexpanded:
            # Iterate over all operators whose effects might need updating.
            op = heappop(unexpanded)
            next_hmax = op.hmax_value
            for fact_obj in op.effects:
                # Update the fact's hmax value if it is outdated.
                fact_hmax = fact_obj.hmax_value
                if fact_hmax > next_hmax:
                    fact_obj.hmax_value = next_hmax
                    # enqueue all ops of which fact_obj is a hmax supporter
                    for next_op in fact_obj.precondition_of:
                        if next_op.hmax_supporter == fact_obj:
                            next_op.hmax_value = next_hmax + next_op.cost
                            for supp in next_op.precondition:
                                if supp.hmax_value + next_op.cost > next_op.hmax_value:
                                    next_op.hmax_supporter = supp
                                    next_op.hmax_value = supp.hmax_value + next_op.cost
                            heappush(unexpanded, next_op)

    def compute_goal_plateau(self, fact_name: str) -> None:
        """Recursively mark a goal plateau."""
        # assure the fact itself is not in an unreachable region
        fact_in_plateau = self.relaxed_facts[fact_name]
        if (
            fact_in_plateau in self.reachable
            and fact_in_plateau not in self.goal_plateau
        ):
            # add this fact to the goal plateau
            self.goal_plateau.add(fact_in_plateau)
            for op in fact_in_plateau.effect_of:
                # recursive call to mark hmax_supporters of all operators
                if op.cost == 0:
                    assert op.hmax_supporter is not None
                    self.compute_goal_plateau(op.hmax_supporter.name)

    def find_cut(self, state: State) -> set[RelaxedOp]:
        """This returns the set of relaxed operators which are in the cut."""
        unexpanded: list[RelaxedFact] = []
        facts_seen: set[RelaxedFact] = set()
        op_cleared: set[RelaxedOp] = set()
        cut: set[RelaxedOp] = set()

        start_state = set(state)
        if self.always_true in self.relaxed_facts:
            start_state.add(self.always_true)
        for fact in start_state:
            assert fact in self.relaxed_facts
            fact_obj = self.relaxed_facts[fact]
            facts_seen.add(fact_obj)
            heappush(unexpanded, fact_obj)
        while unexpanded:
            fact_obj = heappop(unexpanded)
            for relaxed_op in fact_obj.precondition_of:
                if relaxed_op not in op_cleared:
                    relaxed_op.precond_unsat = len(relaxed_op.precondition)
                    op_cleared.add(relaxed_op)
                relaxed_op.precond_unsat -= 1
                # check if the operator preconditions are all satisfied
                if relaxed_op.precond_unsat == 0:
                    # if so we can expand this operator
                    for eff in relaxed_op.effects:
                        if eff in facts_seen:
                            continue
                        if eff in self.goal_plateau:
                            cut.add(relaxed_op)
                        else:
                            facts_seen.add(eff)
                            heappush(unexpanded, eff)
        return cut

    def __call__(self, node: SearchNode) -> float:
        state = node.state
        heuristic_value = 0.0
        goal_state = self.relaxed_facts[self.explicit_goal]
        # Assume the node is a dead end unless the hmax computation proves
        # otherwise.
        self.dead_end = True
        # Compute hmax starting from the current state.
        self.compute_hmax(state, True)
        if goal_state.hmax_value == float("inf"):
            return float("inf")
        while goal_state.hmax_value != 0:
            # Find an appropriate cut: first compute the goal plateau, then the
            # cut itself.
            self.goal_plateau.clear()
            self.compute_goal_plateau(self.explicit_goal)
            cut = self.find_cut(state)
            # Update the heuristic value and reduce the cut operators' costs.
            min_cost = min(o.cost for o in cut)
            heuristic_value += min_cost
            for o in cut:
                o.cost -= min_cost
                logging.debug(repr(o))
            # Compute the next hmax starting from the cut.
            self.compute_hmax_from_last_cut(state, cut)
        if self.dead_end:
            return float("inf")
        else:
            return heuristic_value
