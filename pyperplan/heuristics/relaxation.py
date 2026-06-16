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

"""The relaxation heuristics hAdd, hMax, hSA and hFF."""

import heapq
from collections.abc import Callable, Iterable
from typing import Any

from ..search.searchspace import SearchNode
from ..task import State, Task
from .heuristic_base import Heuristic

# A heap entry pairs a fact's distance with a tiebreaker and the fact itself.
Heap = list[tuple[float, int, "RelaxedFact"]]


class RelaxedFact:
    """A fact in the delete-relaxed task.

    Attributes:
        name: The name of the relaxed fact.
        precondition_of: The operators this fact is a precondition of.
        expanded: Whether this fact has been expanded during the Dijkstra
            forward pass.
        distance: The heuristic distance value.
        sa_set: The set of operators that have been applied to make this fact
            true (only for hSA).
        cheapest_achiever: The cheapest operator applied to reach this fact
            (only for hFF).
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.precondition_of: list[RelaxedOperator] = []
        self.expanded = False
        self.sa_set: set[str] | None = None
        self.cheapest_achiever: RelaxedOperator | None = None
        self.distance: float = float("inf")


class RelaxedOperator:
    """An operator in the delete-relaxed task (no delete effects).

    Attributes:
        name: The name of the relaxed operator.
        preconditions: The preconditions of this operator.
        add_effects: The add effects of this operator.
        cost: The cost of applying this operator.
        counter: Counts the preconditions not yet reached; the operator becomes
            applicable once it reaches zero.
    """

    def __init__(self, name: str, preconditions: State, add_effects: State) -> None:
        self.name = name
        self.preconditions = preconditions
        self.add_effects = add_effects
        self.cost = 1.0
        self.counter = len(preconditions)


class _RelaxationHeuristic(Heuristic):
    """Base class for all relaxation heuristics.

    It is not meant to be instantiated directly. In principle it already
    implements the hAdd heuristic.

    Attributes:
        facts: A dict mapping fact names to ``RelaxedFact`` objects.
        operators: A list of relaxed operators.
        init: The set of facts that define the initial state.
        goals: The set of facts that define the goal state.
        tie_breaker: A counter used to break ties in the priority queue.
        eval: A function used to evaluate the cost of applying an operator.
    """

    # ``eval`` aggregates precondition distances (sum for hAdd/hFF, max for
    # hMax); set by the subclasses.
    eval: Callable[[Iterable[float]], float]

    def __init__(self, task: Task) -> None:
        self.facts: dict[str, RelaxedFact] = {}
        self.operators: list[RelaxedOperator] = []
        self.goals: State = task.goals
        self.init: State = task.initial_state
        self.tie_breaker = 0
        self.start_state = RelaxedFact("start")

        # Create relaxed facts for all facts in the task description.
        for fact in task.facts:
            self.facts[fact] = RelaxedFact(fact)

        for op in task.operators:
            # Relax operators and add them to operator list.
            ro = RelaxedOperator(op.name, op.preconditions, op.add_effects)
            self.operators.append(ro)

            # Initialize precondition_of-list for each fact
            for var in op.preconditions:
                self.facts[var].precondition_of.append(ro)

            # Handle operators that have no preconditions.
            if not op.preconditions:
                # We add this operator to the precondition_of list of the start
                # state. This way it can be applied to the start state, which
                # also helps when the initial state is empty.
                self.start_state.precondition_of.append(ro)

    def __call__(self, node: SearchNode) -> float:
        """Compute the heuristic value for the state stored in ``node``."""
        state = node.state

        # Reset distance and set to default values.
        self.init_distance(state)

        # Construct the priority queue.
        heap: Heap = []
        # Add a dedicated start state, to cope with operators without
        # preconditions and empty initial state.
        heapq.heappush(heap, (0, self.tie_breaker, self.start_state))
        self.tie_breaker += 1

        for fact in state:
            # Its order is determined by the distance the facts.
            # As a tie breaker we use a simple counter.
            heapq.heappush(
                heap, (self.facts[fact].distance, self.tie_breaker, self.facts[fact])
            )
            self.tie_breaker += 1

        # Call the Dijkstra search that performs the forward pass.
        self.dijkstra(heap)

        # Extract the goal heuristic.
        return self.calc_goal_h()

    def init_distance(self, state: State) -> None:
        """Reset all state that has to be recomputed for each heuristic call."""

        def reset_fact(fact: RelaxedFact) -> None:
            fact.expanded = False
            fact.cheapest_achiever = None
            if fact.name in state:
                fact.distance = 0.0
                fact.sa_set = set()
            else:
                fact.sa_set = None
                fact.distance = float("inf")

        # Reset start state
        reset_fact(self.start_state)

        # Reset facts.
        for fact in self.facts.values():
            reset_fact(fact)

        # Reset operators.
        for operator in self.operators:
            operator.counter = len(operator.preconditions)

    def get_cost(
        self, operator: RelaxedOperator, pre: RelaxedFact
    ) -> tuple[set[str] | None, float]:
        """Calculate the cost of applying ``operator``.

        For hMax and hAdd nothing has to change here apart from the ``eval``
        function. hFF and hSA override this method.
        """
        if operator.preconditions:
            # Sum / maximize over the heuristic values of all preconditions.
            cost = self.eval(self.facts[pre].distance for pre in operator.preconditions)
        else:
            # An operator without preconditions has cost 0.
            cost = 0.0

        # The return value is a tuple because hSA returns the unioned set
        # instead of None.
        return None, cost + operator.cost

    def calc_goal_h(self) -> float:
        """Calculate the heuristic value of the whole goal.

        Like ``get_cost``, this uses the ``eval`` function and is overridden for
        hSA and hFF. Returns 0 if the goal is empty.
        """
        if self.goals:
            return self.eval(self.facts[fact].distance for fact in self.goals)
        else:
            return 0

    def finished(self, achieved_goals: set[str], queue: Heap) -> bool:
        """Return the stopping criterion for the Dijkstra search.

        The criterion differs between heuristics.
        """
        return achieved_goals == self.goals or not queue

    def dijkstra(self, queue: Heap) -> None:
        """Perform the Dijkstra forward pass.

        For efficiency reasons, this is used instead of an explicit graph
        representation of the problem.
        """
        # Stores the achieved subgoals. Needed for abortion criterion of hMax.
        achieved_goals: set[str] = set()
        while not self.finished(achieved_goals, queue):
            # Get the fact with the lowest heuristic value.
            (_dist, _tie, fact) = heapq.heappop(queue)
            # If this node is part of the goal, we add to the goal set, which
            # is used as an abort criterion.
            if fact.name in self.goals:
                achieved_goals.add(fact.name)
            # Check whether we already expanded this fact.
            if not fact.expanded:
                # Iterate over all operators this fact is a precondition of.
                for operator in fact.precondition_of:
                    # Decrease the precondition counter.
                    operator.counter -= 1
                    # Check whether all preconditions are True and we can apply
                    # this operator.
                    if operator.counter <= 0:
                        for n in operator.add_effects:
                            neighbor = self.facts[n]
                            # Calculate the cost of applying this operator.
                            (unioned_sets, tmp_dist) = self.get_cost(operator, fact)
                            if tmp_dist < neighbor.distance:
                                # If the new costs are cheaper, then the old
                                # costs, we change the neighbors heuristic
                                # values.
                                neighbor.distance = tmp_dist
                                neighbor.sa_set = unioned_sets
                                neighbor.cheapest_achiever = operator
                                # And push it on the queue.
                                heapq.heappush(
                                    queue, (tmp_dist, self.tie_breaker, neighbor)
                                )
                                self.tie_breaker += 1
                # Finally the fact is marked as expanded.
                fact.expanded = True


class hAddHeuristic(_RelaxationHeuristic):
    """The hAdd heuristic, which sums over the precondition costs."""

    def __init__(self, task: Task) -> None:
        # hAdd is the base heuristic with ``eval`` set to sum().
        super().__init__(task)
        self.eval = sum


class hMaxHeuristic(_RelaxationHeuristic):
    """The hMax heuristic, which maximizes over the precondition costs."""

    def __init__(self, task: Task) -> None:
        # hMax is the base heuristic with ``eval`` set to max().
        super().__init__(task)
        self.eval = max


class hSAHeuristic(_RelaxationHeuristic):
    """The hSA (set-additive) heuristic."""

    def get_cost(
        self, operator: RelaxedOperator, pre: RelaxedFact
    ) -> tuple[set[str] | None, float]:
        """Calculate the cost of applying ``operator``.

        hSA relies not only on a real-valued distance but also on the set of
        operators that have been applied, so this method is overridden.
        """
        # Initialize.
        cost = 0
        unioned_sets: set[str] = set() if pre.sa_set is None else pre.sa_set

        if operator.preconditions:
            # Collect the sa-sets from all preconditions in a list.
            sa_sets = [
                s
                for pre in operator.preconditions
                if (s := self.facts[pre].sa_set) is not None
            ]
            if sa_sets:
                # Union all these sets.
                unioned_sets = set.union(*sa_sets)
                # The heuristic value equals the cardinality of the unioned
                # sets.
                cost = len(unioned_sets)

        # Add the current operator to the set and return it together with the
        # heuristic value.
        unioned_sets.add(operator.name)
        return (unioned_sets, cost + operator.cost)

    def calc_goal_h(self) -> float:
        """Calculate the heuristic value of the whole goal.

        hSA relies not only on a real-valued distance but also on the set of
        operators that have been applied, so this method is overridden. Returns
        0 if the goal is empty.
        """
        if self.goals:
            # Collect the sa-sets of all facts that are part of the goal.
            sa_sets = [
                s for fact in self.goals if (s := self.facts[fact].sa_set) is not None
            ]
            # All subgoals fulfilled? Then the heuristic value is the size of
            # the union of their sa-sets; otherwise the goal is unreachable.
            if len(sa_sets) == len(self.goals):
                return len(set.union(*sa_sets))
            else:
                return float("inf")
        else:
            return 0


class hFFHeuristic(_RelaxationHeuristic):
    """The hFF (FF) heuristic, which uses the same forward pass as hAdd."""

    def __init__(self, task: Task) -> None:
        super().__init__(task)
        self.eval = sum

    def calc_h_with_plan(self, node: SearchNode) -> tuple[float, set[str] | None]:
        """Calculate the hFF value together with a relaxed plan."""
        state = node.state
        # Reset distance and set to default values.
        self.init_distance(state)

        # Construct the priority queue.
        heap: Heap = []
        for fact in state:
            # The order is determined by the distance of the facts.
            # As a tie breaker we use a simple counter.
            heapq.heappush(
                heap, (self.facts[fact].distance, self.tie_breaker, self.facts[fact])
            )
            self.tie_breaker += 1

        # Call the Dijkstra search that performs the forward pass.
        self.dijkstra(heap)
        return self.calc_goal_h(return_relaxed_plan=True)

    def calc_goal_h(self, return_relaxed_plan: bool = False) -> Any:
        """Calculate the heuristic value, which for hFF needs a backward pass."""
        relaxed_plan: set[str] = set()
        # Check whether we achieved all subgoals.
        hAdd_value = self.eval([self.facts[fact].distance for fact in self.goals])

        if hAdd_value < float("inf"):
            # Initialize a queue and push all goal nodes.
            q: list[RelaxedFact] = []
            closed_list: set[str] = set()
            for g in self.goals:
                q.append(self.facts[g])
                closed_list.add(g)

            # Do backward pass.
            while q:
                fact = q.pop()
                # Check whether this fact has a cheapest achiever and that it
                # is not already expanded
                if (
                    fact.cheapest_achiever is not None
                    and fact.cheapest_achiever not in relaxed_plan
                ):
                    # Add all preconditions of the cheapest achiever to the
                    # queue.
                    for pre in fact.cheapest_achiever.preconditions:
                        if pre not in closed_list:
                            q.append(self.facts[pre])
                            closed_list.add(pre)
                    relaxed_plan.add(fact.cheapest_achiever.name)

            # Extract FF value.
            if return_relaxed_plan:
                return len(relaxed_plan), relaxed_plan
            else:
                return len(relaxed_plan)

        else:
            if return_relaxed_plan:
                return float("inf"), None
            else:
                return float("inf")
