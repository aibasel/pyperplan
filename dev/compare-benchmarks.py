#! /usr/bin/env python3
"""Compare two benchmark result files and plot relative runtimes.

Reads two JSON files produced by ``benchmark-grounding.py`` or
``benchmark-search.py`` (an "old" and a "new" revision) and, for the tasks that
both revisions completed successfully, prints a runtime summary and writes a
log-log scatter plot of old vs. new runtime. Points below the diagonal were
faster on the new revision.

Examples:
    dev/compare-benchmarks.py grounding-base.json grounding-new.json \
        --out grounding.png --title "Grounding time"
    dev/compare-benchmarks.py search-base.json search-new.json \
        --out search.png --title "Search time" --success solved
"""

import argparse
import json
from statistics import geometric_mean, median

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def load(path):
    with open(path) as f:
        return json.load(f)["results"]


def common_tasks(old, new, success):
    """Return tasks both revisions completed with a positive runtime."""
    tasks = []
    for task, old_result in old.items():
        new_result = new.get(task)
        if (
            new_result
            and old_result["status"] == success
            and new_result["status"] == success
            and old_result["time"]
            and new_result["time"]
        ):
            tasks.append(task)
    return sorted(tasks)


def print_summary(old, new, tasks, success):
    def count(results):
        return sum(1 for r in results.values() if r["status"] == success)

    print(f"Successful ('{success}'): old={count(old)}, new={count(new)}")
    print(f"Completed by both: {len(tasks)}")
    if not tasks:
        return

    old_total = sum(old[t]["time"] for t in tasks)
    new_total = sum(new[t]["time"] for t in tasks)
    ratios = [new[t]["time"] / old[t]["time"] for t in tasks]
    faster = sum(1 for r in ratios if r < 1)
    print(f"Total time on common tasks: old={old_total:.2f}s, new={new_total:.2f}s")
    print(f"Overall speedup (old/new): {old_total / new_total:.2f}x")
    print(
        f"Per-task new/old ratio: median={median(ratios):.3f}, "
        f"geomean={geometric_mean(ratios):.3f}"
    )
    print(f"Faster on new: {faster}/{len(tasks)}; slower: {len(tasks) - faster}")

    biggest = sorted(tasks, key=lambda t: new[t]["time"] / old[t]["time"])
    print("\nLargest speedups (new/old):")
    for task in biggest[:5]:
        print(
            f"  {task}: {old[task]['time']:.3f}s -> {new[task]['time']:.3f}s "
            f"({new[task]['time'] / old[task]['time']:.2f}x)"
        )
    if biggest and new[biggest[-1]]["time"] > old[biggest[-1]]["time"]:
        print("Largest slowdowns (new/old):")
        for task in reversed(biggest[-5:]):
            ratio = new[task]["time"] / old[task]["time"]
            if ratio > 1:
                print(
                    f"  {task}: {old[task]['time']:.3f}s -> "
                    f"{new[task]['time']:.3f}s ({ratio:.2f}x)"
                )


def plot(old, new, tasks, title, out):
    xs = [old[t]["time"] for t in tasks]
    ys = [new[t]["time"] for t in tasks]
    colors = ["tab:green" if y < x else "tab:red" for x, y in zip(xs, ys)]

    low = min(xs + ys) * 0.7
    high = max(xs + ys) * 1.4

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(xs, ys, c=colors, s=18, alpha=0.7, edgecolors="none")
    # Diagonal (equal runtime) and 2x reference lines.
    ax.plot([low, high], [low, high], "k-", lw=1, label="equal")
    ax.plot([low, high], [low / 2, high / 2], "k:", lw=0.8, label="2x faster/slower")
    ax.plot([low, high], [low * 2, high * 2], "k:", lw=0.8)

    ax.set(
        xscale="log",
        yscale="log",
        xlim=(low, high),
        ylim=(low, high),
        xlabel="old runtime [s]",
        ylabel="new runtime [s]",
        title=f"{title}\n({len(tasks)} tasks; green = faster on new)",
    )
    ax.set_aspect("equal")
    ax.grid(True, which="both", ls=":", alpha=0.4)
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    print(f"\nWrote {out}")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("old", help="JSON results for the old (base) revision")
    parser.add_argument("new", help="JSON results for the new revision")
    parser.add_argument("--out", default="comparison.png", help="output plot path")
    parser.add_argument("--title", default="Runtime comparison", help="plot title")
    parser.add_argument(
        "--success",
        default="ok",
        help="status counted as success ('ok' for grounding, 'solved' for search)",
    )
    args = parser.parse_args()

    old, new = load(args.old), load(args.new)
    tasks = common_tasks(old, new, args.success)
    print_summary(old, new, tasks, args.success)
    if tasks:
        plot(old, new, tasks, args.title, args.out)


if __name__ == "__main__":
    main()
