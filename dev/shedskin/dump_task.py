#! /usr/bin/env python3
"""Ground a PDDL task with pyperplan and serialize it for the Shed Skin search.

The grounded task (facts, initial state, goal and operators) is written in a
simple, integer-encoded text format that ``bfs_search.py`` can parse without
relying on Python features that Shed Skin does not support (such as ``json`` or
regular expressions). Every fact is mapped to a small integer id and a state is
just a set of such ids.

File format (whitespace separated, one record per line)::

    <num_facts> <num_operators>
    <init id...>
    <goal id...>
    for each operator:
        <operator name>            # may contain spaces
        <precondition id...>
        <add-effect id...>
        <delete-effect id...>

Example:
    dev/shedskin/dump_task.py benchmarks/tpp/task05.pddl --out task05.txt
"""

import argparse
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, REPO_ROOT)

from pyperplan import planner  # noqa: E402


def dump(task, out):
    # Map each fact to a stable integer id (sorted for reproducibility).
    facts = sorted(task.facts)
    fact_id = {fact: i for i, fact in enumerate(facts)}

    def ids(facts):
        return " ".join(str(fact_id[f]) for f in sorted(facts))

    with open(out, "w") as f:
        f.write(f"{len(facts)} {len(task.operators)}\n")
        f.write(ids(task.initial_state) + "\n")
        f.write(ids(task.goals) + "\n")
        for op in task.operators:
            f.write(op.name + "\n")
            f.write(ids(op.preconditions) + "\n")
            f.write(ids(op.add_effects) + "\n")
            f.write(ids(op.del_effects) + "\n")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("problem", help="PDDL problem file (domain is guessed)")
    parser.add_argument("--domain", help="PDDL domain file (default: guess)")
    parser.add_argument("--out", required=True, help="output task file")
    args = parser.parse_args()

    domain = args.domain or planner.find_domain(args.problem)
    task = planner._ground(planner._parse(domain, args.problem))
    dump(task, args.out)
    print(
        f"Wrote {args.out}: {len(task.facts)} facts, {len(task.operators)} operators"
    )


if __name__ == "__main__":
    main()
