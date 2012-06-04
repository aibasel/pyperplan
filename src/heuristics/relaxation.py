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

from task import Operator, Task
from heuristics.heuristic_base import Heuristic
import heapq
import logging

""" This module contains the relaxation heuristics hAdd, hMax, hSA and hFF. """


class RelaxedFact:
    """This class represents a relaxed fact."""
    def __init__(self, name):
        """Construct a new relaxed fact.

        Keyword arguments:
        name -- the name of the relaxed fact.

        Member variables:
        name -- the name of the relaxed fact.
        precondition_of -- a list that contains all operators, this fact is a
                           precondition of.
        expanded -- stores whether this fact has been expanded during the
                    Dijkstra forward pass.
        distance -- stores the heuristic distance value
        sa_set -- stores a set of operators that have been applied to make this
                  fact True (only for hSA).
        cheapest_achiever -- stores the cheapest operator that was applied to
                             reach this fact (only for hFF).
        """
        self.name = name
        self.precondition_of = []
        self.expanded = False
        self.sa_set = None
        self.cheapest_achiever = None
        self.distance = float('inf')


class RelaxedOperator:
    """ This class represents a relaxed operator (no delete effects)."""
    def __init__(self, name, preconditions, add_effects):
        """Construct a new relaxed operator.

        Keyword arguments:
        name -- the name of the relaxed operator.
        preconditions -- the preconditions of this operator
        add_effects -- the add effects of this operator

        Member variables:
        name -- the name of the relaxed operator.
        preconditions -- the preconditions of this operator
        counter -- alternative method to check whether all preconditions are
                   True
        add_effects -- the add effects of this operator
        cost -- the cost for applying this operator
        """
        self.name = name
        self.preconditions = preconditions
        self.add_effects = add_effects
        self.cost = 1
        self.counter = len(preconditions)


class _RelaxationHeuristic(Heuristic):
    """This class is the base class for all relaxation heuristics.

    It is not meant to be instantiated. Nevertheless it is in principle an
    implementation of the hAdd heuristic.
    """
    def __init__(self, task):
        """Construct a instance of _RelaxationHeuristic.

        Keyword arguments:
        task -- an instance of the Task class.

        Member variables:
        facts -- a dict that maps from fact names to fact objects
        operators -- a list of operators
        init -- the set of facts that define the initial state
        goals -- the set of facts that define the goal state
        tie_breaker -- a tie breaker needed for qeueing
        eval -- a function that is used to evaluate the cost of applying an
                operator
        """
        self.facts = dict()
        self.operators = []
        self.goals = task.goals
        self.init = task.initial_state
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
                # We add this operator to the precondtion_of list of the start
                # state. This way it can be applied to the start state. This
                # helps also when the initial state is empty.
                self.start_state.precondition_of.append(ro)

    def __call__(self, node):
        """This function is called whenever the heuristic needs to be computed.

        Keyword arguments:
        node -- the current state
        """
        state = node.state
        state = set(state)

        # Reset distance and set to default values.
        self.init_distance(state)

        # Construct the priority queue.
        heap = []
        # Add a dedicated start state, to cope with operators without
        # preconditions and empty initial state.
        heapq.heappush(heap, (0, self.tie_breaker, self.start_state))
        self.tie_breaker += 1

        for fact in state:
            # Its order is determined by the distance the facts.
            # As a tie breaker we use a simple counter.
            heapq.heappush(heap, (self.facts[fact].distance, self.tie_breaker,
                                  self.facts[fact]))
            self.tie_breaker += 1

        # Call the Dijkstra search that performs the forward pass.
        self.dijkstra(heap)

        # Extract the goal heuristic.
        h_value = self.calc_goal_h()

        return h_value

    def init_distance(self, state):
        """
        This function resets all member variables that store information that
        needs to be recomputed for each call of the heuristic.
        """
        def reset_fact(fact):
            fact.expanded = False
            fact.cheapest_achiever = None
            if fact.name in state:
                fact.distance = 0
                fact.sa_set = set()
            else:
                fact.sa_set = None
                fact.distance = float('inf')
        # Reset start state
        reset_fact(self.start_state)

        # Reset facts.
        for fact in self.facts.values():
            reset_fact(fact)

        # Reset operators.
        for operator in self.operators:
            operator.counter = len(operator.preconditions)

    def get_cost(self, operator, pre):
        """This function calculated the cost of applying an operator.

        For hMax and hAdd this nothing has to be changed here, but to use
        different functions for eval. hFF and hSA overwrite this function.
        """

        if operator.preconditions:
            # If this operator has preconditions, we sum / maximize over the
            # heuristic values of all preconditions.
            cost = self.eval([self.facts[pre].distance
                              for pre in operator.preconditions])
        else:
            # If there are no preconditions for this operator, its cost is 0.
            cost = 0

        # The return value is a tuple, because in hSA instead of None, the
        # unioned set is returned.
        return None, cost + operator.cost

    def calc_goal_h(self):
        """This function calculates the heuristic value of the whole goal.

        As get_cost, it is makes use of the eval function, and has to be
        overwritten for hSA and hFF.
        If the goal is empty: Return 0
        """
        if self.goals:
            return self.eval([self.facts[fact].distance
                              for fact in self.goals])
        else:
            return 0

    def finished(self, achieved_goals, queue):
        """
        This function is used as a stopping criterion for the Dijkstra search,
        which differs for different heuristics.
        """
        return achieved_goals == self.goals or not queue

    def dijkstra(self, queue):
        """This function is an implementation of a Dijkstra search.

        For efficiency reasons, it is used instead of an explicit graph
        representation of the problem.
        """
        # Stores the achieved subgoals. Needed for abortion criterion of hMax.
        achieved_goals = set()
        while not self.finished(achieved_goals, queue):
            # Get the fact with the lowest heuristic value.
            (dist, tie, fact) = heapq.heappop(queue)
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
                            (unioned_sets, tmp_dist) = self.get_cost(operator,
                                                                     fact)
                            if tmp_dist < neighbor.distance:
                                # If the new costs are cheaper, then the old
                                # costs, we change the neighbors heuristic
                                # values.
                                neighbor.distance = tmp_dist
                                neighbor.sa_set = unioned_sets
                                neighbor.cheapest_achiever = operator
                                # And push it on the queue.
                                heapq.heappush(queue, (tmp_dist,
                                                       self.tie_breaker,
                                                       neighbor))
                                self.tie_breaker += 1
                # Finally the fact is marked as expanded.
                fact.expanded = True


