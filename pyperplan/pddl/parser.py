#!/usr/bin/python3
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

"""The main parser logic.

A partial parser is implemented for each AST node, and these are called
recursively to construct a complete parse.
"""

from .lisp_parser import parse_lisp_iterator
from .parser_common import reserved
from .tree_visitor import TraversePDDLDomain, TraversePDDLProblem, Visitable

# This emulates a C/C++ enum to distinguish between formulas, variables and
# constants in formulas.
(TypeFormula, TypeVariable, TypeConstant) = range(3)

###
### Definitions of AST nodes
###


class Keyword(Visitable):
    """AST node for a PDDL keyword."""

    def __init__(self, name):
        # ``name`` is the keyword without its colon, e.g. 'typed' for ':typed'.
        self._visitor_name = "visit_keyword"
        self.name = name


class Variable(Visitable):
    """AST node for a PDDL variable."""

    def __init__(self, name, types=None):
        """
        name: the name of the variable, e.g. 'x' for '?x'.
        types: a list of names of the possible types of this variable, or None.
            Whether these types exist is checked later by the TreeVisitor.
        """
        self._visitor_name = "visit_variable"
        self.name = name
        self.typed = types is not None
        self.types = types


class Type(Visitable):
    """AST node for a PDDL type."""

    def __init__(self, name, parent=None):
        # ``parent`` is the name of the parent type, or None.
        self._visitor_name = "visit_type"
        self.name = name
        self.parent = parent


class Predicate(Visitable):
    """AST node for a PDDL predicate."""

    def __init__(self, name, parameters=None):
        # ``parameters`` is a list of Variables.
        self._visitor_name = "visit_predicate"
        self.name = name
        self.parameters = parameters or []


class PredicateInstance(Visitable):
    """AST node for a PDDL predicate instance."""

    def __init__(self, name, parameters=None):
        # ``parameters`` is a list of object names.
        self._visitor_name = "visit_predicate_instance"
        self.name = name
        self.parameters = parameters or []


class RequirementsStmt(Visitable):
    """AST node for a PDDL requirements statement."""

    def __init__(self, keywords=None):
        # ``keywords`` is the list of requirements, represented as Keywords.
        self._visitor_name = "visit_requirements_stmt"
        self.keywords = keywords or []


class DomainStmt(Visitable):
    """AST node for a PDDL domain statement (the domain name)."""

    def __init__(self, name):
        self._visitor_name = "visit_domain_stmt"
        self.name = name


class PreconditionStmt(Visitable):
    """AST node for a PDDL action precondition."""

    def __init__(self, formula):
        # ``formula`` is the parsed Formula. Arbitrary formulas are allowed
        # here; STRIPS compatibility is checked later by the TreeVisitor.
        self._visitor_name = "visit_precondition_stmt"
        self.formula = formula


class EffectStmt(Visitable):
    """AST node for a PDDL action effect."""

    def __init__(self, formula):
        # ``formula`` is the parsed Formula. Arbitrary formulas are allowed
        # here; STRIPS compatibility is checked later by the TreeVisitor.
        self._visitor_name = "visit_effect_stmt"
        self.formula = formula


class Formula(Visitable):
    """AST node for a PDDL formula, as used in preconditions and effects."""

    def __init__(self, key, children=None, type=TypeFormula):
        """
        key: the operator of the subformula, e.g. 'not' for '(not (on a c))'.
        children: a list of immediate descending subformulas.
        type: the type of the key, one of TypeFormula, TypeVariable or
            TypeConstant.
        """
        self._visitor_name = "visit_formula"
        self.key = key
        self.children = children or []
        self.type = type


class ActionStmt(Visitable):
    """AST node for a PDDL action."""

    def __init__(self, name, parameters, precond, effect):
        """
        parameters: a list of Variables denoting the parameters.
        precond: the precondition of the action, given as a Formula.
        effect: the effect of the action, given as a Formula.
        """
        self._visitor_name = "visit_action_stmt"
        self.name = name
        self.parameters = parameters
        self.precond = precond
        self.effect = effect


