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

from .errors import *
from .lisp_parser import parse_lisp_iterator
from .parser_common import *
from .tree_visitor import TraversePDDLDomain, TraversePDDLProblem, Visitable


"""
This module contains the main parser logic.
Partial parser for each AST node are implemented
and called recursively to construct a complete parse.
"""

# This emulates an c/c++ enum to distinguish between formulas variables and
# constants in formulas.
(TypeFormula, TypeVariable, TypeConstant) = range(3)

###
### Definitions of AST nodes
###


class Keyword(Visitable):
    """This class represents the AST node for a pddl keyword."""

    def __init__(self, name):
        """Construct a new Keyword.

        Keyword arguments:
        name -- the name of the keyword e.g. 'typed' if the keyword
                were ':typed'
        """
        self._visitorName = "visit_keyword"
        self.name = name


class Variable(Visitable):
    """This class represents the AST node for a pddl variable."""

    def __init__(self, name, types=None):
        """Construct a new Variable.

        Keyword arguments:
        name -- the name of the variable e.g. 'x' if the variable were '?x'
        types -- a list of names of Types denoting the possible types of this
                 variable
                 NOTE: checks that these types actually exist are implemented
                 in the TreeVisitor
        """
        self._visitorName = "visit_variable"
        self.name = name
        self.typed = types != None  # either True or False
        self.types = types  # either None or a List of Types


class Type(Visitable):
    """This class represents the AST node for a pddl type."""

    def __init__(self, name, parent=None):
        """Construct a new Type.

        Keyword arguments:
        name -- the name of the type
        parent -- a string that denotes the Typ instance that is the parent of
                  this type or None
        """
        self._visitorName = "visit_type"
        self.name = name
        self.parent = parent  # either None or a Type


class Predicate(Visitable):
    """This class represents the AST node for a pddl predicate."""

    def __init__(self, name, parameters=None):
        """Construct a new Predicate.

        Keyword arguments:
        name -- the name of the Predicate
        parameters -- a list of parameters described as variables
        """
        self._visitorName = "visit_predicate"
        self.name = name
        self.parameters = parameters or []  # a list of Variables


class PredicateInstance(Visitable):
    """This class represents the AST node for a pddl predicate instance."""

    def __init__(self, name, parameters=[]):
        """Construct a new Predicate.

        Keyword arguments:
        name -- the name of the Predicate
        parameters -- a list of parameters described as variables
        """
        self._visitorName = "visit_predicate_instance"
        self.name = name
        self.parameters = parameters  # a list of object names


class RequirementsStmt(Visitable):
    """This class represents the AST node for a pddl requirements statement."""

    def __init__(self, keywords=None):
        """Construct a new RequirementsStmt.

        Keyword arguments:
        keywords -- the list of requirements, represented as keywords
        """
        self._visitorName = "visit_requirements_stmt"
        self.keywords = keywords or []  # a list of keywords


class DomainStmt(Visitable):
    """This class represents the AST node for a pddl domain statement."""

    def __init__(self, name):
        """Construct a new RequirementsStmt.

        Keyword arguments:
        name -- the domain name as a string
        """
        self._visitorName = "visit_domain_stmt"
        self.name = name


class PreconditionStmt(Visitable):
    """This class represents the AST node for a pddl action precondition."""

    def __init__(self, formula):
        """Construct a new PreconditionStmt.

        Keyword arguments:
        formula -- the parsed formula,
                   NOTE: Arbitrary formulas are allowed here. STRIPS
                   compatibility etc. is checked later by the TreeVisitor
        """
        self._visitorName = "visit_precondition_stmt"
        self.formula = formula  # a Formula


class EffectStmt(Visitable):
    """This class represents the AST node for a pddl action effect."""

    def __init__(self, formula):
        """Construct a new EffectStmt.

        Keyword arguments:
        formula -- the parsed formula,
                   NOTE: Arbitrary formulas are allowed here. STRIPS
                   compatibility etc. is checked later by the TreeVisitor
        """
        self._visitorName = "visit_effect_stmt"
        self.formula = formula  # a Formula


class Formula(Visitable):
    """
    This class represents the AST node for a pddl formula,
    as it can be specified for preconditions and effects.
    """

    def __init__(self, key, children=None, type=TypeFormula):
        """Construct a new Formula.

        Keyword arguments:
        key -- the operator of the subformula e.g. 'not' if the formula were
               '(not (on a c))'
        children -- a list of immediate descending subformulas of this formula
        type -- the type of this formulas key --> one of
                (TypeFormula, TypeVariable, TypeConstant)
        """
        self._visitorName = "visit_formula"
        self.key = key
        self.children = children or []  # a list of Formulas
        self.type = type  # a Type


