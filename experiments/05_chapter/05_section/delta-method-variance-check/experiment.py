# ---
# description: Empirical RSE of kQSketch and kQSketchRounding direct estimators vs the delta-method variance guarantee, swept over m and over k
# ---
"""
Validates the delta-method variance guarantees derived in the appendix for the
direct estimators of kQSketch (floor quantization) and kQSketchRounding
(rounding quantization).

Both estimators share the predicted variance coefficient
    c(k) = (k+1) ln(k) / (k-1) - 1,
so their relative standard error obeys RSE(k, m) = sqrt(c(k) / m).

Left subplot:  empirical RSE vs m at fixed k, against the theory line sqrt(c(k)/m).
Right subplot: empirical RSE * sqrt(m) vs k at fixed m, against the theory line sqrt(c(k)).
"""

import numpy as np
import tqdm

from weighted_cardinality_estimation import kQSketch, kQSketchRounding, stat
from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager
from data_for_figure_dataclass import DataModel

# REVIEWED AND ACCEPTED DRAFT VARIABLES. RSE needs many reps for a stable std estimate.
# BENCHMARK: DRAFT=0: ~70s, DRAFT=1: ~9s, DRAFT=2: ~1s.
match DRAFT:
    case DraftLevel.DRAFT_FINAL_VERSION:
        N_REPS = 5000
        N_POINTS = 12
    case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
        N_REPS = 400
        N_POINTS = 10
    case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
        N_REPS = 20
        N_POINTS = 5

K_FIXED = 2.0
B_BITS = 8
M_FIXED = 1000
LAMBDA = 1000.0  # large enough to keep registers off the bottom clamp (matches the continuous model)
N_STREAM = 100
M_RANGE = (50, 2000)
K_RANGE = (1.1, 2.4)  # delta-method approximation is stated for k <= 2.4


def empirical_rse(sketch_cls, m: int, k: float, n_reps: int) -> float:
    """Std of the relative error of the direct estimator over n_reps trials."""
    rels = np.empty(n_reps)
    for rep in range(n_reps):
        sk = sketch_cls(m, seed=rep, amount_bits=B_BITS, logarithm_base=k)
        elems, weights = stat.weighted_stream(N_STREAM, LAMBDA, dist=stat.Constant(), seed=rep)
        sk.add_many(elems, weights)
        rels[rep] = sk.estimate_direct() / LAMBDA - 1.0
    return float(np.std(rels))


def main() -> None:
    out = GeneratedOutputManager(__file__)

    ms = np.unique(np.geomspace(M_RANGE[0], M_RANGE[1], N_POINTS).astype(int))
    ks = np.linspace(K_RANGE[0], K_RANGE[1], N_POINTS)

    tasks = [("m", int(m)) for m in ms] + [("k", float(k)) for k in ks]
    TOTAL_PBAR_VALUE = len(tasks)
    pbar = tqdm.tqdm(total=TOTAL_PBAR_VALUE, desc="Delta-method RSE validation",
                     colour="magenta", unit="pt", mininterval=10.0)

    rse_floor_m, rse_round_m = [], []
    rse_floor_k, rse_round_k = [], []
    for kind, val in tasks:
        if kind == "m":
            rse_floor_m.append(empirical_rse(kQSketch, val, K_FIXED, N_REPS))
            rse_round_m.append(empirical_rse(kQSketchRounding, val, K_FIXED, N_REPS))
        else:
            rse_floor_k.append(empirical_rse(kQSketch, M_FIXED, val, N_REPS))
            rse_round_k.append(empirical_rse(kQSketchRounding, M_FIXED, val, N_REPS))
        pbar.update(1)
    pbar.close()

    out.save_dataclass(DataModel(
        ms=ms.tolist(),
        rse_floor_m=rse_floor_m,
        rse_round_m=rse_round_m,
        ks=ks.tolist(),
        rse_floor_k=rse_floor_k,
        rse_round_k=rse_round_k,
        m_fixed=M_FIXED,
        lam=LAMBDA,
        k_fixed=K_FIXED,
        b_bits=B_BITS,
        n_stream=N_STREAM,
        n_reps=N_REPS,
    ), DataModel)


if __name__ == "__main__":
    main()
