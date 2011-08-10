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
This module contains all data structures needed to represent a PDDL domain and
possibly a task definition.
"""


class Type:
    """
    This class represents a PDDL type.
    """
    def __init__(self, name, parent):
        self.name = name.lower()
        self.parent = parent

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Predicate:
    def __init__(self, name, signature):
        """
        name: The name of the predicate.
        signature: A list of tuples (name, [types]) to represent a list of
                   parameters and their type(s).
        """
        self.name = name
        self.signature = signature

    def __repr__(self):
        return self.name + str(self.signature)

    def __str__(self):
        return self.name + str(self.signature)


# Formula is unused right now!
#class Formula:
#    def __init__(self, operator, operands=[]):
#        # right now we only need AND
#        self._operator = operator # 'AND' | 'OR' | 'NOT'
#        self._operands = operands
#
#    def getOperator(self):
#        return self._operator
#    operator = property(getOperator)
#
#    def getOperands(self):
#        return self._operands
#    operands = property(getOperands)


class Effect:
    def __init__(self):
        """
        addlist: Set of predicates that have to be true after the action
        dellist: Set of predicates that have to be false after the action
        """
        self.addlist = set()
        self.dellist = set()


class Action:
    def __init__(self, name, signature, precondition, effect):
        """
        name: The name identifying the action
        signature: A list of tuples (name, [types]) to represent a list of
                   parameters an their type(s).
        precondition: A list of predicates that have to be true before the
                      action can be applied
        effect: An effect instance specifying the postcondition of the action
        """
        self.name = name
        self.signature = signature
        self.precondition = precondition
        self.effect = effect


class Domain:
    def __init__(self, name, types, predicates, actions, constants={}):
        """
        name: The name of the domain
        types: A dict of typename->Type instances in the domain
        predicates: A list of predicates in the domain
        actions: A list of actions in the domain
        constants: A dict of name->type pairs of the constants in the domain
        """
        self.name = name
        self.types = types
        self.predicates = predicates
        self.actions = actions
        self.constants = constants

    def __repr__(self):
        return ('< Domain definition: %s Predicates: %s Actions: %s '
                'Constants: %s >' % (self.name,
                                     [str(p) for p in self.predicates],
                                     [str(a) for a in self.actions],
                                     [str(c) for c in self.constants]))

    __str__ = __repr__


class Problem:
    def __init__(self, name, domain, objects, init, goal):
        """
        name: The name of the problem
        domain: The domain in which the problem has to be solved
        objects: A dict name->type of objects that are used in the problem
        init: A list of predicates describing the initial state
        goal: A list of predicates describing the goal state
        """
        self.name = name
        self.domain = domain
        self.objects = objects
        self.initial_state = init
        self.goal = goal

    def __repr__(self):
        return ('< Problem definition: %s '
                'Domain: %s Objects: %s Initial State: %s Goal State : %s >' %
                (self.name, self.domain.name,
                 [self.objects[o].name for o in self.objects],
                 [str(p) for p in self.initial_state],
                 [str(p) for p in self.goal]))

    __str__ = __repr__