class ActionStmt(Visitable):
    """This class represents the AST node for a pddl action."""

    def __init__(self, name, parameters, precond, effect):
        """Construct a new Action.

        Keyword arguments:
        name -- the name of the action
        parameters -- a list of variables denoting the parameters
        precond -- the precondition of the action given as a Formula
        effect -- the effect of the action given as a Formula
        """
        self._visitorName = "visit_action_stmt"
        self.name = name
        self.parameters = parameters  # a list of parameters
        self.precond = precond  # right now: a Formula << PreconditionStmt
        # right now also a Formula << EffectStmt
        # --> should be checked when traversing the tree
        self.effect = effect


class PredicatesStmt(Visitable):
    """Represents the AST node for a pddl domain predicates definition."""

    def __init__(self, predicates):
        """Construct a new Action.

        Keyword arguments:
        predicates -- a list of predicates
        """
        self._visitorName = "visit_predicates_stmt"
        self.predicates = predicates  # a list of Predicates


class DomainDef(Visitable):
    """This class represents the AST node for a pddl domain."""

    def __init__(
        self,
        name,
        requirements=None,
        types=None,
        predicates=None,
        actions=None,
        constants=None,
    ):
        """Construct a new Domain AST node.

        Keyword arguments:
        name -- the domain name
        types -- a list of Type AST nodes
        predicates -- a list of Predicate AST nodes
        actions -- a list of Action AST nodes
        constants -- a list of Constants, as Object AST nodes
        """
        self._visitorName = "visit_domain_def"
        self.name = name
        self.requirements = requirements  # a RequirementsStmt
        self.types = types  # a list of Types
        self.predicates = predicates  # a PredicatesStmt
        if actions == None:
            self.actions = []
        else:
            self.actions = actions  # a list of ActionStmt
        self.constants = constants


class ProblemDef(Visitable):
    """This class represents the AST node for a pddl domain."""

    def __init__(self, name, domainName, objects=None, init=None, goal=None):
        """Construct a new Problem AST node.

        Keyword arguments:
        name -- the problem name
        domainName -- the domain name that corresponds to this problem
        objects -- a list of objects defined in the problem file
        init -- an initial condition represented by an InitStmt
        goal -- a  goal condition represented by an GoalStmt
        """
        self._visitorName = "visit_problem_def"
        self.name = name
        self.domainName = domainName
        self.objects = objects
        self.init = init
        self.goal = goal


class Object(Visitable):
    """This class represents the AST node for a pddl object."""

    def __init__(self, name, type):
        """Construct a new Object AST node.

        Keyword arguments:
        name -- the name of the object
        type -- the name of this objects Type
        """
        self._visitorName = "visit_object"
        self.name = name
        self.typeName = type


class InitStmt(Visitable):
    """
    This class represents the AST node for a pddl problem initial condition.
    """

    def __init__(self, predicates):
        """Construct a new InitStmt AST node.

        Keyword arguments:
        predicates -- a list of predicates denoting the initial codition
        """
        self._visitorName = "visit_init_stmt"
        self.predicates = predicates


class GoalStmt(Visitable):
    """This class represents the AST node for a pddl problem goal condition."""

    def __init__(self, formula):
        """Construct a new GoalStmt AST node.

        Keyword arguments:
        predicates -- a list of predicates denoting the goal codition
        """
        self._visitorName = "visit_goal_stmt"
        self.formula = formula


###
### some little helper functions
###


def parse_name(iter, father):
    if not iter.peek().is_word():
        raise ValueError("Error %s predicate statement must contain a name!" % father)
    return next(iter).get_word()


def parse_list_template(f, iter):
    """This function implements a common pattern used in this parser.

    It tries to parse a list of 'f' objects from the string 'string[i:end]'.
    The 'f' objects must be seperated by whitespace
    Returns a tuple of the position after the parsed list and the list.
    """
    result = list()
    # parse all possible occurences up to the end of the substring
    for elem in iter:
        var = f(elem)
        if var != None:
            result.append(var)
    return result


def _parse_string_helper(iter):
    return iter.get_word()


