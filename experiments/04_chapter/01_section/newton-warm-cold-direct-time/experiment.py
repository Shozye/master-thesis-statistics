# ---
# description: Estimation time and Newton iteration counts for Direct, Cold, and Warm vs m
# ---
"""
Left subplot:   Wall-clock estimation time vs m (fixed Lambda=1000)
Middle subplot: Newton-Raphson iteration count vs m (fixed Lambda=1000)
Right subplot:  Newton-Raphson iteration count vs Lambda (fixed m=400)
"""

import time
import numpy as np
import tqdm

from weighted_cardinality_estimation import kQSketch, stat
from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager
from data_for_figure_dataclass import DataModel

# REVIEWED AND ACCEPTED DRAFT VARIABLES. Timing measurement; 300 reps sufficient for stable mean timing.
# BENCHMARK: DRAFT=0: >80s, DRAFT=1: 13.2s, DRAFT=2: 1.1s.
match DRAFT:
    case DraftLevel.DRAFT_FINAL_VERSION:
        N_REPS = 2000
        N_POINTS = 100
    case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
        N_REPS = 40
        N_POINTS = 50
    case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
        N_REPS = 3
        N_POINTS = 8

K = 2.0
B_BITS = 8
LAMBDA_FIXED = 1000.0
M_FIXED = 400
M_RANGE = (100, 400)
LAMBDA_RANGE = (-40, 40)  # log10 scale: 10^-40 to 10^40


def measure_at(m: int, lam: float, n_reps: int) -> dict[str, float]:
    """Return avg time and avg iterations for each estimator."""
    t_d, t_c, t_w = 0.0, 0.0, 0.0
    iters_c, iters_w = 0, 0
    for rep in range(n_reps):
        sk = kQSketch(m, seed=rep, amount_bits=B_BITS, logarithm_base=K)
        elems, weights = stat.weighted_stream(100, lam, dist=stat.Constant())
        sk.add_many(elems, weights)

        t0 = time.perf_counter()
        sk.estimate_direct()
        t_d += time.perf_counter() - t0

        t0 = time.perf_counter()
        try:
            sk.estimate_newton_cold()
            t_c += time.perf_counter() - t0
            iters_c += sk.estimate_newton_cold_iterations()
        except RuntimeError:
            t_c += time.perf_counter() - t0
            iters_c += 1000

        t0 = time.perf_counter()
        try:
            sk.estimate_newton_warm()
            t_w += time.perf_counter() - t0
            iters_w += sk.estimate_newton_warm_iterations()
        except RuntimeError:
            t_w += time.perf_counter() - t0
            iters_w += 1000

    return {
        "time_direct": t_d / n_reps,
        "time_cold": t_c / n_reps,
        "time_warm": t_w / n_reps,
        "iters_cold": iters_c / n_reps,
        "iters_warm": iters_w / n_reps,
    }



def main() -> None:
    out = GeneratedOutputManager(__file__)

    ms = np.linspace(M_RANGE[0], M_RANGE[1], N_POINTS, dtype=int)
    exponents = np.linspace(LAMBDA_RANGE[0], LAMBDA_RANGE[1], N_POINTS)
    lambdas = 10.0**exponents

    res_m = {k: [] for k in ["time_direct", "time_cold", "time_warm", "iters_cold", "iters_warm"]}
    res_lam = {k: [] for k in ["iters_cold", "iters_warm"]}

    tasks = [("m", int(m)) for m in ms] + [("lam", lam) for lam in lambdas]
    TOTAL_PBAR_VALUE = len(tasks)
    pbar = tqdm.tqdm(total=TOTAL_PBAR_VALUE, desc="Time & iterations", colour="blue", unit="pt", mininterval=10.0)
    for kind, val in tasks:
        if kind == "m":
            r = measure_at(val, LAMBDA_FIXED, N_REPS)
            for k in res_m:
                res_m[k].append(r[k])
        else:
            r = measure_at(M_FIXED, val, N_REPS)
            for k in res_lam:
                res_lam[k].append(r[k])
        pbar.update(1)
    pbar.close()

    out.save_dataclass(DataModel(
        ms=ms.tolist(),
        time_direct=res_m["time_direct"],
        time_cold=res_m["time_cold"],
        time_warm=res_m["time_warm"],
        iters_cold_m=res_m["iters_cold"],
        iters_warm_m=res_m["iters_warm"],
        exponents=exponents.tolist(),
        iters_cold_lam=res_lam["iters_cold"],
        iters_warm_lam=res_lam["iters_warm"],
        lam_fixed=LAMBDA_FIXED,
        m_fixed=M_FIXED,
        n_reps=N_REPS,
        k=K,
        b_bits=B_BITS,
    ), DataModel)


if __name__ == "__main__":
    main()
