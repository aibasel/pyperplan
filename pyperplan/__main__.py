#! /usr/bin/env python3
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

# TODO: Give searches and heuristics commandline options and reenable preferred
# operators.

import argparse
import logging
import os
import sys

from pyperplan.planner import (
    find_domain,
    HEURISTICS,
    search_plan,
    SEARCHES,
    validate_solution,
    write_solution,
)


def main():
    # Commandline parsing
    log_levels = ["debug", "info", "warning", "error"]

    # get pretty print names for the search algorithms:
    # use the function/class name and strip off '_search'
    def get_callable_names(callables, omit_string):
        names = [c.__name__ for c in callables]
        names = [n.replace(omit_string, "").replace("_", " ") for n in names]
        return ", ".join(names)

    search_names = get_callable_names(SEARCHES.values(), "_search")

    argparser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    argparser.add_argument(dest="domain", nargs="?")
    argparser.add_argument(dest="problem")
    argparser.add_argument("-l", "--loglevel", choices=log_levels, default="info")
    argparser.add_argument(
        "-H",
        "--heuristic",
        choices=HEURISTICS.keys(),
        help="Select a heuristic",
        default="hff",
    )
    argparser.add_argument(
        "-s",
        "--search",
        choices=SEARCHES.keys(),
        help=f"Select a search algorithm from {search_names}",
        default="bfs",
    )
    args = argparser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.loglevel.upper()),
        format="%(asctime)s %(levelname)-8s %(message)s",
        stream=sys.stdout,
    )

    hffpo_searches = ["gbf", "wastar", "ehs"]
    if args.heuristic == "hffpo" and args.search not in hffpo_searches:
        print(
            "ERROR: hffpo can currently only be used with %s\n" % hffpo_searches,
            file=sys.stderr,
        )
        argparser.print_help()
        sys.exit(2)

    args.problem = os.path.abspath(args.problem)
    if args.domain is None:
        args.domain = find_domain(args.problem)
    else:
        args.domain = os.path.abspath(args.domain)

    search = SEARCHES[args.search]
    heuristic = HEURISTICS[args.heuristic]

    if args.search in ["bfs", "ids", "sat"]:
        heuristic = None

    logging.info("using search: %s" % search.__name__)
    logging.info("using heuristic: %s" % (heuristic.__name__ if heuristic else None))
    use_preferred_ops = args.heuristic == "hffpo"
    solution = search_plan(
        args.domain,
        args.problem,
        search,
        heuristic,
        use_preferred_ops=use_preferred_ops,
    )

    if solution is None:
        logging.warning("No solution could be found")
    else:
        solution_file = args.problem + ".soln"
        logging.info("Plan length: %s" % len(solution))
        write_solution(solution, solution_file)
        validate_solution(args.domain, args.problem, solution_file)


if __name__ == "__main__":
    main()
