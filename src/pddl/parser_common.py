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

"""
This module contains methods that carry out the tokenization of the pddl input.
Since we directly parse our tokens from the input string in-place a token is
uniquely identified by its start and end position.
"""

# define the set of special characters
whiteSpace = set([' ', '\n', '\t'])
comment = set([';'])
reserved = set([':', ')', '(']).union(comment)
