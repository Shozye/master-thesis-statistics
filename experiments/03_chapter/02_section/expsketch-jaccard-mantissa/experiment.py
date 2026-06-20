# ---
# description: RSE of ExpSketch Jaccard similarity vs mantissa bits p for different exponent bits q
# ---
"""Sweep mantissa bits p=1..9 and measure RSE of jaccard_struct for various true Jaccard values.

Uses clone_with optimization: ingest once at max precision, then truncate to each (q, p).
3 subplots for q=5, 7, 9. Lines for J=0.2, 0.5, 0.8, 0.95, 0.97.
"""

import numpy as np
import tqdm
from weighted_cardinality_estimation import FastExpSketchCustomFloat, stat
from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager
from data_for_figure_dataclass import DataModel

# REVIEWED AND ACCEPTED DRAFT VARIABLES. Jaccard RSE measurement; 500 trials sufficient for stable curves.
# BENCHMARK: DRAFT=0: >80s, DRAFT=1: 31.7s, DRAFT=2: 1.5s.
match DRAFT:
    case DraftLevel.DRAFT_FINAL_VERSION:
        N_TRIALS = 1000
        N_ELEMENTS = 1000
    case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
        N_TRIALS = 50
        N_ELEMENTS = 1000
    case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
        N_TRIALS = 3
        N_ELEMENTS = 100

M = 100
Q_VALUES = [5, 7, 9]
P_VALUES = list(range(1, 10))
J_VALUES = [0.2, 0.5, 0.8, 0.95, 0.97]
Q_MAX = 11  # max exponent bits for ingestion
P_MAX = 23  # max mantissa bits for ingestion (float32 level)


def theoretical_rse(j: float) -> float:
    """Theoretical RSE for structural Jaccard: sqrt((1-J)/(m*J))."""
    return np.sqrt((1 - j) / (M * j))


def measure_rse(q: int, j: float) -> list[float]:
    """Measure RSE for each p in P_VALUES at given q and target Jaccard j."""
    errors_by_p = [[] for _ in P_VALUES]
    (a_elems, w_a), (b_elems, w_b) = stat.jaccard_streams(
        N_ELEMENTS, 10.0, j, dist=stat.Uniform(), common=stat.CommonPlacement.RANDOM
    )

    for trial in range(N_TRIALS):
        # Ingest at max precision
        sk_a = FastExpSketchCustomFloat(M, seed=trial, exp_bits=Q_MAX, mant_bits=P_MAX)
        sk_b = FastExpSketchCustomFloat(M, seed=trial, exp_bits=Q_MAX, mant_bits=P_MAX)

        sk_a.add_many(a_elems, w_a)
        sk_b.add_many(b_elems, w_b)

        # Truncate to target q, then sweep p
        sk_a_q = sk_a.clone_with(exp_bits=q, mant_bits=P_MAX)
        sk_b_q = sk_b.clone_with(exp_bits=q, mant_bits=P_MAX)

        for i, p in enumerate(P_VALUES):
            sk_a_p = sk_a_q.clone_with(exp_bits=q, mant_bits=p)
            sk_b_p = sk_b_q.clone_with(exp_bits=q, mant_bits=p)
            j_est = sk_a_p.jaccard_struct(sk_b_p)
            errors_by_p[i].append((j_est - j) / j if j > 0 else j_est)

    return [float(np.sqrt(np.mean(np.array(e) ** 2))) for e in errors_by_p]



def main() -> None:
    out = GeneratedOutputManager(__file__)

    # Collect all RSE data first
    rse_data = []
    TOTAL_PBAR_VALUE = len(Q_VALUES)
    pbar = tqdm.tqdm(total=TOTAL_PBAR_VALUE, desc="q values", colour="green", unit="subplot", mininterval=10.0)
    for q in Q_VALUES:
        rse_q = [measure_rse(q, j) for j in J_VALUES]
        rse_data.append(rse_q)
        pbar.update(1)
    pbar.close()

    out.save_dataclass(
        DataModel(rse_data=rse_data, q_values=Q_VALUES, p_values=P_VALUES, j_values=J_VALUES, m=M),
        DataModel,
    )


if __name__ == "__main__":
    main()
