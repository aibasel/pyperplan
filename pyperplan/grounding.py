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

import itertools
import logging
from collections import defaultdict

from .task import Operator, Task

# controls mass log output
verbose_logging = False


def ground(
    problem, remove_statics_from_initial_state=True, remove_irrelevant_operators=True
):
    """Ground the PDDL ``problem`` and return a ``task.Task`` instance.

    Note: only typed PDDL problems are supported at the moment.

    Overview of corresponding variable names in pddl.py, grounding.py and
    task.py::

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
        logging.debug(f"Objects:\n{objects}")

    # Get the names of the static predicates
    statics = _get_statics(predicates, actions)
    if verbose_logging:
        logging.debug(f"Static predicates:\n{statics}")

    # Create a map from types to objects
    type_map = _create_type_map(objects)
    if verbose_logging:
        logging.debug(f"Type to object map:\n{type_map}")

    # Transform initial state into a specific
    init = _get_partial_state(problem.initial_state)
    if verbose_logging:
        logging.debug(f"Initial state with statics:\n{init}")

    # Ground actions
    operators = _ground_actions(actions, type_map, statics, init)
    if verbose_logging:
        operator_str = "\n".join(map(str, operators))
        logging.debug(f"Operators:\n{operator_str}")

    # Ground goal
    # TODO: Remove facts that can only become true and are true in the
    #       initial state
    # TODO: Return simple unsolvable problem if goal contains a fact that can
    #       only become false and is false in the initial state
    goals = _get_partial_state(problem.goal)
    if verbose_logging:
        logging.debug(f"Goal:\n{goals}")

    # Collect facts from operators and include the ones from the goal
    facts = _collect_facts(operators) | goals
    if verbose_logging:
        logging.debug(f"All grounded facts:\n{facts}")

    # Remove statics from initial state
    if remove_statics_from_initial_state:
        init &= facts
        if verbose_logging:
            logging.debug(f"Initial state without statics:\n{init}")

    # Perform relevance analysis
    if remove_irrelevant_operators:
        operators = _relevance_analysis(operators, goals)

    return Task(problem.name, facts, init, goals, operators)


def _relevance_analysis(operators, goals):
    """Drop operators and effects that cannot contribute to reaching the goal.

    Starting from the goal facts, we iteratively compute a fixpoint of all
    relevant facts: a fact is relevant if it is a goal or a precondition of an
    operator that has at least one relevant effect. Effects on irrelevant facts
    are removed, and operators left without any effect are pruned entirely.
    """
    relevant_facts = set(goals)
    changed = True
    while changed:
        old_relevant_facts = relevant_facts.copy()
        for op in operators:
            if (op.add_effects | op.del_effects) & relevant_facts:
                relevant_facts |= op.preconditions
        changed = old_relevant_facts != relevant_facts

    relevant_operators = []
    for op in operators:
        op.add_effects &= relevant_facts
        op.del_effects &= relevant_facts
        if op.add_effects or op.del_effects:
            relevant_operators.append(op)
        elif verbose_logging:
            logging.debug(f"Relevance analysis removed operator {op.name}")

    return relevant_operators


def _get_statics(predicates, actions):
    """Determine the static predicates and return their names as a set.

    Knowing the statics lets us avoid grounding actions whose static
    preconditions are violated. A predicate is static if it does not occur in
    any action's effects.

    Returning a set keeps the ``in statics`` checks during grounding O(1).
    """
    effect_names = {
        effect.name
        for action in actions
        for effect in action.effect.addlist | action.effect.dellist
    }
    return {pred.name for pred in predicates if pred.name not in effect_names}


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

    # Add each object to its type and to all of that type's supertypes.
    for object_name, object_type in objects.items():
        while object_type is not None:
            type_map[object_type].add(object_name)
            object_type = object_type.parent

    # TODO: sets in map should be ordered lists
    return type_map


def _collect_facts(operators):
    """
    Collect all facts from grounded operators (precondition, add
    effects and delete effects).
    """
    facts = set()
    for op in operators:
        facts.update(op.preconditions, op.add_effects, op.del_effects)
    return facts


def _ground_actions(actions, type_map, statics, init):
    """Ground all ``actions`` and return the resulting list of operators.

    type_map: Mapping from type to objects of that type.
    statics: Names of the static predicates.
    init: Grounded initial state.
    """
    init_index = _index_init(init)
    op_lists = [
        _ground_action(action, type_map, statics, init, init_index)
        for action in actions
    ]
    return list(itertools.chain(*op_lists))


def _index_init(init):
    """Index the initial state by ``(predicate, argument position, object)``.

    Static-precondition analysis can then check in constant time whether the
    initial state contains a given predicate with a given object at a given
    argument position, instead of scanning all facts for each query.
    """
    index = set()
    for fact in init:
        # A grounded fact looks like "(predicate obj0 obj1 ...)".
        name, *args = fact[1:-1].split()
        for position, obj in enumerate(args):
            index.add((name, position, obj))
    return index


def _ground_action(action, type_map, statics, init, init_index=None):
    """Ground ``action`` and return the resulting list of operators."""
    logging.debug(f"Grounding {action.name}")
    if init_index is None:
        init_index = _index_init(init)
    param_to_objects = {}

    for param_name, param_types in action.signature:
        # Combine the objects of all types of this parameter into one set.
        objects = set(itertools.chain.from_iterable(type_map[t] for t in param_types))
        param_to_objects[param_name] = objects

    # For each parameter, drop objects that violate a static precondition.
    removed_objects = 0
    for param, objects in param_to_objects.items():
        for pred in action.precondition:
            if pred.name not in statics:
                continue
            # Find the position at which the parameter occurs in the predicate.
            sig_pos = -1
            for pos, (var, _) in enumerate(pred.signature):
                if var == param:
                    sig_pos = pos
            if sig_pos != -1:
                # Keep only objects for which an instantiation exists in init.
                valid = {o for o in objects if (pred.name, sig_pos, o) in init_index}
                removed_objects += len(objects) - len(valid)
                objects.intersection_update(valid)
    if verbose_logging:
        logging.info(
            f"Static precondition analysis removed {removed_objects} possible objects"
        )

    # List the possible (param_name, object) assignments for each parameter.
    domain_lists = [
        [(name, obj) for obj in objects] for name, objects in param_to_objects.items()
    ]

    # Create an operator for each possible assignment, dropping invalid ones.
    operators = [
        _create_operator(action, dict(assignment), statics, init)
        for assignment in itertools.product(*domain_lists)
    ]
    return [op for op in operators if op is not None]


def _create_operator(action, assignment, statics, init):
    """Create an operator for ``action`` and ``assignment``.

    Statics are handled here. True statics aren't added to the precondition
    facts of a grounded operator. If there is a false static in the ungrounded
    precondition, the operator won't be created.

    assignment: mapping from parameter name to object name.
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
    """We use the lisp notation (e.g. "(unstack c e)")."""
    args_string = " " + " ".join(args) if args else ""
    return f"({name}{args_string})"


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
    """Return a set of the grounded representation of the atoms."""
    return {_ground_atom(atom, assignment) for atom in atoms}


def _get_fact(atom):
    """Return the string representation of the grounded atom."""
    args = [name for name, types in atom.signature]
    return _get_grounded_string(atom.name, args)


def _get_partial_state(atoms):
    """Return a set of the string representation of the grounded atoms."""
    return frozenset(_get_fact(atom) for atom in atoms)
