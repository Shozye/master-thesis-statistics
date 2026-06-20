# ---
# description: Mean relative error vs Lambda for float types and QSketch bit widths
# ---
"""
Experiment: Relative error comparison across float types and QSketch bit widths.

Sweeps Lambda from 10^-300 to 10^300 and measures mean relative error for:
  - ExpSketch float16 (simulated)
  - ExpSketch float32 (FastExpSketchFloat32)
  - ExpSketch float64 (ExpSketch)
  - QSketch b=6, b=9, b=12

Parameters: m=50.

Output: generated_output/03_chapter/float_bits_error_comparison/
"""

import numpy as np
import tqdm

from weighted_cardinality_estimation import (
    FastExpSketchFloat32,
    FastExpSketch,
    QSketch,
    stat,
)
from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager
from data_for_figure_dataclass import DataModel

# REVIEWED AND ACCEPTED DRAFT VARIABLES. MRE sweep across Lambda; 300 reps sufficient for comparison curves.
# BENCHMARK: DRAFT=0: >80s, DRAFT=1: 10.4s, DRAFT=2: 1.3s.
match DRAFT:
    case DraftLevel.DRAFT_FINAL_VERSION:
        N_REPS = 1000
        N_POINTS = 200
    case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
        N_REPS = 50
        N_POINTS = 50
    case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
        N_REPS = 5
        N_POINTS = 10

# --- Experiment parameters ---
M = 50
EXP_MIN, EXP_MAX = -321, 308
EXPONENTS = np.linspace(EXP_MIN, EXP_MAX, N_POINTS)
LAMBDAS = 10.0**EXPONENTS


def _capped_error(estimate: float, lam: float) -> float:
    err = stat.relative_error(estimate, lam)
    return 10.0 if not np.isfinite(err) else min(err, 10.0)


def mre_fastexpsketch_float32(elems: list[str], weights: list[float], lam: float) -> float:
    errors = []
    for trial in range(N_REPS):
        s = FastExpSketchFloat32(M, seed=trial)
        s.add_many(elems, weights)
        errors.append(_capped_error(s.estimate(), lam))
    return float(np.mean(errors))


def mre_fastexpsketch(elems: list[str], weights: list[float], lam: float) -> float:
    errors = []
    for trial in range(N_REPS):
        s = FastExpSketch(M, seed=trial)
        s.add_many(elems, weights)
        errors.append(_capped_error(s.estimate(), lam))
    return float(np.mean(errors))


def mre_qsketch(elems: list[str], weights: list[float], lam: float, b: int) -> float:
    errors = []
    for trial in range(N_REPS):
        s = QSketch(M, seed=trial, amount_bits=b)
        s.add_many(elems, weights)
        errors.append(_capped_error(s.estimate(), lam))
    return float(np.mean(errors))


def main() -> None:
    out = GeneratedOutputManager(__file__)

    configs = [
        (
            "FastExpSketch float32",
            "#1f77b4",
            "-",
            lambda e, w, l: mre_fastexpsketch_float32(e, w, l),
        ),
        ("FastExpSketch float64", "#2ca02c", "-", lambda e, w, l: mre_fastexpsketch(e, w, l)),
        (r"QSketch $b=6$", "#ff7f0e", "--", lambda e, w, l: mre_qsketch(e, w, l, 6)),
        (r"QSketch $b=7$", "#d62728", "--", lambda e, w, l: mre_qsketch(e, w, l, 7)),
        (r"QSketch $b=8$", "#9467bd", "--", lambda e, w, l: mre_qsketch(e, w, l, 8)),
        (r"QSketch $b=9$", "#8c564b", "--", lambda e, w, l: mre_qsketch(e, w, l, 9)),
        (r"QSketch $b=10$", "#e377c2", "--", lambda e, w, l: mre_qsketch(e, w, l, 10)),
        (r"QSketch $b=11$", "#7f7f7f", "--", lambda e, w, l: mre_qsketch(e, w, l, 11)),
        (r"QSketch $b=12$", "#bcbd22", "--", lambda e, w, l: mre_qsketch(e, w, l, 12)),
    ]

    all_errors = []
    TOTAL_PBAR_VALUE = len(configs)
    pbar = tqdm.tqdm(total=TOTAL_PBAR_VALUE, desc="float vs qsketch sweep", colour="red", unit="config", mininterval=10.0)
    for label, color, ls, fn in configs:
        errors = []
        for lam in LAMBDAS:
            elems, weights = stat.weighted_stream(100, lam, dist=stat.Constant())
            errors.append(fn(elems, weights, lam))
        all_errors.append(errors)
        pbar.update(1)
    pbar.close()

    out.save_dataclass(
        DataModel(
            exponents=EXPONENTS.tolist(),
            errors=all_errors,
            labels=[c[0] for c in configs],
            colors=[c[1] for c in configs],
            linestyles=[c[2] for c in configs],
            m=M,
            n_reps=N_REPS,
            exp_min=EXP_MIN,
            exp_max=EXP_MAX,
        ),
        DataModel,
    )


if __name__ == "__main__":
    main()
