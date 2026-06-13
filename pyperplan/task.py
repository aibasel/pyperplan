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

"""Classes for representing a STRIPS planning task."""


class Operator:
    """An action that transforms one state into another.

    The preconditions are the facts that have to be true before the operator
    can be applied. The add effects are the facts that the operator makes true,
    the delete effects the facts that it makes false.
    """

    def __init__(self, name, preconditions, add_effects, del_effects):
        self.name = name
        self.preconditions = frozenset(preconditions)
        self.add_effects = frozenset(add_effects)
        self.del_effects = frozenset(del_effects)

    def applicable(self, state):
        """Return whether the operator can be applied in ``state``.

        An operator is applicable when its preconditions are a subset of the
        facts that are true in ``state``.
        """
        return self.preconditions <= state

    def apply(self, state):
        """Return the state that results from applying the operator in ``state``.

        Applying an operator removes its delete effects from the set of true
        facts and adds its add effects. A fact that appears in both effects is
        therefore true in the resulting state.
        """
        assert self.applicable(state)
        assert isinstance(state, (set, frozenset))
        return (state - self.del_effects) | self.add_effects

    def __eq__(self, other):
        return (
            self.name == other.name
            and self.preconditions == other.preconditions
            and self.add_effects == other.add_effects
            and self.del_effects == other.del_effects
        )

    def __hash__(self):
        return hash((self.name, self.preconditions, self.add_effects, self.del_effects))

    def __str__(self):
        s = f"{self.name}\n"
        for group, facts in [
            ("PRE", self.preconditions),
            ("ADD", self.add_effects),
            ("DEL", self.del_effects),
        ]:
            for fact in facts:
                s += f"  {group}: {fact}\n"
        return s

    def __repr__(self):
        return f"<Op {self.name}>"


class Task:
    """A STRIPS planning task."""

    def __init__(self, name, facts, initial_state, goals, operators):
        """
        name: The task's name.
        facts: A set of all the fact names that are valid in the domain.
        initial_state: A set of fact names that are true at the beginning.
        goals: A set of fact names that must be true to solve the problem.
        operators: A set of operator instances for the domain.
        """
        self.name = name
        self.facts = facts
        self.initial_state = initial_state
        self.goals = goals
        self.operators = operators

    def goal_reached(self, state):
        """Return whether ``state`` satisfies all of the task's goals.

        The goal has been reached once every fact in ``goals`` is true in
        ``state``.
        """
        return self.goals <= state

    def get_successor_states(self, state):
        """Return the ``(operator, successor_state)`` pairs reachable from ``state``.

        Each pair consists of an operator applicable in ``state`` and the state
        that results from applying it.
        """
        return [(op, op.apply(state)) for op in self.operators if op.applicable(state)]

    def __str__(self):
        operators = "\n".join(map(repr, self.operators))
        return (
            f"Task {self.name}\n"
            f"  Vars:  {', '.join(self.facts)}\n"
            f"  Init:  {self.initial_state}\n"
            f"  Goals: {self.goals}\n"
            f"  Ops:   {operators}"
        )

    def __repr__(self):
        return (
            f"<Task {self.name}, vars: {len(self.facts)}, "
            f"operators: {len(self.operators)}>"
        )