class PredicatesStmt(Visitable):
    """AST node for a PDDL domain predicates definition."""

    def __init__(self, predicates):
        # ``predicates`` is a list of Predicates.
        self._visitor_name = "visit_predicates_stmt"
        self.predicates = predicates


class DomainDef(Visitable):
    """AST node for a PDDL domain."""

    def __init__(
        self,
        name,
        requirements=None,
        types=None,
        predicates=None,
        actions=None,
        constants=None,
    ):
        """
        name: the domain name.
        requirements: a RequirementsStmt.
        types: a list of Type AST nodes.
        predicates: a PredicatesStmt.
        actions: a list of ActionStmt AST nodes.
        constants: a list of constants, as Object AST nodes.
        """
        self._visitor_name = "visit_domain_def"
        self.name = name
        self.requirements = requirements
        self.types = types
        self.predicates = predicates
        self.actions = [] if actions is None else actions
        self.constants = constants


class ProblemDef(Visitable):
    """AST node for a PDDL problem."""

    def __init__(self, name, domain_name, objects=None, init=None, goal=None):
        """
        name: the problem name.
        domain_name: the name of the domain this problem belongs to.
        objects: a list of objects defined in the problem file.
        init: an initial condition represented by an InitStmt.
        goal: a goal condition represented by a GoalStmt.
        """
        self._visitor_name = "visit_problem_def"
        self.name = name
        self.domain_name = domain_name
        self.objects = objects
        self.init = init
        self.goal = goal


class Object(Visitable):
    """AST node for a PDDL object."""

    def __init__(self, name, type):
        # ``type`` is the name of this object's type.
        self._visitor_name = "visit_object"
        self.name = name
        self.type_name = type


class InitStmt(Visitable):
    """AST node for a PDDL problem initial condition."""

    def __init__(self, predicates):
        # ``predicates`` is a list of predicates denoting the initial condition.
        self._visitor_name = "visit_init_stmt"
        self.predicates = predicates


class GoalStmt(Visitable):
    """AST node for a PDDL problem goal condition."""

    def __init__(self, formula):
        # ``formula`` is the Formula denoting the goal condition.
        self._visitor_name = "visit_goal_stmt"
        self.formula = formula


###
### some little helper functions
###


def parse_name(iterator, father):
    if not iterator.peek().is_word():
        raise ValueError(f"Error {father} predicate statement must contain a name!")
    return next(iterator).get_word()


def parse_list_template(f, iterator):
    """This function implements a common pattern used in this parser.

    It tries to parse a list of 'f' objects from the string 'string[i:end]'.
    The 'f' objects must be separated by whitespace.
    Returns a tuple of the position after the parsed list and the list.
    """
    result = []
    # Parse all possible occurrences up to the end of the substring.
    for elem in iterator:
        var = f(elem)
        if var is not None:
            result.append(var)
    return result


def _parse_string_helper(iterator):
    return iterator.get_word()


def _parse_type_helper(iterator, type_class):
    """This function implements another common idiom used in this parser.

    It parses a list consisting either of Objects or Variables or Types
    which can all have additional type inheritance information.
    A list of objects could for example be defined as:
    o1 o2 o3 o4 - car
    Which would represent 4 objects (o1-o4) of type car.
    Since Variable- and Typelists are specified using the same pattern for
    type/supertype information this function takes the 'type_class' as an
    argument and parses an appropriate list of type_class instances.

    Returns the parsed list of instances.
    """
    # There may be several objects with the same type, hence we store each
    # parsed object in a list and attach a new type instance whenever a type is
    # specified.
    result = []
    tmp_list = []
    while not iterator.empty():
        var = next(iterator).get_word()
        if type_class != Variable and len(var) > 0 and var[0] in reserved:
            raise ValueError("Error type must not begin with reserved char!")
        elif var == "-":
            # check if either definition present
            if iterator.peek().is_structure():
                # must contain either definition
                types_iter = next(iterator)
                if not types_iter.try_match("either"):
                    raise ValueError(
                        'Error multiple parent definition must start with "either"'
                    )
                tlist = parse_list_template(_parse_string_helper, types_iter)
                while tmp_list:
                    result.append(type_class(tmp_list.pop(), tlist))
            else:
                # Found type information, so flush objects into the result list.
                ctype = next(iterator).get_word()
                while tmp_list:
                    if type_class == Variable:
                        result.append(type_class(tmp_list.pop(), [ctype]))
                    else:
                        result.append(type_class(tmp_list.pop(), ctype))
        elif var is not None and var != "":
            # Found a new object definition, so enqueue it.
            if type_class == Variable and var[0] != "?":
                raise ValueError('Error variables must start with a "?"')
            tmp_list.insert(0, var)
    while tmp_list:
        # Append all left-over objects; these are untyped.
        result.append(type_class(tmp_list.pop(), None))
    return result


