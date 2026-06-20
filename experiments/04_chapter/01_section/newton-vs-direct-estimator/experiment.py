# ---
# description: RSE comparison of kQSketch Newton-Raphson vs Direct estimator across Lambda and m
# ---
"""
Compares the relative standard error of Newton-Cold, Newton-Warm, and Direct
estimators for kQSketch with k=2 and b=8 bits.

Left subplot:  RSE vs log10(Lambda) at fixed m=400
Right subplot: RSE vs m at fixed Lambda=1000
"""

import numpy as np
import tqdm

from weighted_cardinality_estimation import kQSketch, stat
from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager
from data_for_figure_dataclass import DataModel

# REVIEWED AND ACCEPTED DRAFT VARIABLES. RSE comparison of 3 estimators; 1000 reps gives stable curves.
# BENCHMARK: DRAFT=0: >80s, DRAFT=1: 21.0s, DRAFT=2: 1.7s.
match DRAFT:
    case DraftLevel.DRAFT_FINAL_VERSION:
        N_REPS = 5000
        N_POINTS = 100
    case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
        N_REPS = 100
        N_POINTS = 40
    case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
        N_REPS = 10
        N_POINTS = 10

K = 2.0
B_BITS = 8
M_FIXED = 400
LAMBDA_FIXED = 1000.0
M_RANGE = (100, 400)
LAMBDA_RANGE = (-40, 40)  # log10 scale: 10^-40 to 10^40


def rse_at(m: int, lam: float, n_reps: int) -> tuple[float, float, float]:
    """Return (rse_direct, rse_newton_cold, rse_newton_warm)."""
    errs_d, errs_c, errs_w = [], [], []
    for rep in range(n_reps):
        sk = kQSketch(m, seed=rep, amount_bits=B_BITS, logarithm_base=K)
        elems, weights = stat.weighted_stream(100, lam, dist=stat.Constant())
        sk.add_many(elems, weights)
        errs_d.append(stat.relative_error(sk.estimate_direct(), lam))
        try:
            errs_c.append(stat.relative_error(sk.estimate_newton_cold(), lam))
        except RuntimeError:
            errs_c.append(np.nan)
        try:
            errs_w.append(stat.relative_error(sk.estimate_newton_warm(), lam))
        except RuntimeError:
            errs_w.append(np.nan)
    return float(np.nanstd(errs_d)), float(np.nanstd(errs_c)), float(np.nanstd(errs_w))



def main() -> None:
    out = GeneratedOutputManager(__file__)

    exponents = np.linspace(LAMBDA_RANGE[0], LAMBDA_RANGE[1], N_POINTS)
    lambdas = 10.0**exponents
    ms = np.linspace(M_RANGE[0], M_RANGE[1], N_POINTS, dtype=int)

    rse_d1, rse_c1, rse_w1 = [], [], []
    rse_d2, rse_c2, rse_w2 = [], [], []
    tasks = [("lam", lam) for lam in lambdas] + [("m", int(m)) for m in ms]
    TOTAL_PBAR_VALUE = len(tasks)
    pbar = tqdm.tqdm(total=TOTAL_PBAR_VALUE, desc="Newton vs Direct RSE", colour="blue", unit="pt", mininterval=10.0)
    for kind, val in tasks:
        if kind == "lam":
            d, c, w = rse_at(M_FIXED, val, N_REPS)
            rse_d1.append(d)
            rse_c1.append(c)
            rse_w1.append(w)
        else:
            d, c, w = rse_at(val, LAMBDA_FIXED, N_REPS)
            rse_d2.append(d)
            rse_c2.append(c)
            rse_w2.append(w)
        pbar.update(1)
    pbar.close()

    out.save_dataclass(DataModel(
        exponents=exponents.tolist(),
        rse_d1=rse_d1,
        rse_c1=rse_c1,
        rse_w1=rse_w1,
        ms=ms.tolist(),
        rse_d2=rse_d2,
        rse_c2=rse_c2,
        rse_w2=rse_w2,
        m_fixed=M_FIXED,
        lam_fixed=LAMBDA_FIXED,
        n_reps=N_REPS,
        k=K,
        b_bits=B_BITS,
    ), DataModel)


if __name__ == "__main__":
    main()
