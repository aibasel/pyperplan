# Running pyperplan's search with Shed Skin

[Shed Skin](https://github.com/shedskin/shedskin) is a restricted-Python-to-C++
compiler. This directory contains an experiment that compiles pyperplan's blind
breadth-first search with Shed Skin and compares its speed against CPython using
the existing benchmark tooling in `dev/`.

## What is and isn't compiled

Shed Skin only supports a statically typed subset of Python. Pyperplan's full
pipeline (PDDL parsing and grounding) relies on regular expressions, recursive
descent parsing and dynamic dispatch that Shed Skin cannot compile. The
**search** phase, however, operates on a grounded task whose states are
`frozenset`s of facts — a clean, self-contained target.

We therefore:

1. ground a task with pyperplan and serialize it to an integer-encoded text
   format (`dump_task.py`), then
2. run a self-contained reimplementation of pyperplan's blind breadth-first
   search (`bfs_search.py`) on it.

`bfs_search.py` is the same algorithm as
`pyperplan/search/breadth_first_search.py` and reproduces pyperplan's results
exactly (identical plan lengths and expanded-node counts). The *same source
file* runs under CPython and, once compiled by Shed Skin, as a native
executable, so the comparison isolates "interpreter vs. compiler" for an
identical algorithm and data representation.

## Files

| File | Purpose |
| --- | --- |
| `bfs_search.py` | Self-contained blind BFS; runs under CPython and compiles with Shed Skin. |
| `dump_task.py` | Grounds a PDDL task with pyperplan and serializes it for `bfs_search.py`. |
| `benchmark.py` | Builds the native executable and benchmarks CPython vs. Shed Skin over the benchmark suite. |

## Requirements

* Shed Skin (latest release): `uv pip install shed-skin` (the PyPI package is
  named `shed-skin`; the command it installs is `shedskin`).
* A C++ compiler, CMake, and the Boehm GC / PCRE2 development libraries that
  Shed Skin links against.

## Usage

Build the native executable and run the full comparison (writes two JSON files
in the format produced by `dev/benchmark-search.py`):

```
dev/shedskin/benchmark.py --tasks-per-domain 1
```

Plot and summarize the results with the existing comparison script:

```
dev/compare-benchmarks.py shedskin-python.json shedskin-native.json \
    --success solved --title "BFS: CPython vs Shed Skin" --out bfs.png
```

You can also build and run the executable by hand:

```
cd dev/shedskin
shedskin build -x -b -w --noassert --build-type Release --jobs 4 bfs_search
dev/shedskin/dump_task.py benchmarks/tpp/task05.pddl --out task.txt
./build/bfs_search task.txt        # native (Shed Skin)
python3 bfs_search.py task.txt     # interpreted (CPython)
```

## Results

Measured on this repository's benchmark suite (blind BFS, search time only,
excluding parsing/grounding; CPython 3.11, Shed Skin 0.9.12, GCC, `-O` release
build).

**Shed Skin does not give pyperplan's search a consistent speedup.** The search
is dominated by `set`/`frozenset` operations (subset tests, set difference and
union, and membership in the closed list), which CPython already implements in
mature, cache-friendly C with cached `frozenset` hashes. Compiling the *same*
set-based algorithm with Shed Skin (whose sets are allocated through the Boehm
garbage collector) is therefore roughly break-even and highly task-dependent:
on some tasks the native build is several times faster, on others several times
slower.

Over the first two tasks of every benchmark domain (40 tasks solved by both,
per-run timeout 15 s):

| Metric | Value |
| --- | --- |
| Total search time, CPython | 22.89 s |
| Total search time, Shed Skin native | 24.02 s |
| Overall speedup (CPython / native) | **0.95×** |
| Per-task ratio (native / CPython) | median 0.97, geomean 0.95 |
| Tasks faster on native | 22 / 40 |

The per-task speedup of the native build (CPython time ÷ native time, so a value
above 1 means the native build was faster) varies widely on the tasks with a
non-trivial runtime:

| Task | CPython | Native | Speedup |
| --- | ---: | ---: | ---: |
| freecell/task01 | 1.954 s | 0.602 s | **3.25×** |
| transport/task02 | 0.232 s | 0.108 s | 2.16× |
| depot/task02 | 1.441 s | 1.253 s | 1.15× |
| elevators/task01 | 11.499 s | 10.629 s | 1.08× |
| sokoban/task01 | 0.064 s | 0.062 s | 1.04× |
| logistics/task01 | 0.193 s | 0.228 s | 0.85× |
| scanalyzer/task02 | 2.180 s | 2.635 s | 0.83× |
| openstacks/task02 | 0.266 s | 0.415 s | 0.64× |
| woodworking/task01 | 0.474 s | 0.789 s | 0.60× |
| woodworking/task02 | 2.198 s | 4.570 s | **0.48×** |

(Sub-millisecond tasks are omitted as timing noise.)

### Takeaway

For pyperplan specifically, naively compiling the search with Shed Skin is not a
reliable win, because the hot path is set manipulation that CPython already runs
as optimized C. A compiled planner that wants to beat CPython would need a
different state representation (for example fixed-width integer bitmasks instead
of `frozenset`s) so that the inner loop becomes integer/bitwise work, which is
where Shed Skin's ahead-of-time compilation pays off. The infrastructure here
makes it easy to try such variants: drop in another `*_search.py`, rebuild, and
re-run `benchmark.py`.