###
### parser functions
###


def parse_keyword(iterator):
    """Parse a keyword and return a Keyword instance."""
    name = iterator.get_word()
    if name == "":
        raise ValueError("Error empty keyword found")
    # Keywords have to start with a colon.
    if name[0] != ":":
        raise ValueError('Error keywords have to start with a colon ":"')
    return Keyword(name[1:])


def parse_keyword_list(iterator):
    """Parse a list of keywords and return it."""
    return parse_list_template(parse_keyword, iterator)


def parse_variable(iterator):
    """Parse a Variable and return it."""
    name = iterator.get_word()
    if name == "":
        raise ValueError("Error empty variable found")
    # Variables have to start with a question mark.
    if name[0] != "?":
        raise ValueError('Error variables must start with a "?"')
    return Variable(name, None)


def parse_typed_var_list(iterator):
    """Parse a list of (possibly typed) variables and return it."""
    return _parse_type_helper(iterator, Variable)


def parse_parameters(iterator):
    """Parse an action's parameter list and return it."""
    if not iterator.try_match(":parameters"):
        raise ValueError('Error keyword ":parameters" required before parameter list!')
    return parse_typed_var_list(next(iterator))


def parse_requirements_stmt(iterator):
    """Parse the PDDL requirements definition and return a RequirementsStmt."""
    if not iterator.try_match(":requirements"):
        raise ValueError('Error requirements list must contain keyword ":requirements"')
    keywords = parse_keyword_list(iterator)
    return RequirementsStmt(keywords)


def _parse_types_with_error(iterator, keyword, classt):
    if not iterator.try_match(keyword):
        raise ValueError(
            f'Error keyword "{keyword}" required before {classt.__name__}!'
        )
    return _parse_type_helper(iterator, classt)


# Constants / Objects and types can be parsed in the same way because of their
# similar structure, so we delegate to _parse_types_with_error.
def parse_types_stmt(iterator):
    return _parse_types_with_error(iterator, ":types", Type)


def parse_objects_stmt(iterator):
    return _parse_types_with_error(iterator, ":objects", Object)


def parse_constants_stmt(iterator):
    return _parse_types_with_error(iterator, ":constants", Object)


def _parse_domain_helper(iterator, keyword):
    """Parse the domain statement (the domain name) and return a DomainStmt."""
    if not iterator.try_match(keyword):
        raise ValueError("Error domain statement must be present before domain name!")
    name = parse_name(iterator, "domain")
    return DomainStmt(name)


def parse_domain_stmt(iterator):
    return _parse_domain_helper(iterator, "domain")


def parse_problem_domain_stmt(iterator):
    return _parse_domain_helper(iterator, ":domain")


def parse_predicate(iterator):
    """Parse a predicate (its name and typed-variable signature).

    Returns a Predicate instance.
    """
    name = parse_name(iterator, "predicate")
    params = parse_typed_var_list(iterator)
    return Predicate(name, params)


def parse_predicate_list(iterator):
    """Parse a list of predicates and return it."""
    return parse_list_template(parse_predicate, iterator)


def parse_predicate_instance(iterator):
    """Parse a predicate instance (a predicate with a possibly instantiated
    signature) and return a PredicateInstance.
    """
    name = parse_name(iterator, "domain")
    params = parse_list_template(_parse_string_helper, iterator)
    return PredicateInstance(name, params)


def parse_predicate_instance_list(iterator):
    """Parse a list of predicate instances and return it."""
    return parse_list_template(parse_predicate_instance, iterator)


