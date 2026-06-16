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


from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Imported only for type checking to avoid an import cycle: the search
    # package imports the heuristics (and vice versa) at runtime.
    from ..search.searchspace import SearchNode
    from ..task import Task


class Heuristic:
    def __init__(self, task: Task) -> None:
        """Heuristics are constructed from the planning task they estimate."""

    def __call__(self, node: SearchNode) -> float:
        """Return the heuristic value for the state stored in ``node``."""
        raise NotImplementedError

    def calc_h_with_plan(self, node: SearchNode) -> tuple[float, set[str] | None]:
        """Return the heuristic value and a relaxed plan (preferred operators).

        Only heuristics that support preferred operators (currently hFF)
        override this; the others inherit this default.
        """
        raise NotImplementedError
