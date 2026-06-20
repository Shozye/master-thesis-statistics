# ---
# description: RSE of kQSketchShifted vs k for b={5,6,7}, m=400, Lambda=1, n=10
# ---
"""RSE of kQSketchShifted as a function of k for multiple bit widths."""

import multiprocessing

import numpy as np
import tqdm

from weighted_cardinality_estimation import kQSketchShifted, QSketch
from weighted_cardinality_estimation.stat import weighted_stream, Uniform, relative_error
from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager
from data_for_figure_dataclass import BResult, DataModel

M = 400
LAMBDA = 1.0
N_ELEMS = 10
B_VALUES = [5, 6, 7]


def _run_b(args):
    b, k_values, n_reps = args
    rng = np.random.default_rng()
    rse_newton = []
    for k in k_values:
        errors = []
        for _ in range(n_reps):
            sk = kQSketchShifted(
                M, seed=int(rng.integers(2**31)), amount_bits=b, logarithm_base=float(k)
            )
            elems, weights = weighted_stream(N_ELEMS, LAMBDA, Uniform())
            sk.add_many(elems, weights)
            errors.append(relative_error(sk.estimate_newton_warm(), LAMBDA))
        rse_newton.append(float(np.sqrt(np.mean(np.array(errors) ** 2))))
    return b, rse_newton


def _run_qsketch(n_reps):
    rng = np.random.default_rng()
    q_errors = []
    for _ in range(n_reps):
        sk = QSketch(M, seed=int(rng.integers(2**31)), amount_bits=8)
        elems, weights = weighted_stream(N_ELEMS, LAMBDA, Uniform())
        sk.add_many(elems, weights)
        q_errors.append(relative_error(sk.estimate(), LAMBDA))
    return float(np.sqrt(np.mean(np.array(q_errors) ** 2)))


def main():
    out = GeneratedOutputManager(__file__)

    # REVIEWED AND ACCEPTED DRAFT VARIABLES. RSE vs k with N_ELEMS=10 (noisy regime); 20K reps gives ~0.7% RSE estimation error.
    # BENCHMARK: DRAFT=0: >80s, DRAFT=1: 39.0s, DRAFT=2: 1.7s.
    match DRAFT:
        case DraftLevel.DRAFT_FINAL_VERSION:
            n_reps = 50000
            n_points = 50
        case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
            n_reps = 3500
            n_points = 10
        case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
            n_reps = 50
            n_points = 5

    k_values = list(np.linspace(1.2, 2.4, n_points).round(4))

    tasks = [(b, k_values, n_reps) for b in B_VALUES]

    with multiprocessing.Pool(len(B_VALUES) + 1) as pool:
        qsketch_future = pool.apply_async(_run_qsketch, (n_reps,))
        b_futures = pool.map(_run_b, tasks)
        rse_qsketch = qsketch_future.get()

    b_results = [
        BResult(b=b, rse_newton=rse_newton, rse_qsketch=rse_qsketch)
        for b, rse_newton in b_futures
    ]

    out.save_dataclass(
        DataModel(
            k_values=k_values,
            b_results=b_results,
            n_reps=n_reps,
            m=M,
            lam=LAMBDA,
            n_elems=N_ELEMS,
        ),
        DataModel,
    )


if __name__ == "__main__":
    main()
