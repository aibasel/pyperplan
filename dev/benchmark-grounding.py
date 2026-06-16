#! /usr/bin/env python3
"""Ground every task in the benchmark set, timing each grounding.

Each task is grounded in a separate subprocess so that a per-task timeout can
be enforced (grounding a large task can take a long time or a lot of memory).
The results are written as JSON so that two revisions can be compared with
``compare-benchmarks.py``.

The ``--src`` option selects which pyperplan source tree to benchmark; it is put
on ``PYTHONPATH`` for the worker subprocesses, so the script itself can live
outside the revision under test.

Examples:
    dev/benchmark-grounding.py --out grounding-new.json
    dev/benchmark-grounding.py --src /tmp/pyperplan-base --out grounding-base.json
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from glob import glob

NUMBER = re.compile(r"\d+")
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def find_domain(problem):
    """Guess the domain file for ``problem`` (mirrors pyperplan.planner)."""
    directory, name = os.path.split(problem)
    match = NUMBER.search(name)
    number = match.group(0) if match else ""
    domain = os.path.join(directory, "domain.pddl")
    for file in os.listdir(directory):
        if "domain" in file and number in file:
            domain = os.path.join(directory, file)
            break
    return domain if os.path.isfile(domain) else None


def ground_single(domain, problem):
    """Worker mode: parse and ground one task, printing the elapsed seconds."""
    from pyperplan import planner

    start = time.perf_counter()
    task = planner._ground(planner._parse(domain, problem))
    elapsed = time.perf_counter() - start
    print(f"RESULT time={elapsed:.6f} operators={len(task.operators)}")


def benchmark(src, benchmarks, timeout):
    env = dict(os.environ, PYTHONPATH=src)
    tasks = sorted(glob(os.path.join(benchmarks, "*", "task*.pddl")))
    results = {}
    for i, problem in enumerate(tasks, start=1):
        rel = os.path.relpath(problem, benchmarks)
        domain = find_domain(problem)
        if domain is None:
            results[rel] = {"status": "no-domain", "time": None}
            print(f"[{i}/{len(tasks)}] {rel}: no domain found")
            continue
        cmd = [sys.executable, os.path.abspath(__file__), "--single", domain, problem]
        try:
            proc = subprocess.run(
                cmd, env=env, timeout=timeout, capture_output=True, text=True
            )
        except subprocess.TimeoutExpired:
            results[rel] = {"status": "timeout", "time": None}
            print(f"[{i}/{len(tasks)}] {rel}: timeout (>{timeout:g}s)")
            continue
        match = re.search(r"RESULT time=(\S+) operators=(\d+)", proc.stdout)
        if proc.returncode == 0 and match:
            results[rel] = {
                "status": "ok",
                "time": float(match.group(1)),
                "operators": int(match.group(2)),
            }
            print(f"[{i}/{len(tasks)}] {rel}: {results[rel]['time']:.3f}s")
        else:
            results[rel] = {"status": "error", "time": None}
            print(f"[{i}/{len(tasks)}] {rel}: error (returncode {proc.returncode})")
    return results


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--single",
        nargs=2,
        metavar=("DOMAIN", "PROBLEM"),
        help="internal worker mode: ground a single task and print its time",
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
        "--timeout",
        type=float,
        default=60.0,
        help="per-task timeout in seconds (default: 60)",
    )
    parser.add_argument("--out", help="write the results to this JSON file")
    args = parser.parse_args()

    if args.single:
        ground_single(*args.single)
        return

    src = os.path.abspath(args.src)
    benchmarks = args.benchmarks or os.path.join(src, "benchmarks")
    results = benchmark(src, benchmarks, args.timeout)

    if args.out:
        payload = {"src": src, "timeout": args.timeout, "results": results}
        with open(args.out, "w") as f:
            json.dump(payload, f, indent=2)
        print(f"Wrote {args.out}")

    grounded = sum(1 for r in results.values() if r["status"] == "ok")
    print(f"Grounded {grounded}/{len(results)} tasks within {args.timeout:g}s.")


if __name__ == "__main__":
    main()
