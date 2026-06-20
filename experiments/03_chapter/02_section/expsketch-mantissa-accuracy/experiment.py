# ---
# description: ExpSketch accuracy vs mantissa bits p across log10(Lambda)
# ---
"""
Experiment: How mantissa bits p affect cardinality estimation accuracy in ExpSketch.
Uses ExpSketchCustomFloat with q=6 exponent bits and varies p from 1 to 23.
Plots mean relative error vs log10(Lambda) for each p value.
"""

import numpy as np
import tqdm


from weighted_cardinality_estimation import ExpSketch, FastExpSketchCustomFloat, stat
from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager
from data_for_figure_dataclass import DataModel

# REVIEWED AND ACCEPTED DRAFT VARIABLES. RSE estimation needs more samples; 500 gives ~4.5% estimation error.
# BENCHMARK: DRAFT=0: >80s, DRAFT=1: 29.6s, DRAFT=2: 8.2s.
match DRAFT:
    case DraftLevel.DRAFT_FINAL_VERSION:
        N_REPS = 5000
        N_LAMBDAS = 50
    case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
        N_REPS = 20
        N_LAMBDAS = 30
    case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
        N_REPS = 10
        N_LAMBDAS = 15

N_ELEMENTS = 500
M = 100
Q_BITS = 6
P_VALUES = [1, 2, 3, 4, 5, 6, 7]
LOG_LAMBDAS = np.linspace(-10, 10, N_LAMBDAS)
LAMBDA_VALUES = (10.0**LOG_LAMBDAS).tolist()


def measure_error(p: int, total_weight: float) -> float:
    errors = []
    for rep in range(N_REPS):
        elems, weights = stat.weighted_stream(N_ELEMENTS, total_weight, dist=stat.Uniform())
        sk = FastExpSketchCustomFloat(M, seed=rep, exp_bits=Q_BITS, mant_bits=p)
        sk.add_many(elems, weights)
        errors.append(stat.relative_error(sk.estimate(), total_weight))
    return float(np.sqrt(np.mean(np.array(errors) ** 2)))


def measure_error_float64(total_weight: float) -> float:
    errors = []
    for rep in range(N_REPS):
        elems, weights = stat.weighted_stream(N_ELEMENTS, total_weight, dist=stat.Uniform())
        sk = ExpSketch(M, seed=rep)
        sk.add_many(elems, weights)
        errors.append(stat.relative_error(sk.estimate(), total_weight))
    return float(np.sqrt(np.mean(np.array(errors) ** 2)))



def main() -> None:
    out = GeneratedOutputManager(__file__)

    errors_by_p = []
    TOTAL_PBAR_VALUE = len(P_VALUES)
    pbar = tqdm.tqdm(total=TOTAL_PBAR_VALUE, desc="mantissa bits", unit="p", colour="#2ca02c", mininterval=10.0)
    for p in P_VALUES:
        errors = [measure_error(p, lam) for lam in LAMBDA_VALUES]
        errors_by_p.append(errors)
        pbar.update(1)
    pbar.close()

    errors_f64 = [measure_error_float64(lam) for lam in LAMBDA_VALUES]

    out.save_dataclass(
        DataModel(
            log_lambdas=LOG_LAMBDAS.tolist(),
            errors_by_p=errors_by_p,
            p_values=P_VALUES,
            errors_float64=errors_f64,
            q_bits=Q_BITS,
            m=M,
        ),
        DataModel,
    )


if __name__ == "__main__":
    main()
