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
Classes and methods for grounding a schematic PDDL task to a STRIPS planning
task.
"""

import logging
import itertools
import re
from collections import defaultdict

from task import Task, Operator

# controls mass log output
verbose_logging = False


def ground(problem):
    """
    This is the main method that grounds the PDDL task and returns an
    instance of the task.Task class.

    @note Assumption: only PDDL problems with types at the moment.

    @param problem A pddl.Problem instance describing the parsed problem
    @return A task.Task instance with the grounded problem
    """

    """
    Overview of variable names in pddl.py, grounding.py and task.py:
    Problem.initial_state       -> init         -> Task.initial_state
    Problem.goal                -> goal         -> Task.goal
    Problem.domain.actions      -> operators    -> Task.operators
    Problem.domain.predicates   -> variables    -> Task.facts
    """
    domain = problem.domain
    actions = domain.actions.values()
    predicates = domain.predicates.values()

    # Objects
    objects = problem.objects
    objects.update(domain.constants)
    if verbose_logging:
        logging.debug('Objects:\n%s' % objects)

    # Get the names of the static predicates
    statics = _get_statics(predicates, actions)
    if verbose_logging:
        logging.debug("Static predicates:\n%s" % statics)

    # Create a map from types to objects
    type_map = _create_type_map(objects)
    if verbose_logging:
        logging.debug("Type to object map:\n%s" % type_map)

    # Transform initial state into a specific
    init = _get_partial_state(problem.initial_state)
    if verbose_logging:
        logging.debug("Initial state with statics:\n%s" % init)

    # Ground actions
    operators = _ground_actions(actions, type_map, statics, init)
    if verbose_logging:
        logging.debug('Operators:\n%s' % '\n'.join(map(str, operators)))

    # Ground goal
    # TODO: Remove facts that can only become true and are true in the
    #       initial state
    # TODO: Return simple unsolvable problem if goal contains a fact that can
    #       only become false and is false in the initial state
    goals = _get_partial_state(problem.goal)
    if verbose_logging:
        logging.debug("Goal:\n%s" % goals)

    # Collect facts from operators and include the ones from the goal
    facts = _collect_facts(operators) | goals
    if verbose_logging:
        logging.debug("All grounded facts:\n%s" % facts)

    # Remove statics from initial state
    init &= facts
    if verbose_logging:
        logging.debug("Initial state without statics:\n%s" % init)

    # perform relevance analysis
    operators = _relevance_analysis(operators, goals)

    name = problem.name
    return Task(name, facts, init, goals, operators)


def _relevance_analysis(operators, goals):
    """This implements a relevance analysis of operators.

    We start with all facts within the goal and iteratively compute
    a fixpoint of all relevant effects.
    Relevant effects are those that contribute to a valid path to the goal.
    """
    debug = True
    debug_pruned_op = set()

    relevant_facts = set()
    old_relevant_facts = set()
    changed = True
    for goal in goals:
        relevant_facts.add(goal)

    while changed:
        # set next relevant facts to current facts
        # if we do not add anything in the following for loop
        # we have already found a fixpoint
        old_relevant_facts = relevant_facts.copy()
        # compute cut of relevant facts with effects of all operators
        for op in operators:
            new_addlist = op.add_effects & relevant_facts
            new_dellist = op.del_effects & relevant_facts
            if new_addlist or new_dellist:
                # add all preconditions to relevant facts
                relevant_facts |= op.preconditions
        changed = old_relevant_facts != relevant_facts

    # delete all irrellevant effects
    del_operators = set()
    for op in operators:
        # calculate new effects
        new_addlist = op.add_effects & relevant_facts
        new_dellist = op.del_effects & relevant_facts
        if debug:
            debug_pruned_op |= op.add_effects - relevant_facts
            debug_pruned_op |= op.del_effects - relevant_facts
        # store new effects
        op.add_effects = new_addlist
        op.del_effects = new_dellist
        if not new_addlist and not new_dellist:
            if verbose_logging:
                logging.debug('Relevance analysis removed oparator %s' %
                              op.name)
            del_operators.add(op)
    if debug:
        logging.info('Relevance analysis removed %d facts' %
                     len(debug_pruned_op))
    # remove completely irrelevant operators
    return [op for op in operators if not op in del_operators]


def _get_statics(predicates, actions):
    """
    Determine all static predicates and return them as a list.

    We want to know the statics to avoid grounded actions with static
    preconditions violated. A static predicate is a predicate which
    doesn't occur in an effect of an action.
    """
    def get_effects(action):
        return action.effect.addlist | action.effect.dellist

    effects = [get_effects(action) for action in actions]
    effects = set(itertools.chain(*effects))

    def static(predicate):
        return not any(predicate.name == eff.name for eff in effects)

    statics = [pred.name for pred in predicates if static(pred)]
    return statics


def _create_type_map(objects):
    """
    Create a map from each type to its objects.

    For each object we know the type. This returns a dictionary
    from each type to a set of objects (of this type). We also
    have to care about type hierarchy. An object
    of a subtype is a specialization of a specific type. We have
    to put this object into the set of the supertype, too.
    """
    type_map = defaultdict(set)

    # for every type we append the corresponding object
    for object_name, object_type in objects.items():
        parent_type = object_type.parent
        while True:
            type_map[object_type].add(object_name)
            object_type, parent_type = parent_type, object_type.parent
            if parent_type is None:
            #if object_type is None:
                break

    # TODO sets in map should be ordered lists
    return type_map


def _collect_facts(operators):
    """
    Collect all facts from grounded operators (precondition, add
    effects and delete effects).
    """
    facts = set()
    for op in operators:
        facts |= op.preconditions | op.add_effects | op.del_effects
    return facts


def _ground_actions(actions, type_map, statics, init):
    """
    Ground a list of actions and return the resulting list of operators.

    @param actions: List of actions
    @param type_map: Mapping from type to objects of that type
    @param statics: Names of the static predicates
    @param init: Grounded initial state
    """
    op_lists = [_ground_action(action, type_map, statics, init)
                for action in actions]
    operators = list(itertools.chain(*op_lists))
    return operators


def _find_pred_in_init(pred_name, param, sig_pos, init):
    """
    This method is used to check whether an instantiation of the predicate
    denoted by pred_name with the parameter param at position sig_pos is
    present in the initial condition.

    Useful to evaluate static preconditions efficiently.
    """
    match_init = None
    if sig_pos == 0:
        match_init = re.compile('\(%s %s.*' % (pred_name, param))
    else:
        reg_ex = '\(%s\s+' % pred_name
        reg_ex += '[\w\d-]+\s+' * sig_pos
#        for i in xrange(sig_pos):
#            reg_ex += '[\w\d-]+\s+'
        reg_ex += '%s.*' % param
        match_init = re.compile(reg_ex)
    assert (match_init is not None)
    return any([match_init.match(string) for string in init])


def _ground_action(action, type_map, statics, init):
    """
    Ground the action and return the resulting list of operators.
    """
    logging.debug('Grounding %s' % action.name)
    param_to_objects = {}

    for param_name, param_types in action.signature:
        # List of sets of objects for this parameter
        objects = [type_map[type] for type in param_types]
        # Combine the sets into one set
        objects = set(itertools.chain(*objects))
        param_to_objects[param_name] = objects

    # For each parameter that is not constant,
    # remove all invalid static preconditions
    remove_debug = 0
    for param, objects in param_to_objects.items():
        for pred in action.precondition:
            # if a static predicate is present in the precondition
            if pred.name in statics:
                sig_pos = -1
                count = 0
                # check if there is an instantiation with the current parameter
                for var, _ in pred.signature:
                    if var == param:
                        sig_pos = count
                    count += 1
                if sig_pos != -1:
                    # remove if no instantiation present in initial state
                    obj_copy = objects.copy()
                    for o in obj_copy:
                        if not _find_pred_in_init(pred.name, o, sig_pos, init):
                            if verbose_logging:
                                remove_debug += 1
                            objects.remove(o)
    if verbose_logging:
        logging.info('Static precondition analysis removed %d possible objects'
                     % remove_debug)

    # save a list of possible assignment tuples (param_name, object)
    domain_lists = [[(name, obj) for obj in objects] for name, objects in
                    param_to_objects.items()]
    # Calculate all possible assignments
    assignments = itertools.product(*domain_lists)

    # Create a new operator for each possible assignment of parameters
    ops = [_create_operator(action, dict(assign), statics, init)
            for assign in assignments]
    # Filter out the None values
    ops = filter(bool, ops)

    return ops


def _create_operator(action, assignment, statics, init):
    """Create an operator for "action" and "assignment".

    Statics are handled here. True statics aren't added to the
    precondition facts of a grounded operator. If there is a false static
    in the ungrounded precondition, the operator won't be created.
    @param assignment: mapping from predicate name to object name
    """
    precondition_facts = set()
    for precondition in action.precondition:
        fact = _ground_atom(precondition, assignment)
        predicate_name = precondition.name
        if predicate_name in statics:
            # Check if this precondition is false in the initial state
            if fact not in init:
                # This precondition is never true -> Don't add operator
                return None
        else:
            # This precondition is not always true -> Add it
            precondition_facts.add(fact)

    add_effects = _ground_atoms(action.effect.addlist, assignment)
    del_effects = _ground_atoms(action.effect.dellist, assignment)
    # If the same fact is added and deleted by an operator the STRIPS formalism
    # adds it.
    del_effects -= add_effects
    # If a fact is present in the precondition, we do not have to add it.
    # Note that if a fact is in the delete and in the add effects,
    # it has already been deleted in the previous step.
    add_effects -= precondition_facts
    args = [assignment[name] for name, types in action.signature]
    name = _get_grounded_string(action.name, args)
    return Operator(name, precondition_facts, add_effects, del_effects)


def _get_grounded_string(name, args):
    """ We use the lisp notation (e.g. "(unstack c e)"). """
    args_string = ' ' + ' '.join(args) if args else ''
    return '(%s%s)' % (name, args_string)


def _ground_atom(atom, assignment):
    """
    Return a string with the grounded representation of "atom" with respect
    to "assignment".
    """
    names = []
    for name, types in atom.signature:
        if name in assignment:
            names.append(assignment[name])
        else:
            names.append(name)
    return _get_grounded_string(atom.name, names)


def _ground_atoms(atoms, assignment):
    """ Return a set of the grounded representation of the atoms. """
    return {_ground_atom(atom, assignment) for atom in atoms}


def _get_fact(atom):
    """ Return the string representation of the grounded atom. """
    args = [name for name, types in atom.signature]
    return _get_grounded_string(atom.name, args)


def _get_partial_state(atoms):
    """ Return a set of the string representation of the grounded atoms. """
    return frozenset(_get_fact(atom) for atom in atoms)