def parse_formula(iterator):
    """Parse a Formula recursively and return it."""
    if iterator.is_structure():
        # This is a nested formula.
        type = TypeFormula
        key = iterator.peek().get_word()
        next(iterator)
        if key[0] in reserved:
            raise ValueError("Error: Formula must not start with reserved char!")
        children = parse_list_template(parse_formula, iterator)
    else:
        # This is a non-nested formula.
        key = iterator.get_word()
        children = []
        if key[0] == "?":
            key = parse_variable(iterator)
            type = TypeVariable
        else:
            type = TypeConstant
    return Formula(key, children, type)


def _parse_precondition_or_effect(iterator, keyword, type):
    """Parse an action precondition or effect.

    Returns a PreconditionStmt or EffectStmt instance.
    """
    if not iterator.try_match(keyword):
        raise ValueError(f'Error: {type.__name__} must start with "{keyword}" keyword')
    cond = parse_formula(next(iterator))
    return type(cond)


def parse_precondition_stmt(iterator):
    return _parse_precondition_or_effect(iterator, ":precondition", PreconditionStmt)


def parse_effect_stmt(iterator):
    return _parse_precondition_or_effect(iterator, ":effect", EffectStmt)


def parse_action_stmt(iterator):
    """
    Parse an action definition which consists of a name, parameters a
    precondition and an effect.

    Returns an ActionStmt instance.
    """
    # each action begins with a name
    if not iterator.try_match(":action"):
        raise ValueError('Error: action must start with ":action" keyword!')
    name = parse_name(iterator, "action")
    # call parsers to parse parameters, precondition, effect
    param = parse_parameters(iterator)
    pre = parse_precondition_stmt(iterator)
    eff = parse_effect_stmt(iterator)
    return ActionStmt(name, param, pre, eff)


def parse_predicates_stmt(iterator):
    """
    Parse a PredicatesStmt which is essentially a list of predicates preceded
    by the ':predicates' keyword.

    Returns a PredicatesStmt instance
    """
    if not iterator.try_match(":predicates"):
        raise ValueError(
            'Error predicate definition must start with ":predicates" keyword!'
        )
    preds = parse_predicate_list(iterator)
    return PredicatesStmt(preds)


def parse_domain_def(iterator):
    """Parse a complete domain definition and return a DomainDef instance.

    Recursively calls all parsers needed to parse a domain definition.
    """
    def_string = parse_name(iterator, "domain def")
    if def_string != "define":
        raise ValueError(
            'Invalid domain definition! --> domain definition must start with "define"'
        )
    dom = parse_domain_stmt(next(iterator))
    domain = DomainDef(dom.name)
    # First parse all optional keywords.
    while not iterator.empty():
        next_iter = next(iterator)
        key = parse_keyword(next_iter.peek())
        if key.name == "requirements":
            domain.requirements = parse_requirements_stmt(next_iter)
        elif key.name == "types":
            domain.types = parse_types_stmt(next_iter)
        elif key.name == "predicates":
            domain.predicates = parse_predicates_stmt(next_iter)
        elif key.name == "constants":
            domain.constants = parse_constants_stmt(next_iter)
        elif key.name == "action":
            domain.actions.append(parse_action_stmt(next_iter))
            # From this point on only actions are allowed to follow.
            break
        else:
            raise ValueError(f"Found unknown keyword in domain definition: {key.name}")
    # Then parse all remaining actions.
    while not iterator.empty():
        next_iter = next(iterator)
        key = parse_keyword(next_iter.peek())
        if key.name != "action":
            raise ValueError("Error: Found invalid keyword while parsing actions")
        domain.actions.append(parse_action_stmt(next_iter))
    iterator.match_end()
    return domain


def parse_problem_name(iterator):
    """Parse a problem name (preceded by the 'problem' keyword) and return it."""
    if not iterator.try_match("problem"):
        raise ValueError(
            "Invalid problem name specification! problem name "
            'definition must start with "problem"'
        )
    return parse_name(iterator, "problem name")