def _parse_type_helper(iter, type_class):
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
    # there may be several objects with the same type
    # hence we need to store each parsed object in a list and attach a new type
    # instance whenever a type is specified
    result = list()
    tmpList = list()
    while not iter.empty():
        var = next(iter).get_word()
        # print('VAR:', var)
        if type_class != Variable and len(var) > 0 and var[0] in reserved:
            raise ValueError("Error type must not begin with reserved char!")
        elif var == "-":
            # check if either definition present
            if iter.peek().is_structure():
                # must contain either definition
                types_iter = next(iter)
                if not types_iter.try_match("either"):
                    raise ValueError(
                        "Error multiple parent definition must " 'start with "either"'
                    )
                tlist = parse_list_template(_parse_string_helper, types_iter)
                while len(tmpList) != 0:
                    result.append(type_class(tmpList.pop(), tlist))
            else:
                # found type information --> flush objects into result list
                ctype = next(iter).get_word()
                while len(tmpList) != 0:
                    if type_class == Variable:
                        result.append(type_class(tmpList.pop(), [ctype]))
                    else:
                        result.append(type_class(tmpList.pop(), ctype))
        elif var != None and var != "":
            # found new object definition --> enqueue
            if type_class == Variable:
                if var[0] != "?":
                    raise ValueError('Error variables must start with a "?"')
                tmpList.insert(0, var)
            else:
                tmpList.insert(0, var)
    while len(tmpList) != 0:
        # append all left over objects --> these are untyped !!
        result.append(type_class(tmpList.pop(), None))
    return result


###
### parser functions
###


def parse_keyword(iter):
    """Parses a keyword from a given substring string[i:end].
    Returns the position in the string after the parsed keyword
    and the keyword itself as a tuple.
    """
    name = iter.get_word()
    if name == "":
        raise ValueError("Error empty keyword found")
    # ensure keyword starts with ':'
    if name[0] != ":":
        raise ValueError('Error keywords have to start with a colon ":"')
    return Keyword(name[1:])


def parse_keyword_list(iter):
    """Parses a list of keywords using the parse_list_template helper.

    Returns a tuple of the position within the string after the parsed list and
    the list itself.
    """
    return parse_list_template(parse_keyword, iter)


def parse_variable(iter):
    """Parses a Variable from the supplied string.

    Returns the position after the variable definition and a Variable instance.
    """
    name = iter.get_word()
    if name == "":
        raise ValueError("Error empty variable found")
    # ensure variable starts with '?'
    if name[0] != "?":
        raise ValueError('Error variables must start with a "?"')
    return Variable(name, None)


def parse_typed_var_list(iter):
    """
    Parses a list of - possibly typed - variables using the _parse_type_helper
    function.

    Returns the position after the type list and the resulting list of type
    instances.
    """
    return _parse_type_helper(iter, Variable)


def parse_parameters(iter):
    """
    Parses a list of parameters using the parse_typed_var_list parser function.
    """
    # check that the parameters definition starts with the correct keyword
    if not iter.try_match(":parameters"):
        raise ValueError(
            'Error keyword ":parameters" required before ' "parameter list!"
        )
    varList = parse_typed_var_list(next(iter))
    return varList


def parse_requirements_stmt(iter):
    """Parse the pddl requirements definition.
    Returns an RequirementsStmt.
    """
    # check for requirements keyword
    if not iter.try_match(":requirements"):
        raise ValueError(
            "Error requirements list must contain keyword " '":requirements"'
        )
    keywords = parse_keyword_list(iter)
    return RequirementsStmt(keywords)


def _parse_types_with_error(iter, keyword, classt):
    if not iter.try_match(keyword):
        raise ValueError(
            f'Error keyword "{keyword}" required before {classt.__name__}!'
        )
    return _parse_type_helper(iter, classt)


# Constants / Objects and types can be parsed in the same way because of their
# familiar structure.
# Hence instantiate them with _parse_types_with_error.
_common_types = [(":types", Type), (":objects", Object), (":constants", Object)]
(parse_types_stmt, parse_objects_stmt, parse_constants_stmt) = map(
    lambda tup: lambda it: _parse_types_with_error(it, tup[0], tup[1]), _common_types
)


def _parse_domain_helper(iter, keyword):
    """Parses the domain statement, which consists of the domain name.

    Returns a DomainStmt instance.
    """
    if not iter.try_match(keyword):
        raise ValueError(
            "Error domain statement must be present before " "domain name!"
        )
    name = parse_name(iter, "domain")
    return DomainStmt(name)


parse_domain_stmt = lambda it: _parse_domain_helper(it, "domain")
parse_problem_domain_stmt = lambda it: _parse_domain_helper(it, ":domain")


def parse_predicate(iter):
    """
    Parse a single predicate instance by parsing its name and a list of typed
    variables defining the signature.
    Returns a Predicate instance.
    """
    name = parse_name(iter, "predicate")
    params = parse_typed_var_list(iter)
    return Predicate(name, params)


def parse_predicate_list(iter):
    """Parses a list of predicates using the parse_list_template helper.

    Returns a list containing predicates.
    """
    return parse_list_template(parse_predicate, iter)


