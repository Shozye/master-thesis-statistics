# ---
# description: LogExpSketchFastNoShifted cardinality RSE vs log10(Lambda) and Jaccard RSE vs bits b over the Float32 range
# ---
"""How many bits per register b does LogExpSketch need to cover the Float32 range.

Panel (a): cardinality estimator RSE across log10(Lambda) in [-35, 35] for the
Float32 baseline (FastExpSketchFloat32) and LogExpSketchFastNoShifted with
b in {9, 10, 11}. The grid spans v_min = 1/v_max .. v_max with v_max = float32_max.
Panel (b): Jaccard estimator RSE versus b in {9..14} for several true Jaccard
values J. Theoretical horizontal lines use the ExpSketch formula sqrt((1-J)/(m*J)).
"""

import numpy as np
import tqdm
from weighted_cardinality_estimation import (
    FastExpSketchFloat32,
    LogExpSketchFastNoShifted,
    stat,
)
from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager
from data_for_figure_dataclass import DataModel

# REVIEWED AND ACCEPTED DRAFT VARIABLES. RSE over independent seeds; curves stabilise by ~500 trials.
# BENCHMARK: DRAFT=0: ~120s, DRAFT=1: ~25s, DRAFT=2: ~3s.
match DRAFT:
    case DraftLevel.DRAFT_FINAL_VERSION:
        N_TRIALS = 5000
        N_ELEMENTS = 5000
    case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
        N_TRIALS = 60
        N_ELEMENTS = 1000
    case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
        N_TRIALS = 3
        N_ELEMENTS = 100

M = 400
V_MAX = float(np.finfo(np.float32).max)  # ~3.4028235e38

# Panel (a)
LAMBDA_EXPONENTS = list(range(-35, 36))  # log10(Lambda) from -35 to 35
A_BITS = [8, 9, 10, 11]

# Panel (b)
B_VALUES = [11, 12, 13, 14, 15]
J_VALUES = [0.2, 0.5, 0.8, 0.9, 0.95]


def panel_a_rse_for_lambda(make_sketch, exponent: int) -> float:
    """RSE of the cardinality estimate for a single weighted element of weight Lambda."""
    lam = 10.0**exponent
    errors = []
    for trial in range(N_TRIALS):
        sk = make_sketch(trial)
        sk.add("x0", lam)
        errors.append((sk.estimate() - lam) / lam)
    return float(np.sqrt(np.mean(np.array(errors) ** 2)))


def panel_b_rse_for_bits(b: int, j: float) -> float:
    """RSE of the structural Jaccard estimator for LogExpSketch with b bits."""
    (a_elems, w_a), (b_elems, w_b) = stat.jaccard_streams(
        N_ELEMENTS, 1000.0, j, dist=stat.Uniform(), common=stat.CommonPlacement.RANDOM, seed=0
    )
    errors = []
    for trial in range(N_TRIALS):
        sk_a = LogExpSketchFastNoShifted(M, seed=trial, amount_bits=b, v_max=V_MAX)
        sk_b = LogExpSketchFastNoShifted(M, seed=trial, amount_bits=b, v_max=V_MAX)
        sk_a.add_many(a_elems, w_a)
        sk_b.add_many(b_elems, w_b)
        errors.append((sk_a.jaccard_struct(sk_b) - j) / j)
    return float(np.sqrt(np.mean(np.array(errors) ** 2)))


def main() -> None:
    out = GeneratedOutputManager(__file__)

    series = [("FastExpSketchFloat32", lambda t: FastExpSketchFloat32(M, seed=t))]
    for b in A_BITS:
        series.append(
            (
                f"LogExpSketch $b={b}$",
                lambda t, b=b: LogExpSketchFastNoShifted(M, seed=t, amount_bits=b, v_max=V_MAX),
            )
        )

    TOTAL_PBAR_VALUE = len(series) + len(J_VALUES)
    pbar = tqdm.tqdm(total=TOTAL_PBAR_VALUE, desc="bits sweep", colour="green", unit="series", mininterval=10.0)

    panel_a_labels = []
    panel_a_rse = []
    for label, make_sketch in series:
        panel_a_labels.append(label)
        panel_a_rse.append([panel_a_rse_for_lambda(make_sketch, e) for e in LAMBDA_EXPONENTS])
        pbar.update(1)

    panel_b_rse = []
    for j in J_VALUES:
        panel_b_rse.append([panel_b_rse_for_bits(b, j) for b in B_VALUES])
        pbar.update(1)
    pbar.close()

    out.save_dataclass(
        DataModel(
            m=M,
            v_max=V_MAX,
            log_lambdas=[float(e) for e in LAMBDA_EXPONENTS],
            panel_a_labels=panel_a_labels,
            panel_a_rse=panel_a_rse,
            b_values=B_VALUES,
            j_values=J_VALUES,
            panel_b_rse=panel_b_rse,
        ),
        DataModel,
    )


if __name__ == "__main__":
    main()
