# ---
# description: RSE comparison of FastExpSketchCustomFloat(p=7,q=8) vs ExpSketchFloat32 across Lambda range
# ---
"""
Experiment: Show that FastExpSketchCustomFloat with p=7, q=8 (15-bit register)
produces identical accuracy to FastExpSketchFloat32 (32-bit register) across the
full Lambda range where both are valid.
"""

import numpy as np
import tqdm

from weighted_cardinality_estimation import FastExpSketchFloat32, FastExpSketchCustomFloat, stat
from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager
from data_for_figure_dataclass import DataModel

# REVIEWED AND ACCEPTED DRAFT VARIABLES. RSE estimation needs many reps for stable curves.
# BENCHMARK: DRAFT=0: ~300s, DRAFT=1: ~35s, DRAFT=2: ~3s.
match DRAFT:
    case DraftLevel.DRAFT_FINAL_VERSION:
        N_REPS = 10000
        N_LAMBDAS = 50
    case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
        N_REPS = 100
        N_LAMBDAS = 20
    case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
        N_REPS = 20
        N_LAMBDAS = 15

M = 400
P = 7
Q = 8
N_ELEMENTS = 500
LOG_LAMBDAS = np.linspace(-10, 10, N_LAMBDAS)
LAMBDA_VALUES = (10.0**LOG_LAMBDAS).tolist()


def measure_rse_custom(lam: float) -> float:
    errors = []
    for rep in range(N_REPS):
        elems, weights = stat.weighted_stream(N_ELEMENTS, lam, dist=stat.Uniform())
        sk = FastExpSketchCustomFloat(M, seed=rep, exp_bits=Q, mant_bits=P)
        sk.add_many(elems, weights)
        errors.append(stat.relative_error(sk.estimate(), lam))
    return float(np.sqrt(np.mean(np.array(errors) ** 2)))


def measure_rse_float32(lam: float) -> float:
    errors = []
    for rep in range(N_REPS):
        elems, weights = stat.weighted_stream(N_ELEMENTS, lam, dist=stat.Uniform())
        sk = FastExpSketchFloat32(M, seed=rep)
        sk.add_many(elems, weights)
        errors.append(stat.relative_error(sk.estimate(), lam))
    return float(np.sqrt(np.mean(np.array(errors) ** 2)))


def main() -> None:
    out = GeneratedOutputManager(__file__)

    rse_custom = []
    rse_f32 = []
    TOTAL_PBAR_VALUE = len(LAMBDA_VALUES)
    pbar = tqdm.tqdm(total=TOTAL_PBAR_VALUE, desc="Lambda sweep", colour="#e377c2", unit="pt", mininterval=10.0)
    for lam in LAMBDA_VALUES:
        rse_custom.append(measure_rse_custom(lam))
        rse_f32.append(measure_rse_float32(lam))
        pbar.update(1)
    pbar.close()

    out.save_dataclass(
        DataModel(
            log_lambdas=LOG_LAMBDAS.tolist(),
            rse_custom_float=rse_custom,
            rse_float32=rse_f32,
            p=P,
            q=Q,
            m=M,
        ),
        DataModel,
    )


if __name__ == "__main__":
    main()