def parse_predicate_instance(iter):
    """
    Parses a predicate instance which is a predicate with possibly instantiated
    signature.
    Returns a Predicate instance.
    """
    name = parse_name(iter, "domain")
    params = parse_list_template(_parse_string_helper, iter)
    return PredicateInstance(name, params)


def parse_predicate_instance_list(iter):
    """
    Parse a list of predicate instances using the parse_list_template helper.
    """
    return parse_list_template(parse_predicate_instance, iter)


def parse_formula(iter):
    """Parse a Formula recursively

    Note: This parses formulas recursively !!
          We do not use tail recursion

    Returns the position after the formula and the Formula instance
    """
    if iter.is_structure():
        # this is a nested formula
        type = TypeFormula
        key = iter.peek().get_word()
        next(iter)
        if key[0] in reserved:
            raise ValueError("Error: Formula must not start with reserved " "char!")
        children = parse_list_template(parse_formula, iter)
    else:
        # non nested formula
        key = iter.get_word()
        children = []
        if key[0] == "?":
            key = parse_variable(iter)
            type = TypeVariable
        else:
            type = TypeConstant
    return Formula(key, children, type)


def _parse_precondition_or_effect(iter, keyword, type):
    """Parse an action precondition or effect

    Returns a PreconditionStmt or EffectStmt instance.
    """
    if not iter.try_match(keyword):
        raise ValueError(f'Error: {type.__name__} must start with "{keyword}" keyword')
    cond = parse_formula(next(iter))
    return type(cond)


def parse_precondition_stmt(it):
    return _parse_precondition_or_effect(it, ":precondition", PreconditionStmt)


def parse_effect_stmt(it):
    return _parse_precondition_or_effect(it, ":effect", EffectStmt)


def parse_action_stmt(iter):
    """
    Parse an action definition which consists of a name, parameters a
    precondition and an effect.

    Returns an ActionStmt instance.
    """
    # each action begins with a name
    if not iter.try_match(":action"):
        raise ValueError('Error: action must start with ":action" keyword!')
    name = parse_name(iter, "action")
    # call parsers to parse parameters, precondition, effect
    param = parse_parameters(iter)
    pre = parse_precondition_stmt(iter)
    eff = parse_effect_stmt(iter)
    return ActionStmt(name, param, pre, eff)


def parse_predicates_stmt(iter):
    """
    Parse a PredicatesStmt which is essentially a list of predicates preceded
    by the ':predicates' keyword.

    Returns a PredicatesStmt instance
    """
    if not iter.try_match(":predicates"):
        raise ValueError(
            "Error predicate definition must start with " '":predicates" keyword!'
        )
    preds = parse_predicate_list(iter)
    return PredicatesStmt(preds)


def parse_domain_def(iter):
    """Main parser method to parse a domain definition.

    Recursively calls all parsers needed to parse a domain definition.
    Returns a DomainDef instance
    """
    defString = parse_name(iter, "domain def")
    if defString != "define":
        raise ValueError(
            "Invalid domain definition! --> domain definition "
            'must start with "define"'
        )
    dom = parse_domain_stmt(next(iter))
    # create new DomainDef
    domain = DomainDef(dom.name)
    # first parse all optional keywords
    while not iter.empty():
        next_iter = next(iter)
        key = parse_keyword(next_iter.peek())
        if key.name == "requirements":
            req = parse_requirements_stmt(next_iter)
            domain.requirements = req
        elif key.name == "types":
            types = parse_types_stmt(next_iter)
            domain.types = types
        elif key.name == "predicates":
            pred = parse_predicates_stmt(next_iter)
            domain.predicates = pred
        elif key.name == "constants":
            const = parse_constants_stmt(next_iter)
            domain.constants = const
        elif key.name == "action":
            action = parse_action_stmt(next_iter)
            domain.actions.append(action)
            # from this point on only actions are allowed to follow
            break
        else:
            raise ValueError("Found unknown keyword in domain definition: " + key.name)
    # next parse all defined actions
    while not iter.empty():
        next_iter = next(iter)
        key = parse_keyword(next_iter.peek())
        if key.name != "action":
            raise ValueError("Error: Found invalid keyword while parsing " "actions")
        action = parse_action_stmt(next_iter)
        domain.actions.append(action)
    # assert end is reached
    iter.match_end()
    return domain


def parse_problem_name(iter):
    """
    Parse a problem name, which is a string, preceded by the ':problem'
    keyword.

    Returns the name as a string.
    """
    if not iter.try_match("problem"):
        raise ValueError(
            "Invalid problem name specification! problem name "
            'definition must start with "problem"'
        )
    name = parse_name(iter, "problem name")
    return name


