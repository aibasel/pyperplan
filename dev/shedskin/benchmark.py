#! /usr/bin/env python3
"""Compare CPython and Shed Skin on pyperplan's blind breadth-first search.

For each benchmark task this script

1. grounds the task with pyperplan and serializes it (``dump_task.py``),
2. runs the breadth-first search (``bfs_search.py``) once under CPython and once
   as the native executable produced by Shed Skin, and
3. records the reported search time.

The results are written as two JSON files in the same format as
``dev/benchmark-search.py``, so they can be compared and plotted with the
existing ``dev/compare-benchmarks.py``::

    dev/shedskin/benchmark.py --tasks-per-domain 1
    dev/compare-benchmarks.py shedskin-python.json shedskin-native.json \\
        --success solved --title "BFS: CPython vs Shed Skin" --out bfs.png

The native executable is built automatically with ``shedskin`` if it is missing;
pass ``--rebuild`` to force a rebuild.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from glob import glob

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(HERE))
EXECUTABLE = os.path.join(HERE, "build", "bfs_search")
RESULT = re.compile(r"RESULT time=(\S+) plan=(-?\d+) expanded=(\d+)")


def build_executable(rebuild):
    if os.path.exists(EXECUTABLE) and not rebuild:
        return
    print("Building native executable with Shed Skin ...")
    subprocess.run(
        [
            "shedskin", "build", "-x", "-b", "-w", "--noassert",
            "--jobs", "4", "--build-type", "Release", "bfs_search",
        ],
        cwd=HERE,
        check=True,
    )


def collect_tasks(benchmarks, per_domain):
    tasks = []
    for domain_dir in sorted(glob(os.path.join(benchmarks, "*", ""))):
        domain_tasks = sorted(glob(os.path.join(domain_dir, "task*.pddl")))
        tasks.extend(domain_tasks[:per_domain])
    return tasks


def dump_task(problem, task_file, timeout):
    cmd = [sys.executable, os.path.join(HERE, "dump_task.py"), problem, "--out", task_file]
    try:
        proc = subprocess.run(cmd, timeout=timeout, capture_output=True, text=True)
    except subprocess.TimeoutExpired:
        return False
    return proc.returncode == 0 and os.path.exists(task_file)


def run_search(cmd, timeout):
    """Run a search command and return ``{"status", "time"}``."""
    try:
        proc = subprocess.run(cmd, timeout=timeout, capture_output=True, text=True)
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "time": None}
    if proc.returncode != 0:
        return {"status": "error", "time": None}
    match = RESULT.search(proc.stdout)
    if not match:
        return {"status": "error", "time": None}
    plan = int(match.group(2))
    return {
        "status": "solved" if plan >= 0 else "unsolved",
        "time": float(match.group(1)),
    }


def benchmark(benchmarks, per_domain, timeout):
    tasks = collect_tasks(benchmarks, per_domain)
    python_results = {}
    native_results = {}
    task_file = os.path.join(HERE, "build", "_current_task.txt")
    for i, problem in enumerate(tasks, start=1):
        rel = os.path.relpath(problem, benchmarks)
        if not dump_task(problem, task_file, timeout):
            python_results[rel] = {"status": "error", "time": None}
            native_results[rel] = {"status": "error", "time": None}
            print(f"[{i}/{len(tasks)}] {rel}: grounding failed")
            continue
        py = run_search([sys.executable, os.path.join(HERE, "bfs_search.py"), task_file], timeout)
        native = run_search([EXECUTABLE, task_file], timeout)
        python_results[rel] = py
        native_results[rel] = native
        os.remove(task_file)

        def fmt(r):
            return f"{r['time']:.3f}s" if r["time"] is not None else r["status"]

        speedup = ""
        if py["time"] and native["time"]:
            speedup = f"  (python/native: {py['time'] / native['time']:.2f}x)"
        print(
            f"[{i}/{len(tasks)}] {rel}: python={fmt(py)} native={fmt(native)}{speedup}"
        )
    return python_results, native_results


def write(path, results, timeout):
    payload = {"src": HERE, "timeout": timeout, "results": results}
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"Wrote {path}")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--benchmarks",
        default=os.path.join(REPO_ROOT, "benchmarks"),
        help="benchmark directory (default: <repo>/benchmarks)",
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
        "--rebuild", action="store_true", help="force rebuilding the native executable"
    )
    parser.add_argument("--out-python", default="shedskin-python.json")
    parser.add_argument("--out-native", default="shedskin-native.json")
    args = parser.parse_args()

    build_executable(args.rebuild)
    python_results, native_results = benchmark(
        args.benchmarks, args.tasks_per_domain, args.timeout
    )
    write(args.out_python, python_results, args.timeout)
    write(args.out_native, native_results, args.timeout)

    common = [
        t
        for t in python_results
        if python_results[t]["time"] and native_results[t].get("time")
    ]
    if common:
        py_total = sum(python_results[t]["time"] for t in common)
        native_total = sum(native_results[t]["time"] for t in common)
        print(
            f"\nCommon tasks: {len(common)}  "
            f"CPython total={py_total:.2f}s  native total={native_total:.2f}s  "
            f"native speedup (python/native)={py_total / native_total:.2f}x"
        )
    print(
        "\nCompare and plot with:\n"
        f"  dev/compare-benchmarks.py {args.out_python} {args.out_native} "
        '--success solved --title "BFS: CPython vs Shed Skin" --out bfs.png'
    )


if __name__ == "__main__":
    main()
