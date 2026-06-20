"""Run all experiment scripts in parallel using multiprocessing."""

import subprocess
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import matplotlib
from tabulate import tabulate


EXPERIMENTS_DIR = Path(__file__).parent
WORKERS = 8


def run_script(script: Path) -> tuple[Path, int, float]:
    start = time.monotonic()
    result = subprocess.run([sys.executable, str(script)], cwd=EXPERIMENTS_DIR.parent)
    elapsed = time.monotonic() - start
    return script, result.returncode, elapsed


def main() -> None:
    scripts = sorted(
        EXPERIMENTS_DIR.rglob("experiment.py"),
        key=lambda p: (p.relative_to(EXPERIMENTS_DIR).parts[0], p.name),
    )
    if not scripts:
        print("No experiment scripts found.")
        return

    print(f"Running {len(scripts)} experiments with {WORKERS} workers...\n")
    total_start = time.monotonic()

    rows = []
    with Pool(WORKERS) as pool:
        for script, code, elapsed in pool.imap_unordered(run_script, scripts):
            rel = script.relative_to(EXPERIMENTS_DIR)
            chapter = rel.parts[0]
            exp_name = rel.parts[-2]  # parent directory name
            if code == 0:
                status = "\033[32m✓ PASS\033[0m"
            else:
                status = f"\033[31m✗ FAIL ({code})\033[0m"
            print(f"  {status}  {chapter}/{exp_name}  ({elapsed:.1f}s)")
            rows.append([chapter, exp_name, status, f"{elapsed:.1f}"])

    total = time.monotonic() - total_start
    rows.sort()

    # Color time using matplotlib RdYlGn colormap (green=fast, red=slow)
    times = [float(r[3]) for r in rows]
    t_min, t_max = min(times), max(times)
    cmap = matplotlib.colormaps["RdYlGn_r"]

    def color_time(val: str) -> str:
        t = float(val)
        norm = (t - t_min) / (t_max - t_min) if t_max > t_min else 0.0
        r, g, b, _ = cmap(norm)
        return f"\033[38;2;{int(r * 255)};{int(g * 255)};{int(b * 255)}m{val}\033[0m"

    for r in rows:
        r[3] = color_time(r[3])

    print()
    print(
        tabulate(
            rows,
            headers=["Chapter", "Experiment", "Status", "Time (s)"],
            tablefmt="rounded_outline",
            colalign=("left", "left", "left", "center"),
        )
    )

    passed = sum(1 for r in rows if "PASS" in r[2])
    failed = len(rows) - passed
    print(f"\n✓ {passed} passed, ✗ {failed} failed  (total {total:.1f}s)")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
