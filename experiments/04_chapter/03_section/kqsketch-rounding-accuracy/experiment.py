# ---
# description: RSE comparison of kQSketchRounding vs ExpSketch vs QSketch vs kQSketch across Lambda range
# ---
"""Parallelism: set the WORKERS env var (e.g. WORKERS=8) to fan the per-Lambda RSE
computations out over a process pool. Each Lambda point is an independent task; the
tqdm bar advances as points complete (per-Lambda granularity, since worker processes
cannot update the parent's bar directly). The seed list is precomputed and passed to
every task, so the result is identical regardless of how many workers run or the order
points finish in."""

import os

import numpy as np
import tqdm

from weighted_cardinality_estimation import ExpSketch, kQSketch, kQSketchRounding, stat
from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager
from data_for_figure_dataclass import DataModel

# REVIEWED AND ACCEPTED DRAFT VARIABLES. RSE comparison across Lambda range; 3000 reps for smooth curves.
# BENCHMARK: DRAFT=0: 54.1s, DRAFT=1: 4.1s, DRAFT=2: 1.1s.
match DRAFT:
    case DraftLevel.DRAFT_FINAL_VERSION:
        N_REPS = 500000
        N_POINTS = 50
    case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
        N_REPS = 300
        N_POINTS = 50
    case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
        N_REPS = 20
        N_POINTS = 20

M = 100
K = 2.0
B_BITS = 8

WORKERS = int(os.environ.get("WORKERS", "16"))


def rse_at(lam: float, seeds: list[int]) -> tuple[float, float, float, float]:
    """Return (rse_exp, rse_kqsk, rse_round, rse_round_corrected)."""
    errs_exp, errs_kqsk, errs_round, errs_round_corrected = [], [], [], []
    for seed in seeds:
        sk_exp = ExpSketch(M, seed=seed)
        sk_exp.add("elem", lam)
        errs_exp.append(stat.relative_error(sk_exp.estimate(), lam))

        sk_kqsk = kQSketch(M, seed=seed, amount_bits=B_BITS, logarithm_base=K)
        sk_kqsk.add("elem", lam)
        try:
            errs_kqsk.append(stat.relative_error(sk_kqsk.estimate_newton_warm(), lam))
        except RuntimeError:
            errs_kqsk.append(np.nan)

        sk_round = kQSketchRounding(M, seed=seed, amount_bits=B_BITS, logarithm_base=K)
        sk_round.add("elem", lam)
        errs_round.append(stat.relative_error(sk_round.estimate(), lam))
        errs_round_corrected.append(stat.relative_error(sk_round.estimate_corrected(), lam))

    return (
        stat.compute_rse(errs_exp),
        stat.compute_rse(errs_kqsk),
        stat.compute_rse(errs_round),
        stat.compute_rse(errs_round_corrected),
    )


def _lambda_task(args):
    """One Lambda point: returns (idx, rse_exp, rse_kqsk, rse_round, rse_round_corrected)."""
    idx, lam, seeds = args
    e, k, r, rc = rse_at(lam, seeds)
    return (idx, e, k, r, rc)


def main() -> None:
    out = GeneratedOutputManager(__file__)

    seeds = stat.make_seeds(N_REPS, seed=6312)

    exponents = np.linspace(-8, 8, N_POINTS)
    lambdas = 10.0**exponents

    rse_exp = [0.0] * len(lambdas)
    rse_kqsk = [0.0] * len(lambdas)
    rse_round = [0.0] * len(lambdas)
    rse_round_corrected = [0.0] * len(lambdas)

    tasks = [(idx, lam, seeds) for idx, lam in enumerate(lambdas)]

    TOTAL_PBAR_VALUE = len(lambdas)
    pbar = tqdm.tqdm(
        total=TOTAL_PBAR_VALUE,
        desc=f"kQSketchRounding RSE vs Lambda (workers={WORKERS})",
        colour="red",
        unit="lam",
        mininterval=10.0,
    )

    def store(result) -> None:
        idx, e, k, r, rc = result
        rse_exp[idx] = e
        rse_kqsk[idx] = k
        rse_round[idx] = r
        rse_round_corrected[idx] = rc
        pbar.update(1)

    if WORKERS > 1:
        from concurrent.futures import ProcessPoolExecutor, as_completed

        with ProcessPoolExecutor(max_workers=WORKERS) as executor:
            futures = [executor.submit(_lambda_task, args) for args in tasks]
            for future in as_completed(futures):
                store(future.result())
    else:
        for args in tasks:
            store(_lambda_task(args))

    pbar.close()

    out.save_dataclass(DataModel(
        exponents=exponents.tolist(),
        rse_exp=rse_exp,
        rse_kqsk=rse_kqsk,
        rse_round=rse_round,
        rse_round_corrected=rse_round_corrected,
        m=M,
        k=K,
        b_bits=B_BITS,
        n_reps=N_REPS,
    ), DataModel)


if __name__ == "__main__":
    main()
