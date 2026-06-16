#! /usr/bin/env python3
"""Build a mypyc-compiled copy of the pyperplan package.

mypyc translates type-annotated Python into C extension modules, which can run
considerably faster than the interpreted version. This script produces a
self-contained copy of the source tree in which the package modules have been
compiled to ``.so`` files, so it can be benchmarked against the pure-Python
tree with ``benchmark-search.py``/``benchmark-grounding.py`` and compared with
``compare-benchmarks.py``:

    dev/build-mypyc.py --dest build/mypyc
    dev/benchmark-search.py --src . --out search-python.json
    dev/benchmark-search.py --src build/mypyc --out search-mypyc.json
    dev/compare-benchmarks.py search-python.json search-mypyc.json \
        --success solved --title "Search time: Python vs mypyc"

The compiled modules are plain C extensions and do not need mypy at runtime, so
both benchmark runs can use the same interpreter; only ``--src`` differs.

The build itself needs mypy, setuptools and a C compiler. By default it is run
through ``uv run`` (matching the rest of the project's tooling), which provides
mypy and setuptools in a throwaway environment for the chosen Python version.

Notes:
  * ``__main__.py`` is intentionally left uncompiled so that ``python -m
    pyperplan`` keeps working (``-m`` cannot run a compiled module).
  * Each module is compiled as a separate extension (``separate=True``). This
    avoids a whole-program mypyc crash on the current mypy release and keeps the
    build robust as the package evolves.
"""

import argparse
import glob
import os
import shutil
import subprocess
import sys
import sysconfig
import textwrap

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Build script written into the destination tree and executed there.
SETUP_TEMPLATE = textwrap.dedent(
    """\
    import glob

    from mypyc.build import mypycify
    from setuptools import setup

    # Compile every package module except __main__.py (see build-mypyc.py).
    modules = sorted(
        m
        for m in glob.glob("pyperplan/**/*.py", recursive=True)
        if os.path.basename(m) != "__main__.py"
    )
    setup(
        name="pyperplan",
        ext_modules=mypycify(modules, opt_level="3", separate=True),
    )
    """
)


def copy_package(dest):
    """Copy the pyperplan package into ``dest``, dropping tests and artifacts."""
    package_src = os.path.join(REPO_ROOT, "pyperplan")
    package_dst = os.path.join(dest, "pyperplan")
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)
    shutil.copytree(
        package_src,
        package_dst,
        ignore=shutil.ignore_patterns("tests", "__pycache__", "*.so", "*.pyc"),
    )
    return package_dst


def write_setup(dest):
    setup_path = os.path.join(dest, "setup_mypyc.py")
    with open(setup_path, "w") as f:
        f.write("import os\n")
        f.write(SETUP_TEMPLATE)
    return setup_path


def build(dest, python_version, use_uv):
    setup_path = write_setup(dest)
    build_cmd = [os.path.basename(setup_path), "build_ext", "--inplace"]
    if use_uv:
        cmd = [
            "uv",
            "run",
            "--no-project",
            "--python",
            python_version,
            "--with",
            "mypy",
            "--with",
            "setuptools",
            "--with",
            "packaging>=24.2",
            "python",
        ] + build_cmd
    else:
        cmd = [sys.executable] + build_cmd
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, cwd=dest, check=True)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--dest",
        default=os.path.join(REPO_ROOT, "build", "mypyc"),
        help="output directory for the compiled tree (default: <repo>/build/mypyc)",
    )
    default_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    parser.add_argument(
        "--python",
        default=default_version,
        help=(
            "Python version to compile for via uv (default: this interpreter, "
            f"{default_version}). Benchmark the result with a matching interpreter."
        ),
    )
    parser.add_argument(
        "--no-uv",
        action="store_true",
        help="build with the current interpreter instead of uv "
        "(it must provide mypy and setuptools)",
    )
    args = parser.parse_args()

    dest = os.path.abspath(args.dest)
    copy_package(dest)
    build(dest, args.python, use_uv=not args.no_uv)

    suffix = sysconfig.get_config_var("EXT_SUFFIX") or ".so"
    pattern = os.path.join(dest, "pyperplan", "**", f"*{suffix}")
    compiled = glob.glob(pattern, recursive=True)
    print(f"\nCompiled {len(compiled)} extension modules into {dest}")
    print(f"Benchmark it with: --src {os.path.relpath(dest)}")


if __name__ == "__main__":
    main()