class hAddHeuristic(_RelaxationHeuristic):
    """This class is an implementation of the hADD heuristic.

    It derives from the _RelaxationHeuristic class.
    """
    def __init__(self, task):
        """
        To make this class an implementation of hADD, apart from deriving from
        _RelaxationHeuristic,  we only need to set eval to sum().
        """
        super().__init__(task)
        self.eval = sum


class hMaxHeuristic(_RelaxationHeuristic):
    """This class is an implementation of the hMax heuristic.

    It derives from the _RelaxationHeuristic class.
    """
    def __init__(self, task):
        """
        To make this class an implementation of hADD, apart from deriving from
        _RelaxationHeuristic, we only need to set eval to max().
        """
        super().__init__(task)
        self.eval = max


class hSAHeuristic(_RelaxationHeuristic):
    """This class is an implementation of the hSA heuristic.

    It derives from the _RelaxationHeuristic class.
    """
    def get_cost(self, operator, pre):
        """
        This function has to be overwritten, because the hSA heuristic not
        only relies on a real valued distance, but also on a set of operators
        that have been applied.
        """
        # Initialize.
        cost = 0
        if pre.sa_set is None:
            unioned_sets = set()
        else:
            unioned_sets = pre.sa_set

        if operator.preconditions:
            # Collect the sa-sets from all preconditions in a list.
            l = [self.facts[pre].sa_set for pre in operator.preconditions
                 if self.facts[pre].sa_set is not None]
            if l:
                # Union all these sets.
                unioned_sets = set.union(*l)
                # The heuristic value equals the cardinality of the unioned
                # sets.
                cost = len(unioned_sets)

        # Add the current operator to the set and return it together with the
        # heuristic value.
        unioned_sets.add(operator.name)
        return (unioned_sets, cost + operator.cost)

    def calc_goal_h(self):
        """
        This function has to be overwritten, because the hSA heuristic not only
        relies on a real valued distance, but also on a set of operators that
        have been applied.

        Return 0 if the goal is empty
        """
        if self.goals:
            # Collect the sa-sets of all facts that are part of the goal.
            l = [self.facts[fact].sa_set for fact in self.goals
                 if self.facts[fact].sa_set is not None]
            # Check whether all subgoals are fulfilled.
            if len(l) == len(self.goals):
                # Union all these sets and take the length of the union as
                # heuristic value.
                h_value = len(set.union(*l))
            else:
                # Ff not, return infinty.
                h_value = float('inf')
            return h_value
        else:
            return 0


class hFFHeuristic(_RelaxationHeuristic):
    """ This class is an implementation of the hFF heuristic.

    It derives from the _RelaxationHeuristic class.
    """
    def __init__(self, task):
        """Construct a hFFHeuristic.

        FF uses same forward pass as hAdd.
        """
        super().__init__(task)
        self.eval = sum

    def calc_h_with_plan(self, node):
        """
        Helper method to calculate hFF value together with a relaxed plan.
        """
        state = node.state
        state = set(state)
        # Reset distance and set to default values.
        self.init_distance(state)
        # reset dead end status

        # Construct the priority queue.
        heap = []
        for fact in state:
            # Its order is determined by the distance the facts.
            # As a tie breaker we use a simple counter.
            heapq.heappush(heap, (self.facts[fact].distance, self.tie_breaker,
                                  self.facts[fact]))
            self.tie_breaker += 1

        # Call the Dijkstra search that performs the forward pass.
        self.dijkstra(heap)
        h_value = self.calc_goal_h(True)

        if type(h_value) is tuple:
            return h_value[0], h_value[1]
        else:
            return h_value

    def calc_goal_h(self, return_relaxed_plan=False):
        """
        This function has to be overwritten, because the hFF heuristic needs an
        additional backward pass.
        """
        relaxed_plan = set()
        # Check whether we achieved all subgoals.
        hAdd_value = self.eval([self.facts[fact].distance
                                for fact in self.goals])

        if hAdd_value < float('inf'):
            # Initialize a queue and push all goal nodes.
            q = []
            closed_list = set()
            for g in self.goals:
                q.append(self.facts[g])
                closed_list.add(g)

            # Do backward pass.
            while q:
                fact = q.pop()
                # Check whether this fact has a cheapest achiever and that it
                # is not already expanded
                if (fact.cheapest_achiever is not None and
                    not fact.cheapest_achiever in relaxed_plan):
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
                return float('inf'), None
            else:
                return float('inf')