def parse_problem_def(iter):
    """Main method to parse a problem definition.

    All parser metthods that are needed to parse a problem are called
    recursively by this function.

    Returns a ProblemDef instance
    """
    if not iter.try_match("define"):
        raise ValueError(
            "Invalid problem definition! --> problem definition "
            'must start with "define"'
        )
    # parse problem name and corresponding domain name
    probname = parse_problem_name(next(iter))
    dom = parse_problem_domain_stmt(next(iter))
    # parse all object definitions
    objects = dict()
    if iter.peek_tag() == ":objects":
        objects = parse_objects_stmt(next(iter))
    init = parse_init_stmt(next(iter))
    goal = parse_goal_stmt(next(iter))
    # assert end is reached
    iter.match_end()
    # create new ProblemDef instance
    return ProblemDef(probname, dom.name, objects, init, goal)


def parse_init_stmt(iter):
    """Parse the init statement of a problem definition.

    The InitStmt consists of a list of predicates and thus uses
    parse_predicate_instance_list.

    Returns an InitStmt instance.
    """
    if not iter.try_match(":init"):
        raise ValueError("Error found invalid keyword when parsing InitStmt")
    preds = parse_predicate_instance_list(iter)
    return InitStmt(preds)


def parse_goal_stmt(iter):
    """Parse the init statement of a problem definition.

    The InitStmt consists of an arbitrary formula (STRIPS semantic will be
    checked later by the tree visitor).

    Returns an GoalStmt instance.
    """
    if not iter.try_match(":goal"):
        raise ValueError("Error found invalid keyword when parsing GoalStmt")
    f = parse_formula(next(iter))
    return GoalStmt(f)


class Parser:
    """
    This is the main Parser class that can be used from outside this module
    to translate a given domain and problem file into the representation given
    in pddl.py!
    """

    def __init__(self, domFile, probFile=None):
        """Constructor

        Keyword arguments:
        domFile -- the domain File
        probFile -- the problem File or None
        """
        self.domFile = domFile
        self.probFile = probFile
        self.domInput = ""
        self.probInput = ""

    def _read_input(self, source):
        """Reads the lisp input from a given source and normalizes it.

        Returns the LispIterator that is read from the source.
        """
        result = parse_lisp_iterator(source)
        return result

    def parse_domain(self, read_from_file=True):
        """
        Method that parses a domain, this method will be called from outside
        the parser.

        Keyword arguments:
        read_from_file -- defines whether the input should be read from a file
                          or directly from the input string
        """
        if read_from_file:
            with open(self.domFile, encoding="utf-8") as file:
                self.domInput = self._read_input(file)
        else:
            input = self.domInput.split("\n")
            self.domInput = self._read_input(input)
        domAST = parse_domain_def(self.domInput)
        # initialize the translation visitor
        visitor = TraversePDDLDomain()
        # and traverse the AST
        domAST.accept(visitor)
        # finally return the pddl.Domain
        return visitor.domain

    def parse_problem(self, dom, read_from_file=True):
        """
        Method that parses a problem, this method will be called from outside
        the parser.

        Keyword arguments:
        read_from_file -- defines whether the input should be read from a file
                          or directly from the input string
        """
        if read_from_file:
            with open(self.probFile, encoding="utf-8") as file:
                self.probInput = self._read_input(file)
        else:
            input = self.probInput.split("\n")
            self.probInput = self._read_input(input)
        probAST = parse_problem_def(self.probInput)
        # initialize the translation visitor
        visitor = TraversePDDLProblem(dom)
        # and traverse the AST
        probAST.accept(visitor)
        # finally return the pddl.Problem
        return visitor.get_problem()

    def set_prob_file(self, fname):
        self.probFile = fname


if __name__ == "__main__":
    # additional imports here to prevent cyclic imports!
    argparser = argparse.ArgumentParser()
    argparser.add_argument(dest="domain", help="specify domain file")
    argparser.add_argument(dest="problem", help="specify problem file", nargs="?")
    options = argparser.parse_args()
    if options.domain == None:
        parser.print_usage()
        parser.error("Error domain file must be specified")
    pddlParser = Parser(options.domain)
    print("-------- Starting to parse supplied domain file!")
    domain = pddlParser.parse_domain()
    print("++++++++ parsed domain file successfully")
    print(domain)
    if options.problem != None:
        print("-------- Starting to parse supplied problem file!")
        pddlParser.set_prob_file(options.problem)
        problem = pddlParser.parse_problem(domain)
        print("++++++++ parsed problem file successfully")
        print(problem)
