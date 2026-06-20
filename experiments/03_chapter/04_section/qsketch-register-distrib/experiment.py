# ---
# description: QSketch register value distribution histogram vs theoretical trimmed PMF
# ---
"""
Experiment: QSketch register value distribution.

Two subplots showing how QSketch doesn't use its register range well:
  (a) QSketch b=7, Lambda=1e6
  (b) QSketch b=5, Lambda=1e6

Each subplot: histogram of empirical register values + theoretical trimmed PMF overlay.

Output: generated_output/03_chapter/qsketch_internal_structure/
"""

import numpy as np
import tqdm

from weighted_cardinality_estimation import QSketch
from weighted_cardinality_estimation.stat import weighted_stream, Constant
from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager
from data_for_figure_dataclass import DataModel

# REVIEWED AND ACCEPTED DRAFT VARIABLES. Histogram with M=500 registers × 2000 reps = 1M samples; sufficient for smooth histogram.
# BENCHMARK: DRAFT=0: 15.5s, DRAFT=1: 4.7s, DRAFT=2: 1.6s.
match DRAFT:
    case DraftLevel.DRAFT_FINAL_VERSION:
        N_REPS = 2000
        M = 500
    case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
        N_REPS = 500
        M = 450
    case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
        N_REPS = 80
        M = 500

LAMBDA_VAL = 1e6
N_ELEMENTS = 500


def get_registers(sketch: QSketch) -> list[int]:
    """Extract register values via pickle state."""
    return sketch.__getstate__()[3]


def collect_registers(b: int) -> np.ndarray:
    """Run N_REPS sketches and collect all register values."""
    all_regs = []
    TOTAL_PBAR_VALUE = N_REPS
    pbar = tqdm.tqdm(total=TOTAL_PBAR_VALUE, desc=f"b={b}", colour="blue", unit="trial", mininterval=10.0)
    for trial in range(N_REPS):
        s = QSketch(M, seed=trial, amount_bits=b)
        elems, weights = weighted_stream(N_ELEMENTS, LAMBDA_VAL, Constant())
        s.add_many(elems, weights)
        all_regs.extend(get_registers(s))
        pbar.update(1)
    pbar.close()
    return np.array(all_regs)


def trimmed_pmf(b: int, lam: float) -> tuple[np.ndarray, np.ndarray]:
    """Theoretical trimmed PMF for QSketch register values."""
    r_min = -(2 ** (b - 1) - 1)
    r_max = 2 ** (b - 1) - 1
    values = np.arange(r_min, r_max + 1)
    probs = np.zeros(len(values))

    for i, v in enumerate(values):
        if v == r_min:
            # Left tail: P(true value <= r_min) = exp(-lam * 2^(-r_min))
            probs[i] = np.exp(-lam * 2.0 ** (-r_min))
        elif v == r_max:
            # Right tail (trimmed): P(true value >= r_max) = 1 - exp(-lam * 2^(-r_max))
            probs[i] = 1.0 - np.exp(-lam * 2.0 ** (-r_max))
        else:
            probs[i] = np.exp(-lam * 2.0 ** (-(v + 1))) - np.exp(-lam * 2.0 ** (-v))

    return values, probs


def main() -> None:
    out = GeneratedOutputManager(__file__)

    regs_7 = collect_registers(7)
    regs_5 = collect_registers(5)

    out.save_dataclass(
        DataModel(m=M, n_reps=N_REPS, lambda_val=LAMBDA_VAL, regs_7=regs_7.tolist(), regs_5=regs_5.tolist()),
        DataModel,
    )


if __name__ == "__main__":
    main()
