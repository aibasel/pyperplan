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

from .errors import ParseError


class LispIterator:
    """Iterator for a nested tree structure.

    A tree is either a plain string, in which case it is called a
    "word", or (recursively) a list of trees, in which case it is
    called a "structure".

    For trees that are structures, the iterator offers methods to
    advance through the elements of the structure, producing
    sub-iterators for each element.

    Most methods work on iterators for structures only (indicated in
    their documentation). These methods raise a ParseError when
    invoked on iterators for words.
    """

    def __init__(self, contents):
        """Initialize iterator from a nested list (structure) or
        string (word)."""
        self.position = 0
        self.contents = contents

    def _raise_if(self, condition, msg):
        if condition:
            raise ParseError(msg, self)

    def __repr__(self):
        return "<LispIterator(%d, %r)>" % (self.position, self.contents)

    ## Low-level interface. The following methods may access the
    ## position and contents attributes directly.

    def is_word(self):
        """Returns true iff the tree is a word (has no subtrees)."""
        return isinstance(self.contents, str)

    def is_structure(self):
        """Returns true iff the tree is a structure (has subtrees)."""
        return isinstance(self.contents, list)

    def empty(self):
        self._raise_if(self.is_word(), "cannot call empty on word")
        return self.peek() == None

    def get_word(self):
        """If called on a word, return the word as a string.
        If called on a structure, raise ParseError."""
        self._raise_if(self.is_structure(), "not a word")
        return self.contents

    def peek(self):
        """Structures only. Return iterator for next subtree, or None
        if already at the end. Do not advance."""
        self._raise_if(self.is_word(), "not a structure")
        if self.position == len(self.contents):
            return None
        return LispIterator(self.contents[self.position])

    def __iter__(self):
        """Structures only. Iterate over remaining subtrees."""
        return self

    def __next__(self):
        """Structures only. Return iterator for next subtree and
        advance. Raise StopIteration if at the end."""
        result = self.peek()
        if result is None:
            raise StopIteration
        else:
            self.position += 1
            return result

    ### High-level interface. The following methods are implemented in
    ### terms of the low-level interface.

    def next(self):
        """Structures only. Return iterator for next subtree and
        advance. Raise ParseError if at the end."""
        try:
            return self.__next__()
        except StopIteration:
            self._raise_if(True, "already at end")

    def try_match(self, word):
        """Structure only. If next element is the given word, return
        True and advance. Otherwise, return False and do not advance.
        May be safely called if already at the end."""
        peeked = self.peek()
        if peeked and peeked.is_word() and peeked.get_word() == word:
            self.next()
            return True
        else:
            return False

    def match(self, word):
        """Structure only. Verify that next element is the given word
        and advance. If at the end or if next element is something
        else, raise ParseError."""
        self._raise_if(not self.try_match(word), "expected %r" % word)

    def match_end(self):
        """Structure only. Raise ParseError if not at the end."""
        self._raise_if(self.peek() is not None, "expected to be at end")

    ## Convenience functions for frequently needed operations that are
    ## even higher level than the high-level interface.

    def peek_tag(self):
        """Structure only. If next element is a structure whose first
        element is a word, return that word. If at end, if next
        element is an empty structure, or if next element's first
        element is a structure, return None."""
        item = self.peek()
        if item.is_structure():
            subitem = item.peek()
            if subitem and subitem.is_word():
                return subitem.get_word()
        else:
            return None
