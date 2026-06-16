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

from ..search.searchspace import SearchNode
from ..task import State, Task
from .heuristic_base import Heuristic


class BlindHeuristic(Heuristic):
    """A simple blind heuristic: 0 if the goal is reached and 1 otherwise."""

    def __init__(self, task: Task) -> None:
        super().__init__(task)
        self.goals: State = task.goals

    def __call__(self, node: SearchNode) -> float:
        return 0 if self.goals <= node.state else 1
