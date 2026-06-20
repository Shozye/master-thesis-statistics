# ---
# description: ExpSketch register value histogram for custom float q=5 p=5
# ---
"""
Experiment: ExpSketch register utilization histogram.

Shows how ExpSketchCustomFloat (sign=0, q=5, p=5) distributes values across
all theoretically possible register values after adding a single element.
Three overlaid histograms for Lambda=2^0, 2^5, 2^-5.
"""

import numpy as np

from weighted_cardinality_estimation import FastExpSketchCustomFloat
from generated_output_manager import DRAFT, DraftLevel, GeneratedOutputManager
from data_for_figure_dataclass import DataModel

# REVIEWED AND ACCEPTED DRAFT VARIABLES. Deterministic; M controls histogram smoothness.
# BENCHMARK: DRAFT=0: 1.8s, DRAFT=1: 1.2s, DRAFT=2: 1.1s.
match DRAFT:
    case DraftLevel.DRAFT_FINAL_VERSION:
        M = 50000
    case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
        M = 5000
    case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
        M = 1000

Q_BITS = 5
P_BITS = 5
WEIGHTS = [
    (2.0**0, "#1f77b4", r"$\Lambda=2^0$"),
    (2.0**5, "magenta", r"$\Lambda=2^5$"),
    (2.0**-5, "#2ca02c", r"$\Lambda=2^{-5}$"),
]

Q_BITS_2 = 4
P_BITS_2 = 5
LAMBDA_2 = 2.0**0
M_VALUES = [500, 1000, 2000]
M_COLORS = ["#1f77b4", "magenta", "#2ca02c"]


def all_positive_custom_float_values(q: int, p: int) -> np.ndarray:
    """Enumerate all positive representable values of a custom float (sign=0, q, p)."""
    bias = 2 ** (q - 1) - 1
    n_mant = 2**p
    values = []
    # Subnormals
    for m in range(1, n_mant):
        values.append(2.0 ** (1 - bias) * (m / n_mant))
    # Normals
    for e in range(1, 2**q - 1):
        for m in range(n_mant):
            values.append(2.0 ** (e - bias) * (1 + m / n_mant))
    return np.array(sorted(values))



def _collect_counts(q_bits, p_bits, weight, m) -> list[int]:
    """Collect register histogram counts for a single configuration."""
    possible_values = all_positive_custom_float_values(q_bits, p_bits)
    sk = FastExpSketchCustomFloat(m, seed=42, exp_bits=q_bits, mant_bits=p_bits)
    sk.add("element", weight)
    regs = np.array(sk.__getstate__()[4])
    counts = np.zeros(len(possible_values), dtype=int)
    for i, val in enumerate(possible_values):
        counts[i] = np.sum(np.isclose(regs, val, rtol=1e-12))
    return counts.tolist()


def main() -> None:
    out = GeneratedOutputManager(__file__)

    counts_left = [
        _collect_counts(Q_BITS, P_BITS, w, M) for w, _, _ in WEIGHTS
    ]
    counts_right = [
        _collect_counts(Q_BITS_2, P_BITS_2, LAMBDA_2, m) for m in M_VALUES
    ]

    out.save_dataclass(
        DataModel(
            counts_left=counts_left,
            weights_left=[w for w, _, _ in WEIGHTS],
            labels_left=[label for _, _, label in WEIGHTS],
            q_bits=Q_BITS,
            p_bits=P_BITS,
            m=M,
            counts_right=counts_right,
            m_values=M_VALUES,
            q_bits_2=Q_BITS_2,
            p_bits_2=P_BITS_2,
        ),
        DataModel,
    )


if __name__ == "__main__":
    main()
