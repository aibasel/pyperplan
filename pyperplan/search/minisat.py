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

"""Encode formulas as CNF and solve them with the minisat SAT solver."""

import itertools
import logging
import subprocess
import sys
from typing import IO, Any

from pyperplan import tools

INPUT = "input.cnf"
OUTPUT = "output.txt"
MINISAT = "minisat"


def minisat_available() -> bool:
    return tools.command_available([MINISAT, "--help"])


class CnfWriter:
    cnf_file: IO[str]
    count: "itertools.count[int]"
    vars_to_numbers: dict[str, int]

    def _print_clause(self, clause: list[Any]) -> None:
        print(
            " ".join(str(self._literal_to_int(literal)) for literal in clause) + " 0",
            file=self.cnf_file,
        )

    def _print_clauses(self, clauses: list[list[Any]]) -> None:
        for clause in clauses:
            self._print_clause(clause)

    def _get_aux_var(self) -> int:
        return next(self.count)

    def _literal_to_int(self, literal: str | int) -> int:
        if isinstance(literal, int):
            return literal
        negated = literal.startswith("not-")
        if negated:
            literal = literal[len("not-") :]
        if literal in self.vars_to_numbers:
            number = self.vars_to_numbers[literal]
        else:
            number = next(self.count)
            self.vars_to_numbers[literal] = number
        if negated:
            number = -number
        return number

    def _get_aux_clauses_for_iff(self, iff: str) -> list[list[str]]:
        a2, a1 = iff.split("<->")
        return [
            [iff, a2, a1],
            [iff, "not-" + a2, "not-" + a1],
            ["not-" + iff, a2, "not-" + a1],
            ["not-" + iff, "not-" + a2, a1],
        ]

    def _get_aux_clauses_for_and(
        self, var1: str | int, var2: str | int
    ) -> tuple[int, list[list[Any]]]:
        aux = self._get_aux_var()
        not_var1 = "not-" + var1 if isinstance(var1, str) else -var1
        not_var2 = "not-" + var2 if isinstance(var2, str) else -var2
        return aux, [[-aux, var1], [-aux, var2], [not_var1, not_var2, aux]]

    def write(self, formula: list[Any]) -> dict[str, int]:
        """Write ``formula`` to the CNF input file and return the variable map.

        Helper variables are added for all occurrences of "a2<->a1".
        """
        self.count = itertools.count(start=1)
        self.vars_to_numbers = {}

        aux_iff_vars: set[str] = set()

        logging.debug("Writing minisat input file")
        # We omit the number of variables and clauses because we don't know
        # those when we start writing the file.
        with open(INPUT, "w") as self.cnf_file:
            for disj in formula:
                if not isinstance(disj, list):
                    self._print_clause([disj])
                    continue
                new_clause: list[Any] = []
                for conj in disj:
                    if not isinstance(conj, list):
                        new_clause.append(conj)
                        continue
                    # Add auxiliary variables for iffs.
                    for literal in conj:
                        if "<->" in literal and literal not in aux_iff_vars:
                            self._print_clauses(self._get_aux_clauses_for_iff(literal))
                            aux_iff_vars.add(literal)
                    # Collapse the conjunction into a single literal by chaining
                    # auxiliary AND variables, emitting the matching clauses.
                    literal = conj[0]
                    for next_literal in conj[1:]:
                        literal, clauses = self._get_aux_clauses_for_and(
                            literal, next_literal
                        )
                        self._print_clauses(clauses)
                    new_clause.append(literal)
                self._print_clause(new_clause)

        for key in list(self.vars_to_numbers):
            if "<->" in key:
                del self.vars_to_numbers[key]
        return self.vars_to_numbers


def solve_with_minisat() -> None:
    """Run minisat on the CNF input file, writing its result to the output file."""
    try:
        logging.debug(f"Solving with {MINISAT}")
        process = subprocess.Popen(
            [MINISAT, INPUT, OUTPUT], stderr=subprocess.PIPE, stdout=subprocess.PIPE
        )
        process.wait()
    except OSError:
        logging.error(
            f"Minisat could not be found. "
            f'Please make the executable "{MINISAT}" available on the path '
            f"(e.g. /usr/bin)."
        )
        sys.exit(1)
    tools.remove(INPUT)


def retransform_output(names_to_numbers: dict[str, int]) -> list[str]:
    """Translate minisat's numeric variables back into the planner's names."""
    logging.debug("Retransforming output")
    numbers_to_names = {number: name for name, number in names_to_numbers.items()}

    retransformed: list[str] = []
    with open(OUTPUT) as file:
        lines = file.readlines()
    if lines[0].startswith("SAT"):
        variables = lines[1].split()
        # The last element is always a zero.
        for var in variables[:-1]:
            negation = ""
            if var.startswith("-"):
                negation = "not-"
                var = var[1:]
            name = numbers_to_names.get(int(var))
            # Skip auxiliary variables, which have no name.
            if name:
                retransformed.append(negation + name)
    tools.remove(OUTPUT)
    return retransformed


def solve(formula: list[Any]) -> list[str]:
    """Solve ``formula`` with minisat and return the resulting valuation.

    The formula is transformed into minisat's input format, solved, and the
    output is translated back. If the formula is satisfiable, a list of
    variables is returned: every non-negated variable must be true and every
    negated variable must be false to satisfy the formula. If the formula is
    unsatisfiable, an empty list is returned.
    """
    vars_to_numbers = CnfWriter().write(formula)
    solve_with_minisat()
    return retransform_output(vars_to_numbers)
