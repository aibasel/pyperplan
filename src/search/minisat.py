import os
import sys
import subprocess
import logging
import itertools

import tools


INPUT = 'input.cnf'
OUTPUT = 'output.txt'
MINISAT = 'minisat'


def minisat_available():
    return tools.command_available([MINISAT, '--help'])


class CnfWriter():
    def _print_clause(self, clause):
        print(' '.join(str(self._literal_to_int(literal))
                       for literal in clause) + ' 0', file=self.cnf_file)

    def _print_clauses(self, clauses):
        for clause in clauses:
            self._print_clause(clause)

    def _get_aux_var(self):
        return next(self.count)

    def _literal_to_int(self, literal):
        if type(literal) is int:
            return literal
        negated = literal.startswith('not-')
        if negated:
            # remove the 'not-' string
            literal = literal[4:]
        if literal in self.vars_to_numbers:
            number = self.vars_to_numbers[literal]
        else:
            number = next(self.count)
            self.vars_to_numbers[literal] = number
        if negated:
            number = -number
        return number

    def _get_aux_clauses_for_iff(self, iff):
        a2, a1 = iff.split('<->')
        return [[iff, a2, a1], [iff, 'not-' + a2, 'not-' + a1],
                ['not-' + iff, a2, 'not-' + a1], ['not-' + iff, 'not-' + a2,
                                                  a1]]

    def _get_aux_clauses_for_and(self, var1, var2):
        #aux = '{0}AND{1}'.format(var1, var2)
        aux = self._get_aux_var()
        not_var1 = 'not-' + var1 if type(var1) is str else -var1
        not_var2 = 'not-' + var2 if type(var2) is str else -var2
        return aux, [[-aux, var1], [-aux, var2], [not_var1, not_var2, aux]]

    def write(self, formula):
        """Adds helper variables for all occurences of "a2<->a1" """
        self.count = itertools.count(start=1)
        self.vars_to_numbers = dict()

        aux_iff_vars = set()

        logging.debug('Writing minisat input file')
        # We omit specifying the number of vars and clauses because we don't
        # know those when we start writing the file
        self.cnf_file = open(INPUT, 'w')

        while formula:
            disj = formula.pop(0)
            if not isinstance(disj, list):
                self._print_clause([disj])
                continue
            new_clause = []
            for conj in disj:
                if not isinstance(conj, list):
                    new_clause.append(conj)
                    continue
                # Add auxiliary vars for iffs
                for literal in conj:
                    if '<->' in literal and literal not in aux_iff_vars:
                        self._print_clauses(self._get_aux_clauses_for_iff(
                                                                      literal))
                        aux_iff_vars.add(literal)
                # Turn list into one literal and add auxiliary clauses
                while len(conj) > 1:
                    var1 = conj.pop(0)
                    var2 = conj.pop(0)
                    aux_var, clauses = self._get_aux_clauses_for_and(var1,
                                                                     var2)
                    conj.insert(0, aux_var)
                    self._print_clauses(clauses)
                assert len(conj) == 1, conj
                new_clause.append(conj[0])
            self._print_clause(new_clause)

        self.cnf_file.close()
        for key in list(self.vars_to_numbers):
            if '<->' in key:
                del self.vars_to_numbers[key]
        return self.vars_to_numbers


def solve_with_minisat():
    """
    Calls minisat with the specified formula, the number of variables
    and the number of clauses.
    Returns the output filename of the minisat computation.
    """
    try:
        logging.debug('Solving with %s' % MINISAT)
        process = subprocess.Popen([MINISAT, INPUT, OUTPUT],
                                   stderr=subprocess.PIPE,
                                   stdout=subprocess.PIPE)
        process.wait()
    except OSError:
        logging.error('Minisat could not be found. '
            'Please make the executable "%s" available on the path '
            '(e.g. /usr/bin).' % MINISAT)
        sys.exit(1)
    tools.remove(INPUT)


def retransform_output(names_to_numbers):
    """
    Transform the number-variables-names back into
    the text-variable-names required by our planer.
    """
    logging.debug('Retransforming output')
    numbers_to_names = dict()
    for name, number in names_to_numbers.items():
        numbers_to_names[number] = name

    retransformed = []
    with open(OUTPUT, 'r') as file:
        lines = file.readlines()
    if lines[0].startswith('SAT'):
        vars = lines[1].split()
        # Last element is always a zero
        for var in vars[:-1]:
            negation = ''
            if var.startswith('-'):
                negation = 'not-'
                var = var[1:]
            var = numbers_to_names.get(int(var))
            # We don't need auxiliary variables
            if var:
                retransformed.append(negation + var)
    tools.remove(OUTPUT)
    return retransformed


def solve(formula):
    """
    Transforms the formula into the format required by minisat,
    calls minisat with the transformed formula, retranslates the
    output of minisat and returns the result.
    If the formula is satisfiable, a list of variables is returned:
    Every not-negated variable must be true, every negated variable
    must be false to satisfy the formula.
    If the formula is unsatisfiable, an empty list is returned.
    """
    # vars_to_numbers is a dictionary mapping variable names to numbers
    vars_to_numbers = CnfWriter().write(formula)
    solve_with_minisat()
    valuation = retransform_output(vars_to_numbers)
    return valuation
