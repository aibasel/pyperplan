

import sys
from dataclasses import dataclass
from typing import Optional
from pyperplan.search.searchspace import SearchNode

@dataclass
class SearchResult:
    expansions : int = sys.maxsize
    generations: int = sys.maxsize
    evaluations: int = sys.maxsize
    elapsed    : float = 1e32
    rss     : int = sys.maxsize
    goal_node : Optional[SearchNode] = None


@dataclass
class SearchLimit:
    """
    This dataclass represents the hard and the soft limits for search.

    Whenever any of the hard limits are reached, the search stops.

    Each soft limit must be smaller than the corresponding hard limit, if present.

    The search stops when ALL soft limits are reached.
    """
    min_expansions : Optional[int] = None
    min_generations: Optional[int] = None
    min_evaluations: Optional[int] = None
    min_elapsed    : Optional[float] = None
    min_rss        : Optional[int] = None
    max_expansions : int = sys.maxsize
    max_generations: int = sys.maxsize
    max_evaluations: int = sys.maxsize
    max_elapsed    : float = 1e32
    max_rss        : int = sys.maxsize

    # Implementing the default values for soft limits is a bit complicated.

    # Setting the default value to negative value (which is always reached) is wrong because
    # the search stops immediately when no soft limits are given for exp/gen/eval/elapsed/rss.

    # Setting the default value to maxsize is also wrong, because such a limit is never reached
    # even if all other specified soft limits are reached, making the search continue indefinitely.

    def __post_init__(self):
        if self.min_expansions is not None:
            assert self.min_expansions <= self.max_expansions
        if self.min_generations is not None:
            assert self.min_generations <= self.max_generations
        if self.min_evaluations is not None:
            assert self.min_evaluations <= self.max_evaluations
        if self.min_elapsed is not None:
            assert self.min_elapsed <= self.max_elapsed
        if self.min_rss is not None:
            assert self.min_rss <= self.max_rss

    def satisfy(self, result : SearchResult):
        if self.max_expansions  <= result.expansions  or \
           self.max_generations <= result.generations or \
           self.max_evaluations <= result.evaluations or \
           self.max_elapsed     <= result.elapsed     or \
           self.max_rss         <= result.rss:
            return False

        if (self.min_expansions  is None) and \
           (self.min_generations is None) and \
           (self.min_evaluations is None) and \
           (self.min_elapsed     is None) and \
           (self.min_rss         is None):
            return True

        if ((self.min_expansions  is not None) and (self.min_expansions  > result.expansions )) or \
           ((self.min_generations is not None) and (self.min_generations > result.generations)) or \
           ((self.min_evaluations is not None) and (self.min_evaluations > result.evaluations)) or \
           ((self.min_elapsed     is not None) and (self.min_elapsed     > result.elapsed    )) or \
           ((self.min_rss         is not None) and (self.min_rss         > result.rss)):
            return True

        return False


if __name__ == "__main__":

    r00 = SearchResult(expansions=1,
                       generations=1,
                       evaluations=2500,
                       elapsed=100,
                       rss=1)

    r10 = SearchResult(expansions=1,
                       generations=1,
                       evaluations=7500,
                       elapsed=100,
                       rss=1)

    r20 = SearchResult(expansions=1,
                       generations=1,
                       evaluations=12500,
                       elapsed=100,
                       rss=1)

    r01 = SearchResult(expansions=1,
                       generations=1,
                       evaluations=2500,
                       elapsed=500,
                       rss=1)

    r11 = SearchResult(expansions=1,
                       generations=1,
                       evaluations=7500,
                       elapsed=500,
                       rss=1)

    r21 = SearchResult(expansions=1,
                       generations=1,
                       evaluations=12500,
                       elapsed=500,
                       rss=1)

    r02 = SearchResult(expansions=1,
                       generations=1,
                       evaluations=2500,
                       elapsed=1000,
                       rss=1)

    r12 = SearchResult(expansions=1,
                       generations=1,
                       evaluations=7500,
                       elapsed=1000,
                       rss=1)

    r22 = SearchResult(expansions=1,
                       generations=1,
                       evaluations=12500,
                       elapsed=1000,
                       rss=1)

    # no limit
    l0 = SearchLimit()
    # it stops when it evaluates 10000 nodes
    l1 = SearchLimit(min_evaluations=10000)
    # it stops when it evaluates 10000 nodes
    l2 = SearchLimit(max_evaluations=10000)
    # it stops when it evaluates 5000 nodes
    l3 = SearchLimit(min_evaluations=5000,
                     max_evaluations=10000)
    # it stops when it evaluates 10000 nodes
    # it stops when it searches 900 sec
    # it stops when it evaluates at least 5000 nodes and search at least 300 seconds
    l4 = SearchLimit(min_evaluations=5000,
                     max_evaluations=10000,
                     min_elapsed=300,
                     max_elapsed=900)

    assert l0.satisfy(r00)
    assert l0.satisfy(r10)
    assert l0.satisfy(r20)
    assert l0.satisfy(r01)
    assert l0.satisfy(r11)
    assert l0.satisfy(r21)
    assert l0.satisfy(r02)
    assert l0.satisfy(r12)
    assert l0.satisfy(r22)

    assert l1.satisfy(r00)
    assert l1.satisfy(r10)
    assert not l1.satisfy(r20)
    assert l1.satisfy(r01)
    assert l1.satisfy(r11)
    assert not l1.satisfy(r21)
    assert l1.satisfy(r02)
    assert l1.satisfy(r12)
    assert not l1.satisfy(r22)

    assert l2.satisfy(r00)
    assert l2.satisfy(r10)
    assert not l2.satisfy(r20)
    assert l2.satisfy(r01)
    assert l2.satisfy(r11)
    assert not l2.satisfy(r21)
    assert l2.satisfy(r02)
    assert l2.satisfy(r12)
    assert not l2.satisfy(r22)

    assert l3.satisfy(r00)
    assert not l3.satisfy(r10)
    assert not l3.satisfy(r20)
    assert l3.satisfy(r01)
    assert not l3.satisfy(r11)
    assert not l3.satisfy(r21)
    assert l3.satisfy(r02)
    assert not l3.satisfy(r12)
    assert not l3.satisfy(r22)

    assert l4.satisfy(r00)
    assert l4.satisfy(r10)
    assert not l4.satisfy(r20)  # hard limit
    assert l4.satisfy(r01)
    assert not l4.satisfy(r11)  # soft limit: 7500 > 5000, 500 > 300
    assert not l4.satisfy(r21)  # hard limit
    assert not l4.satisfy(r02)  # hard limit
    assert not l4.satisfy(r12)  # hard limit
    assert not l4.satisfy(r22)  # hard limit
