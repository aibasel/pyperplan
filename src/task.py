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
Classes for representing a STRIPS planning task
"""


class Operator:
    """
    The preconditions represent the facts that have to be true
    before the operator can be applied.
    add_effects are the facts that the operator makes true.
    delete_effects are the facts that the operator makes false.
    """
    def __init__(self, name, preconditions, add_effects, del_effects):
        self.name = name
        self.preconditions = frozenset(preconditions)
        self.add_effects = frozenset(add_effects)
        self.del_effects = frozenset(del_effects)

    def applicable(self, state):
        """
        Operators are applicable when their set of preconditions is a subset
        of the facts that are true in "state".

        @return True if the operator's preconditions is a subset of the state,
                False otherwise
        """
        return self.preconditions <= state

    def apply(self, state):
        """
        Applying an operator means removing the facts that are made false
        by the operator from the set of true facts in state and adding
        the facts made true.

        Note that therefore it is possible to have operands that make a
        fact both false and true. This results in the fact being true
        at the end.

        @param state The state that the operator should be applied to
        @return A new state (set of facts) after the application of the
                operator
        """
        assert self.applicable(state)
        assert type(state) in (frozenset, set)
        return (state - self.del_effects) | self.add_effects

    def __str__(self):
        s = '%s\n' % self.name
        for group, facts in [('PRE', self.preconditions),
                             ('ADD', self.add_effects),
                             ('DEL', self.del_effects)]:
            for fact in facts:
                s += '  %s: %s\n' % (group, fact)
        return s

    def __repr__(self):
        return '<Op %s>' % self.name


class Task:
    """
    A STRIPS planning task
    """
    def __init__(self, name, facts, initial_state, goals, operators):
        """
        @param name The task's name
        @param facts A set of all the fact names that are valid in the domain
        @param initial_state A set of fact names that are true at the beginning
        @param goals A set of fact names that must be true to solve the problem
        @param operators A set of operator instances for the domain
        """
        self.name = name
        self.facts = facts
        self.initial_state = initial_state
        self.goals = goals
        self.operators = operators

    def goal_reached(self, state):
        """
        The goal has been reached if all facts that are true in "goals"
        are true in "state".

        @return True if all the goals are reached, False otherwise
        """
        return self.goals <= state

    def get_successor_states(self, state):
        """
        @return A list with (op, new_state) pairs where "op" is the applicable
        operator and "new_state" the state that results when "op" is applied
        in state "state".
        """
        return [(op, op.apply(state)) for op in self.operators
                if op.applicable(state)]

    def __str__(self):
        s = 'Task {0}\n  Vars:  {1}\n  Init:  {2}\n  Goals: {3}\n  Ops:   {4}'
        return s.format(self.name, ', '.join(self.facts),
                             self.initial_state, self.goals,
                             '\n'.join(map(repr, self.operators)))

    def __repr__(self):
        string = '<Task {0}, vars: {1}, operators: {2}>'
        return string.format(self.name, len(self.facts), len(self.operators))
