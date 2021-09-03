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

"""Basic functions for parsing simple Lisp files."""


from .errors import ParseError
from .lisp_iterators import LispIterator


def parse_lisp_iterator(input):
    return LispIterator(parse_nested_list(input))


def parse_nested_list(input_file):
    tokens = _tokenize(input_file)
    next_token = next(tokens)
    if next_token != "(":
        raise ParseError("Expected '(', got %s." % next_token)
    result = list(_parse_list_aux(tokens))
    for tok in tokens:  # Check that generator is exhausted.
        raise ParseError("Unexpected token: %s." % tok)
    return result


def _tokenize(input_file):
    for line in input_file:
        line = line.partition(";")[0]  # Strip comments.
        line = line.replace("(", " ( ").replace(")", " ) ").replace("?", " ?")
        for token in line.split():
            yield token.lower()


def _parse_list_aux(tokenstream):
    # Invariant: leading "(" has already been swallowed.
    for token in tokenstream:
        if token == ")":  # List is closed.
            return
        elif token == "(":  # Recursive call.
            yield list(_parse_list_aux(tokenstream))
        else:
            yield token
    # If we exhausted the stream, the list is unbalanced.
    raise ParseError("missing closing parenthesis")
