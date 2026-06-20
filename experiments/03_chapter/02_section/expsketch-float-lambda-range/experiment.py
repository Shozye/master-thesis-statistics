# ---
# description: ExpSketch float register valid Lambda range and error by float type
# ---
"""
Experiment: ExpSketch float register range and relative error.

Two side-by-side subplots:
  (a) Representable Lambda range per float type (float16, float32, float64)
  (b) Mean relative error vs Lambda for float16 (simulated), float32, float64

Output: generated_output/03_chapter/expsketch_float_range/
"""

import numpy as np
import tqdm

from weighted_cardinality_estimation import ExpSketch, FastExpSketchFloat32
from weighted_cardinality_estimation.stat import weighted_stream, Constant
from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager
from data_for_figure_dataclass import DataModel

# REVIEWED AND ACCEPTED DRAFT VARIABLES. RSE across Lambda range; 400 reps sufficient for smooth error curves.
# BENCHMARK: DRAFT=0: 57.4s, DRAFT=1: 8.0s, DRAFT=2: 1.0s.
match DRAFT:
    case DraftLevel.DRAFT_FINAL_VERSION:
        N_REPS = 2000
        N_LAMBDAS = 100
    case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
        N_REPS = 100
        N_LAMBDAS = 50
    case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
        N_REPS = 2
        N_LAMBDAS = 7

# --- Experiment parameters ---
M = 100  # sketch size
FLOAT_CONFIGS = [
    {"name": "float16", "color": "#d62728", "dtype": np.float16},
    {"name": "float32", "color": "#1f77b4", "dtype": np.float32},
    {"name": "float64", "color": "#2ca02c", "dtype": np.float64},
]

# OX axis: log10(Lambda) from -300 to 300
EXPONENTS = np.linspace(-300, 300, N_LAMBDAS)
LAMBDAS = 10.0**EXPONENTS


def lam_range_for_dtype(dtype) -> tuple[float, float]:
    fi = np.finfo(dtype)
    return 1.0 / float(fi.max), 1.0 / float(fi.tiny)


def mean_relative_error_sim(lam: float, dtype) -> float:
    """Simulate sketch with registers cast to dtype (covers float16 and float32)."""
    fi = np.finfo(dtype)
    rng = np.random.default_rng(42)
    errors = []
    for _ in range(N_REPS):
        # Draw m Exp(lam) samples, cast to dtype, clamp infinities/zeros
        regs = rng.exponential(scale=1.0 / lam, size=M).astype(dtype).astype(np.float64)
        regs = np.where(regs == 0.0, float(fi.tiny), regs)
        regs = np.where(np.isinf(regs), float(fi.max), regs)
        est = (M - 1) / np.sum(regs)
        errors.append(abs(est - lam) / lam if np.isfinite(est) and est > 0 else 1.0)
    return float(np.mean(errors))


def mean_relative_error_lib(lam: float, sketch_cls) -> float:
    """Measure relative error using actual library sketch class."""
    n_elements = 100
    elems, weights = weighted_stream(n_elements, lam, Constant())
    errors = []
    for trial in range(N_REPS):
        s = sketch_cls(M, seed=trial)
        s.add_many(elems, weights)
        est = s.estimate()
        errors.append(abs(est - lam) / lam if np.isfinite(est) and est > 0 else 1.0)
    return float(np.mean(errors))


def compute_errors() -> tuple[list[float], list[float], list[float]]:
    configs = [
        (np.float16, None),
        (np.float32, FastExpSketchFloat32),
        (np.float64, ExpSketch),
    ]
    all_errors = []
    TOTAL_PBAR_VALUE = len(configs)
    pbar = tqdm.tqdm(total=TOTAL_PBAR_VALUE, desc="float lambda range", colour="cyan", unit="config", mininterval=10.0)
    for dtype, sketch_cls in configs:
        if sketch_cls is None:
            errors = [mean_relative_error_sim(lam, dtype) for lam in LAMBDAS]
        else:
            errors = [mean_relative_error_lib(lam, sketch_cls) for lam in LAMBDAS]
        all_errors.append(errors)
        pbar.update(1)
    pbar.close()
    return all_errors[0], all_errors[1], all_errors[2]



def main() -> None:
    out = GeneratedOutputManager(__file__)

    errors_float16, errors_float32, errors_float64 = compute_errors()
    out.save_dataclass(
        DataModel(
            exponents=EXPONENTS.tolist(),
            errors_float16=errors_float16,
            errors_float32=errors_float32,
            errors_float64=errors_float64,
            m=M,
            n_reps=N_REPS,
        ),
        DataModel,
    )


if __name__ == "__main__":
    main()
