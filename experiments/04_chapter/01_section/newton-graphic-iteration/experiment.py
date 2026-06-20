# ---
# description: Newton-Raphson graphic iteration (cobweb) of the kQSketch MLE map, contrasting cold-start and warm-start convergence to the fixed point.
# ---
"""
Single representative k-QSketch instance. We view Newton-Raphson as a
fixed-point iteration Lambda_{n+1} = g(Lambda_n) with
g(Lambda) = Lambda - f(Lambda)/f'(Lambda), where f is the score function
optimised by the estimator (see fast_k_q_sketch.cpp::ffunc_divided_by_dffunc).

Left panel data:  cold start Lambda_0 = k^{r_min}.
Right panel data: warm start Lambda_0 = direct estimator (zoom near fixed point).

For k = 2 the map is reproduced exactly in float64, so the iterate trajectory
matches the C++ library.
"""

import math

import numpy as np

from weighted_cardinality_estimation import kQSketch, stat
from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager
from data_for_figure_dataclass import DataModel

# REVIEWED AND ACCEPTED DRAFT VARIABLES. Deterministic single instance; the only
# quality knob is the resolution of the plotted Newton map curve.
# BENCHMARK: DRAFT=0: <1s, DRAFT=1: <1s, DRAFT=2: <1s.
match DRAFT:
    case DraftLevel.DRAFT_FINAL_VERSION:
        N_CURVE = 400
    case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
        N_CURVE = 200
    case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
        N_CURVE = 60

K = 2.0
B_BITS = 8
M = 256
LAMBDA_TRUE = 1.0e6
SKETCH_SEED = 0
STREAM_SEED = 0
N_STREAM = 100
NEWTON_TOL = 1e-6
NEWTON_MAX_ITER = 100


def newton_map(registers: list[int], w: float) -> float:
    """One Newton step on the score function: g(w) = w - f(w)/f'(w)."""
    ffunc = 0.0
    dffunc = 0.0
    for r in registers:
        c = K ** (-r)
        a = math.exp(-w * c)
        b = math.exp(-w * c / K)
        diff = b - a
        ffunc += (c * a - (c / K) * b) / diff
        dffunc += -((c - c / K) ** 2) * a * b / (diff * diff)
    return w - ffunc / dffunc


def trajectory(registers: list[int], w0: float) -> list[float]:
    """Iterates Lambda_0, Lambda_1, ... until the relative step is below tol."""
    xs = [w0]
    w = w0
    for _ in range(NEWTON_MAX_ITER):
        wn = newton_map(registers, w)
        xs.append(wn)
        if abs(wn - w) / abs(wn) <= NEWTON_TOL:
            break
        w = wn
    return xs


def main() -> None:
    out = GeneratedOutputManager(__file__)

    sk = kQSketch(M, seed=SKETCH_SEED, amount_bits=B_BITS, logarithm_base=K)
    elems, weights = stat.weighted_stream(
        N_STREAM, LAMBDA_TRUE, dist=stat.Constant(), seed=STREAM_SEED
    )
    sk.add_many(elems, weights)

    registers = sk.get_registers()
    cold_start = K ** min(registers)
    warm_start = sk.estimate_direct()

    cold_traj = trajectory(registers, cold_start)
    warm_traj = trajectory(registers, warm_start)
    root = cold_traj[-1]

    # Iteration counts from the library, so the figure matches the rest of the thesis.
    cold_iters = sk.estimate_newton_cold_iterations()
    warm_iters = sk.estimate_newton_warm_iterations()

    # Cold panel spans the whole staircase; warm panel zooms onto the fixed point.
    cold_lo = min(cold_traj) * 0.7
    cold_hi = max(cold_traj) * 1.3
    warm_lo = min(warm_traj) * 0.9985
    warm_hi = max(warm_traj) * 1.0010

    lam_cold = np.geomspace(cold_lo, cold_hi, N_CURVE)
    lam_warm = np.geomspace(warm_lo, warm_hi, N_CURVE)
    g_cold = [newton_map(registers, float(w)) for w in lam_cold]
    g_warm = [newton_map(registers, float(w)) for w in lam_warm]

    out.save_dataclass(DataModel(
        lam_cold=lam_cold.tolist(),
        g_cold=g_cold,
        lam_warm=lam_warm.tolist(),
        g_warm=g_warm,
        cold_traj=cold_traj,
        warm_traj=warm_traj,
        root=root,
        cold_start=cold_start,
        warm_start=warm_start,
        cold_iters=cold_iters,
        warm_iters=warm_iters,
        lambda_true=LAMBDA_TRUE,
        m=M,
        k=K,
        b_bits=B_BITS,
    ), DataModel)


if __name__ == "__main__":
    main()
