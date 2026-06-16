#! /usr/bin/env python3
"""Run a representative set of search + heuristic configurations on tasks.

For each configuration and task, ``python -m pyperplan`` is invoked as a
subprocess with a per-run timeout, and the planner's reported "Overall time" is
recorded. The results are written as JSON so that two revisions can be compared
with ``compare-benchmarks.py``.

The configurations below cover every search algorithm and every heuristic at
least once. By default the first task of each benchmark domain is used; pass
``--tasks-per-domain`` to include more.

The ``--src`` option selects which pyperplan source tree to benchmark; it is put
on ``PYTHONPATH`` for the subprocesses.

Examples:
    dev/benchmark-search.py --out search-new.json
    dev/benchmark-search.py --src /tmp/pyperplan-base --out search-base.json
"""

import argparse
import json
import os
import re
import subprocess
import sys
from glob import glob

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Representative (search, heuristic) configurations. A heuristic of None means
# the search ignores heuristics (uninformed search). Together these exercise
# every registered search algorithm and every registered heuristic. The SAT
# search is omitted because it needs an external minisat executable.
CONFIGS = [
    ("bfs", None),
    ("ids", None),
    ("astar", "blind"),
    ("astar", "hadd"),
    ("astar", "hmax"),
    ("astar", "hff"),
    ("astar", "hsa"),
    ("astar", "lmcut"),
    ("astar", "landmark"),
    ("gbfs", "hff"),
    ("wastar", "hff"),
    ("ehs", "hff"),
]

OVERALL_TIME = re.compile(r"Overall time: (\d+\.\d+)")


def collect_tasks(benchmarks, per_domain):
    tasks = []
    for domain_dir in sorted(glob(os.path.join(benchmarks, "*", ""))):
        domain_tasks = sorted(glob(os.path.join(domain_dir, "task*.pddl")))
        tasks.extend(domain_tasks[:per_domain])
    return tasks


def run_config(search, heuristic, problem, env, timeout, successor_generator):
    cmd = [sys.executable, "-m", "pyperplan", "-s", search]
    if heuristic is not None:
        cmd += ["-H", heuristic]
    if successor_generator is not None:
        cmd += ["--successor-generator", successor_generator]
    cmd.append(problem)  # The domain is guessed by pyperplan.
    try:
        proc = subprocess.run(
            cmd, env=env, timeout=timeout, capture_output=True, text=True
        )
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "time": None}
    finally:
        # The planner writes the plan next to the problem; keep the tree clean.
        solution = problem + ".soln"
        if os.path.exists(solution):
            os.remove(solution)
    output = proc.stdout + proc.stderr
    if "Plan length:" in output:
        match = OVERALL_TIME.search(output)
        return {"status": "solved", "time": float(match.group(1)) if match else None}
    if "No solution" in output:
        return {"status": "unsolved", "time": None}
    return {"status": "error", "time": None}


def benchmark(src, benchmarks, per_domain, timeout, successor_generator):
    env = dict(os.environ, PYTHONPATH=src)
    tasks = collect_tasks(benchmarks, per_domain)
    results = {}
    runs = [(s, h, t) for s, h in CONFIGS for t in tasks]
    for i, (search, heuristic, problem) in enumerate(runs, start=1):
        config = f"{search}+{heuristic or 'none'}"
        rel = os.path.relpath(problem, benchmarks)
        key = f"{config} | {rel}"
        result = run_config(
            search, heuristic, problem, env, timeout, successor_generator
        )
        results[key] = result
        time = f"{result['time']:.3f}s" if result["time"] is not None else "-"
        print(f"[{i}/{len(runs)}] {key}: {result['status']} {time}")
    return results


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--src",
        default=REPO_ROOT,
        help="pyperplan source tree to benchmark (default: this repository)",
    )
    parser.add_argument(
        "--benchmarks",
        help="benchmark directory (default: <src>/benchmarks)",
    )
    parser.add_argument(
        "--tasks-per-domain",
        type=int,
        default=1,
        help="number of tasks per domain to run (default: 1)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=60.0,
        help="per-run timeout in seconds (default: 60)",
    )
    parser.add_argument(
        "--successor-generator",
        choices=["naive", "tree"],
        help="successor generator to pass to pyperplan (default: planner default)",
    )
    parser.add_argument("--out", help="write the results to this JSON file")
    args = parser.parse_args()

    src = os.path.abspath(args.src)
    benchmarks = args.benchmarks or os.path.join(src, "benchmarks")
    results = benchmark(
        src,
        benchmarks,
        args.tasks_per_domain,
        args.timeout,
        args.successor_generator,
    )

    if args.out:
        payload = {
            "src": src,
            "timeout": args.timeout,
            "tasks_per_domain": args.tasks_per_domain,
            "successor_generator": args.successor_generator,
            "results": results,
        }
        with open(args.out, "w") as f:
            json.dump(payload, f, indent=2)
        print(f"Wrote {args.out}")

    solved = sum(1 for r in results.values() if r["status"] == "solved")
    print(f"Solved {solved}/{len(results)} runs within {args.timeout:g}s.")


if __name__ == "__main__":
    main()