def parse_problem_def(iterator):
    """Parse a complete problem definition and return a ProblemDef instance.

    Recursively calls all parsers needed to parse a problem definition.
    """
    if not iterator.try_match("define"):
        raise ValueError(
            "Invalid problem definition! --> problem definition "
            'must start with "define"'
        )
    # Parse the problem name and the corresponding domain name.
    probname = parse_problem_name(next(iterator))
    dom = parse_problem_domain_stmt(next(iterator))
    # Parse all object definitions.
    objects = {}
    if iterator.peek_tag() == ":objects":
        objects = parse_objects_stmt(next(iterator))
    init = parse_init_stmt(next(iterator))
    goal = parse_goal_stmt(next(iterator))
    iterator.match_end()
    return ProblemDef(probname, dom.name, objects, init, goal)


def parse_init_stmt(iterator):
    """Parse a problem's init statement and return an InitStmt.

    The init statement consists of a list of predicate instances.
    """
    if not iterator.try_match(":init"):
        raise ValueError("Error found invalid keyword when parsing InitStmt")
    preds = parse_predicate_instance_list(iterator)
    return InitStmt(preds)


def parse_goal_stmt(iterator):
    """Parse a problem's goal statement and return a GoalStmt.

    The goal statement consists of an arbitrary formula (STRIPS semantics are
    checked later by the tree visitor).
    """
    if not iterator.try_match(":goal"):
        raise ValueError("Error found invalid keyword when parsing GoalStmt")
    f = parse_formula(next(iterator))
    return GoalStmt(f)


class Parser:
    """The main entry point for translating domain and problem files.

    Use this class from outside the module to turn a domain and problem file
    into the data structures defined in pddl.py.
    """

    def __init__(self, dom_file, prob_file=None):
        # ``dom_file``/``prob_file`` are the domain and (optional) problem files.
        self.dom_file = dom_file
        self.prob_file = prob_file
        self.dom_input = ""
        self.prob_input = ""

    def _read_input(self, source):
        """Read and normalize the lisp input, returning a LispIterator."""
        return parse_lisp_iterator(source)

    def parse_domain(self, read_from_file=True):
        """Parse the domain and return the resulting pddl.Domain.

        If ``read_from_file`` is False, the domain is read from ``self.dom_input``
        instead of from ``self.dom_file``.
        """
        if read_from_file:
            with open(self.dom_file, encoding="utf-8") as file:
                self.dom_input = self._read_input(file)
        else:
            self.dom_input = self._read_input(self.dom_input.split("\n"))
        domain_ast = parse_domain_def(self.dom_input)
        visitor = TraversePDDLDomain()
        domain_ast.accept(visitor)
        return visitor.domain

    def parse_problem(self, dom, read_from_file=True):
        """Parse the problem and return the resulting pddl.Problem.

        If ``read_from_file`` is False, the problem is read from
        ``self.prob_input`` instead of from ``self.prob_file``.
        """
        if read_from_file:
            with open(self.prob_file, encoding="utf-8") as file:
                self.prob_input = self._read_input(file)
        else:
            self.prob_input = self._read_input(self.prob_input.split("\n"))
        problem_ast = parse_problem_def(self.prob_input)
        visitor = TraversePDDLProblem(dom)
        problem_ast.accept(visitor)
        return visitor.get_problem()

    def set_prob_file(self, fname):
        self.prob_file = fname


if __name__ == "__main__":
    import argparse

    argparser = argparse.ArgumentParser()
    argparser.add_argument(dest="domain", help="specify domain file")
    argparser.add_argument(dest="problem", help="specify problem file", nargs="?")
    options = argparser.parse_args()
    if options.domain is None:
        argparser.print_usage()
        argparser.error("Error domain file must be specified")
    pddl_parser = Parser(options.domain)
    print("-------- Starting to parse supplied domain file!")
    domain = pddl_parser.parse_domain()
    print("++++++++ parsed domain file successfully")
    print(domain)
    if options.problem is not None:
        print("-------- Starting to parse supplied problem file!")
        pddl_parser.set_prob_file(options.problem)
        problem = pddl_parser.parse_problem(domain)
        print("++++++++ parsed problem file successfully")
        print(problem)
