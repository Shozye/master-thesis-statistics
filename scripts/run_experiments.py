"""Run experiment scripts matching a pattern in parallel.

Usage:
    python scripts/run_experiments.py <pattern> [--workers N] [--mode experiment|figure]

Pattern matches against experiment directory paths (substring match).
If pattern matches multiple experiments, they run in parallel.
"""

import argparse
import subprocess
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import matplotlib
from tabulate import tabulate

EXPERIMENTS_DIR = Path(__file__).resolve().parent.parent / "experiments"
DEFAULT_WORKERS = 8


def find_experiments(pattern: str) -> list[Path]:
    all_dirs = sorted(
        d for d in EXPERIMENTS_DIR.rglob("experiment.py")
    )
    return [d for d in all_dirs if pattern in str(d.relative_to(EXPERIMENTS_DIR.parent))]


def run_script(args: tuple[Path, str]) -> tuple[Path, int, float]:
    script, mode = args
    target = script if mode == "experiment" else script.parent / "create_figure.py"
    start = time.monotonic()
    result = subprocess.run([sys.executable, str(target)], cwd=EXPERIMENTS_DIR.parent)
    elapsed = time.monotonic() - start
    return script, result.returncode, elapsed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pattern", help="Substring to match against experiment paths")
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS)
    parser.add_argument("--mode", choices=["experiment", "figure"], default="experiment")
    args = parser.parse_args()

    scripts = find_experiments(args.pattern)
    if not scripts:
        print(f"No experiments matching '{args.pattern}'")
        sys.exit(1)

    print(f"Running {len(scripts)} experiments ({args.mode}) with {args.workers} workers...\n")
    total_start = time.monotonic()

    rows = []
    tasks = [(s, args.mode) for s in scripts]
    with Pool(args.workers) as pool:
        for script, code, elapsed in pool.imap_unordered(run_script, tasks):
            rel = script.relative_to(EXPERIMENTS_DIR)
            chapter = rel.parts[0]
            exp_name = rel.parts[-2]
            status = "\033[32m✓ PASS\033[0m" if code == 0 else f"\033[31m✗ FAIL ({code})\033[0m"
            print(f"  {status}  {chapter}/{exp_name}  ({elapsed:.1f}s)")
            rows.append([chapter, exp_name, status, f"{elapsed:.1f}"])

    total = time.monotonic() - total_start
    rows.sort()

    passed = sum(1 for r in rows if "PASS" in r[2])
    failed = len(rows) - passed

    if args.mode == "figure":
        print(f"\n✓ {passed} passed, ✗ {failed} failed  (total {total:.1f}s)")
    else:
        times = [float(r[3]) for r in rows]
        t_min, t_max = min(times), max(times)
        cmap = matplotlib.colormaps["RdYlGn_r"]

        for r in rows:
            t = float(r[3])
            norm = (t - t_min) / (t_max - t_min) if t_max > t_min else 0.0
            rv, g, b, _ = cmap(norm)
            r[3] = f"\033[38;2;{int(rv * 255)};{int(g * 255)};{int(b * 255)}m{r[3]}\033[0m"

        print()
        print(
            tabulate(
                rows,
                headers=["Chapter", "Experiment", "Status", "Time (s)"],
                tablefmt="rounded_outline",
                colalign=("left", "left", "left", "center"),
            )
        )
        print(f"\n✓ {passed} passed, ✗ {failed} failed  (total {total:.1f}s)")

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
